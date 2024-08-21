import pickle
from typing import Optional

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from loguru import logger as log

from autonomous.core.mcts.entity.evaluation_model import Evaluation
from autonomous.core.mcts.entity.node_model import Node
from autonomous.core.mcts.entity.state_model import State
from autonomous.core.mcts.entity.strategy_model import Strategy
from autonomous.core.mcts.prompts.ask_human_prompts import AskHumanPromptTemplate
from autonomous.core.mcts.prompts.evaluation_prompts import EvaluationCurrentPromptTemplate, EvaluationSolutionPromptTemplate
from autonomous.core.mcts.prompts.execution_prompts import PerformPromptTemplate
from autonomous.core.mcts.prompts.expand_prompts import SubObjectivePromptTemplate, NextActionPromptTemplate, \
    KnowledgeRetrievePromptTemplate
from autonomous.core.mcts.prompts.human_input_process_prompt import format_objective
from autonomous.core.mcts.service.ask_human_service import create_ask_human_service
from autonomous.core.mcts.service.evaluation_service import create_evaluation_service
from autonomous.core.mcts.service.execution_service import perform_task_service
from autonomous.core.mcts.service.expand_service import create_expand_service
from autonomous.core.mcts.service.human_feedback_service import create_feedback_extract_service
from autonomous.core.mcts.service.human_input_process_service import create_extract_objective_requirements_service


def init_node(state: State, config: Optional[RunnableConfig] = None):
    init_task = "分析用户输入问题的目标和要求, 以及该问题所涉及的领域和背景信息."  # 分析出目标,要求, 领域, 背景
    # 提取给定的问题的主要目标和要求

    extraction_objective_result: dict = create_extract_objective_requirements_service().invoke({
        "human_input_task": state["human_input_task"]
    })

    log.debug("extraction_result: {}", extraction_objective_result)
    init_task_result = format_objective(extraction_objective_result)
    log.debug("init_task_result: {}", init_task_result)
    # 评估任务和结果
    # mcts_prompt: MctsPrompt = config['configurable']['prompts'] if config['configurable']['prompts'] else MctsPrompt()

    _evaluation_current_prompt = config.get("configurable").get(
        "evaluation_current_prompt_template") if config.get(
        "configurable").get(
        "evaluation_current_prompt_template") else EvaluationCurrentPromptTemplate()
    _evaluation_solution_prompt = config.get("configurable").get(
        "evaluation_solution_prompt_template") if config.get(
        "configurable").get(
        "evaluation_solution_prompt_template") else EvaluationSolutionPromptTemplate()
    evaluation_results = create_evaluation_service(
        evaluation_current_prompt=_evaluation_current_prompt,
        evaluation_solution_prompt=_evaluation_solution_prompt
    ).invoke(
        {
            "human_input_task": state["human_input_task"],
            "task": init_task,
            "task_response": init_task_result,
            "requirements": extraction_objective_result["requirements"],
        },
        # config={'callbacks': [ConsoleCallbackHandler()]}
    )
    log.info(f"evaluation_results: {evaluation_results}")
    # 构建第一个节点
    root = Node(parent=None, task=init_task, evaluation=Evaluation(**evaluation_results),
                task_response=init_task_result)
    return {
        "root": pickle.dumps(root),
        "objective_requirements": extraction_objective_result["requirements"],
    }


def select_node(state: State):
    """从树中选择最优节点"""
    # 从树的最优子节点开始, 产生N个可能的方案，然后进入下一步
    root: Node = pickle.loads(state['root'])
    # 获取当前最优节点
    best_candidate: Node = root.get_best_child() if root.children else root
    messages = best_candidate.get_trajectory()
    log.info(f"最优路经：{messages}")
    return {
        "best_candidate": pickle.dumps(best_candidate)
    }


def expand_node(state: State, config: Optional[RunnableConfig] = None):
    """对当前最后节点进行扩展"""
    # 获取当前最优节点
    best_candidate: Node = pickle.loads(state['best_candidate'])
    # 获取当前节点的轨迹，即局面
    messages = best_candidate.get_trajectory()
    # strategies = create_expand_service().batch(inputs=[{
    #     "intermediate_steps": [HumanMessage(content=intermediate_steps_prompt_template.format(
    #         task_content=message["task"],
    #         task_result=message["task_response"])) for message in messages],
    #     "objectives": state["objectives"]
    # } for _ in range(3)])

    _sub_objective_prompt = config.get("configurable").get(
        "sub_objective_prompt_template") if config.get(
        "configurable").get(
        "sub_objective_prompt_template") else SubObjectivePromptTemplate()

    _next_action_prompt = config.get("configurable").get(
        "next_action_prompt_template") if config.get(
        "configurable").get(
        "next_action_prompt_template") else NextActionPromptTemplate()

    _knowledge_retrieve_prompt = config.get("configurable").get(
        "knowledge_retrieve_prompt_template") if config.get(
        "configurable").get(
        "knowledge_retrieve_prompt_template") else KnowledgeRetrievePromptTemplate()

    strategies = create_expand_service(
        sub_objective_prompt=_sub_objective_prompt,
        next_action_prompt=_next_action_prompt,
        knowledge_retrieve_prompt=_knowledge_retrieve_prompt
    ).invoke({
        "human_input_task": state["human_input_task"],
        "history_actions": messages
    })
    log.info(f"扩展节点:{strategies}")
    return {
        "strategies": [Strategy(
            task=s,
            task_status=None,
            task_result=None,
            ask_human=None,
            human_feed_back=None,
        ) for s in strategies],
    }


def perform_node(state: State, config: Optional[RunnableConfig] = None):
    """执行当前任务.
    @TODO 当前任务信息不够需要人工干预？

    """
    # 对候选的5个方案进行模拟实施
    # 获取当前最优节点
    best_candidate: Node = pickle.loads(state['best_candidate'])
    # 获取当前节点的轨迹，即局面
    messages = best_candidate.get_trajectory()
    configurable = config["configurable"]
    log.debug("tools: {}", configurable.get("tools", []))
    # perform_task_system_template: str = None,
    # perform_task_format_instruction_template: str = None,
    # perform_task_context_template: str = None,
    # perform_task_human_template: str = None

    _perform_prompt = config.get("configurable").get(
        "perform_prompt_template") if config.get(
        "configurable").get(
        "perform_prompt_template") else PerformPromptTemplate()

    task_execution_results = perform_task_service(
        tools=configurable.get("tools", []),
        perform_prompt=_perform_prompt
    ).batch(inputs=[
        {
            **dict(strategy),
            "messages": messages
        } for strategy in state["strategies"]
    ])
    log.debug("task results:{}", task_execution_results)
    return {
        "strategies": [Strategy(**strategy_dict) for strategy_dict in task_execution_results]
    }


def evaluate_node(state: State, config: Optional[RunnableConfig] = None):
    """对当前子节点候选方案进行评估

    @TODO 评估过程需要领域的先验经验，否则如何评估准确?

    """
    # 从树的最优子节点开始, 产生N个可能的方案，然后进入下一步
    root: Node = pickle.loads(state['root'])
    # 获取当前最优节点
    best_candidate: Node = root.get_best_child() if root.children else root
    # 对5个方案执行后的局面进行评估
    # 获取当前节点的轨迹，即局面
    messages = best_candidate.get_trajectory()
    _evaluation_current_prompt = config.get("configurable").get(
        "evaluation_current_prompt_template") if config.get(
        "configurable").get(
        "evaluation_current_prompt_template") else EvaluationCurrentPromptTemplate()
    _evaluation_solution_prompt = config.get("configurable").get(
        "evaluation_solution_prompt_template") if config.get(
        "configurable").get(
        "evaluation_solution_prompt_template") else EvaluationSolutionPromptTemplate()
    _evaluation_results = create_evaluation_service(
        evaluation_current_prompt=_evaluation_current_prompt,
        evaluation_solution_prompt=_evaluation_solution_prompt
    ).batch(inputs=[
        {
            "human_input_task": state["human_input_task"],
            "task": strategy.task,
            "task_response": strategy.task_result,
            "requirements": state["objective_requirements"],
            "messages": messages,
        }
        for strategy in state["strategies"]
    ],
        # config={'callbacks': [ConsoleCallbackHandler()]}
    )
    log.info(f"评估结果：{_evaluation_results}")
    evaluation_results = [Evaluation(**e) for e in _evaluation_results]
    resolved = any(evaluation.found_solution for evaluation in evaluation_results)
    # 把strategy, result, evaluation 组合在一起
    combined = zip(state["strategies"], evaluation_results)
    for (strategy, evaluation) in combined:
        expand_node_ = Node(parent=best_candidate, task=strategy.task, evaluation=evaluation,
                            task_response=strategy.task_result)
        # 反向传播
        expand_node_.back_propagate()
        # 添加到子节点
        best_candidate.children.append(expand_node_)
    return {
        "root": pickle.dumps(root),
        "best_candidate": pickle.dumps(best_candidate),
        "evaluation_results": evaluation_results,
        "resolved": resolved
    }


def should_continue(state: State) -> str:
    resolved = state["resolved"]
    # 从树的最优子节点开始, 产生N个可能的方案，然后进入下一步
    root: Node = pickle.loads(state['root'])
    # 获取当前最优节点
    log.info(f"Tree Height:{root.height}")
    if resolved or root.height > 10:
        return "false"
    else:
        return "true"


def should_interrupt(state: State) -> str:
    strategies = state["strategies"]
    has_ask_human = any([strategy.task_status == "interrupt" for strategy in strategies])
    completed_got_answer = any([strategy.task_status == "completed" for strategy in strategies])
    if has_ask_human:
        return "ask_human_node"
    elif completed_got_answer:
        return "evaluate_node"
    else:
        raise ValueError("Something went")  # TODO 需要修改


def ask_human_node(state: State, config: Optional[RunnableConfig] = None):
    # TODO refine ask human的求助问题，更友好

    _ask_human_prompt = config.get("configurable").get(
        "ask_human_prompt_template") if config.get(
        "configurable").get(
        "ask_human_prompt_template") else AskHumanPromptTemplate()

    strategies = state["strategies"]
    service = create_ask_human_service(ask_human_prompt=_ask_human_prompt)
    response = service.invoke({
        "questions": [strategy.ask_human for strategy in strategies]
    })
    return {
        "ask_human": response
    }


def human_feedback_node(state: State):
    """"""
    strategies = state["strategies"]
    human_feedback_input = state["human_feedback"]
    log.debug("feedback from human: {}", human_feedback_input)
    service = create_feedback_extract_service()
    # 从feedback里面提取每个问题需要的反馈.
    results = service.batch(inputs=[{
        "task": dict(strategy),
        "feedback": human_feedback_input,
    } for strategy in strategies])
    log.debug("strategies after feedback: {}", results)
    # TODO 是否从feedback里面提取用户和最初问题有关的要求和目标?
    return {
        "strategies": [Strategy(**strategy_dict) for strategy_dict in results]
    }


def create_agent_service(checkpointer: BaseCheckpointSaver) -> CompiledStateGraph:
    workflow = StateGraph(State)
    workflow.add_node("init_node", init_node)
    workflow.add_node("select_node", select_node)
    workflow.add_node("ask_human_node", ask_human_node)
    workflow.add_node("expand_node", expand_node)
    workflow.add_node("perform_node", perform_node)
    workflow.add_node("evaluate_node", evaluate_node)
    workflow.add_node("human_feedback_node", human_feedback_node)
    workflow.set_entry_point("init_node")
    workflow.add_edge("init_node", "select_node")
    workflow.add_edge("select_node", "expand_node")
    workflow.add_edge("expand_node", "perform_node")
    workflow.add_conditional_edges("perform_node", should_interrupt)
    workflow.add_conditional_edges("evaluate_node", should_continue, {"true": "select_node", "false": END})
    workflow.add_edge("ask_human_node", "human_feedback_node")
    workflow.add_edge("human_feedback_node", "perform_node")
    return workflow.compile(checkpointer=checkpointer, interrupt_before=['human_feedback_node'])
