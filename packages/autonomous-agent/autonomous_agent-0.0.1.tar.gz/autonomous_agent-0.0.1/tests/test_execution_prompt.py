import operator
from typing import TypedDict, Annotated, List, Sequence

from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.tools import tool, render_text_description, BaseTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph

from autonomous.core.mcts.prompts.execution_prompts import perform_task_prompt
from autonomous.core.mcts.service.execution_service import TaskPerformService
from autonomous.infra.llm.llms import llm

# set_verbose(True)
# set_debug(True)


@tool
def ask_human(query: str) -> str:
    """当你需要用户提供更多信息时，使用该工具对用户提出问题"""
    print("------")
    return query


@tool
def multiple(a: int, b: int) -> int:
    """仅仅当你需要计算乘法的时候，才使用该工具"""
    print("---------")
    return a + b

@tool
def hello(string: str) -> str:
    """当你需要获取人物信息的时候, 使用该工具"""
    print("hello")
    return "xiao laoban bucuo"
tools: Sequence[BaseTool] = [multiple, hello, ask_human]

prompt = perform_task_prompt.partial(
        tools=render_text_description(list(tools)),
        tool_names=", ".join([t.name for t in tools]),
    )

chain = prompt | llm | JsonOutputParser()
# agent = create_react_agent(llm, tools, prompt=use_tool_prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools)
# print(agent_executor.invoke({"input": "基于北京的春天做一首诗?"}))

# r1 = chain.invoke({
#     "input": "221 / 112 ?",
# })
# print(r1)
# r2 = chain.invoke({
#     "input": "221 / 112 ?",
#     "intermediate_action": [
#         AIMessage(content=r1["action_input"]),
#         HumanMessage(content="需要得到商和余数")
#     ]
# })

# print(r2)


task_service = TaskPerformService(tools)
r3 = task_service.invoke({"task": "221 + 112 ?",})
print(r3)
thread = {"configurable": {"thread_id": "thread-3"}}
class State(TypedDict):
    input: str
    action: str
    action_input: str
    history: Annotated[List[BaseMessage], operator.add]
    feed_back: str


def use_tool(state: State):
    resp = chain.invoke({
        "input": state["input"],
        "history": state["history"]
    })
    return {
        "input": state["input"],
        "action": resp["action"],
        "action_input": resp["action_input"]
    }

def should_continue(state: State):
    action = state["action"]
    if action == "ask_human":
        return "human_feedback"
    elif action == "Final Answer":
        return END
    else:
        return END


def human_feedback(state: State):
    action_input = state["action_input"]
    feedback = state["feed_back"]
    print(f"{action_input}: {feedback}")
    return {
        "history": [AIMessage(content=action_input), HumanMessage(content=feedback)]
    }


workflow = StateGraph(State)
workflow.add_node("use_tool", use_tool)
workflow.add_node("human_feedback", human_feedback)
workflow.set_entry_point("use_tool")
workflow.add_conditional_edges("use_tool", should_continue)
workflow.add_edge("human_feedback", "use_tool")

c = workflow.compile(checkpointer=MemorySaver(), interrupt_before=["human_feedback"], debug=True)

rsp = c.invoke({
    "input": "基于山间做一首诗",

}, config=thread)

print(rsp)

response = input(rsp["action_input"])

c.update_state(thread, {"feed_back": response}, )
rsp = c.invoke(None, thread)
print(rsp)