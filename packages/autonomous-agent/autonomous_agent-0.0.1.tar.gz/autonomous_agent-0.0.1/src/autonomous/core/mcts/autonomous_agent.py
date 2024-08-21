from typing import Optional

from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface
from autonomous.core.mcts.serializer.checnpointer_serializer import JarvisCheckpointSerializer
from autonomous.core.mcts.workflow.mcts_workflows import create_agent_service


class AutonomousAgent(Runnable):

    def __init__(
            self,
            pool: ConnectionPool,
            tools: list,
            evaluation_current_template: BasePromptTemplateInterface = None,
            evaluation_solution_template: BasePromptTemplateInterface = None,
            sub_objective_template: BasePromptTemplateInterface = None,
            next_action_template: BasePromptTemplateInterface = None,
            knowledge_retrieve_template: BasePromptTemplateInterface = None,
            perform_template: BasePromptTemplateInterface = None,
            ask_human_template: BasePromptTemplateInterface = None
    ):
        self.pool = pool
        self.tools = tools
        self.evaluation_current_template = evaluation_current_template
        self.evaluation_solution_template = evaluation_solution_template
        self.sub_objective_template = sub_objective_template
        self.next_action_template = next_action_template
        self.knowledge_retrieve_template = knowledge_retrieve_template
        self.perform_template = perform_template
        self.ask_human_template = ask_human_template
        with self.pool.connection() as conn:
            checkpointer = PostgresSaver(conn=conn, serde=JarvisCheckpointSerializer())
            # checkpointer.setup()
            self.agent_service = create_agent_service(checkpointer)

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        request_id = input["request_id"]
        human_input = input["human_input"]
        resume: bool = input.get("resume", False)
        config = {
            "recursion_limit": 100,
            "configurable": {
                "thread_id": request_id,
                "tools": self.tools,
                "evaluation_current_prompt_template": self.evaluation_current_template,
                "evaluation_solution_prompt_template": self.evaluation_solution_template,
                "sub_objective_prompt_template": self.sub_objective_template,
                "next_action_prompt_template": self.next_action_template,
                "knowledge_retrieve_prompt_template": self.knowledge_retrieve_template,
                "perform_prompt_template": self.perform_template,
                "ask_human_prompt_template": self.ask_human_template
            }
        }
        if resume:
            self.agent_service.update_state(config, {"human_feedback": human_input}, as_node="ask_human_node")
            return self.agent_service.invoke(None, config=config)
        else:
            return self.agent_service.invoke({"human_input_task": human_input}, config=config)

