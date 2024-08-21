from typing import Optional, Sequence

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableConfig, RunnableParallel, RunnableLambda
from langchain_core.runnables.utils import Input, Output
from langchain_core.tools import BaseTool, render_text_description
from loguru import logger as log
from pydantic.v1 import BaseModel, Field

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface
from autonomous.infra.llm.llms import llm
from autonomous.infra.parsers import RepairableJsonOutputParser


class PerformTaskResponse(BaseModel):
    """"""
    action: str = Field(title="action", description="The action to take")
    action_content: str = Field(title="action_content", description="Content of action input")


class TaskPerformService(Runnable):
    def __init__(
            self,
            tools: Sequence[BaseTool],
            perform_prompt: BasePromptTemplateInterface
    ):
        self.tool_map: dict[str, BaseTool] = {t.name: t for t in tools}
        _parser = RepairableJsonOutputParser(pydantic_object=PerformTaskResponse)
        _retry_error_parser = RetryWithErrorOutputParser.from_llm(llm=llm, parser=_parser, max_retries=3)
        _perform_task_prompt = perform_prompt.generate_prompt_template()
        _perform_chain = _perform_task_prompt.partial(
            tools=render_text_description(list(tools)),
            tool_names=", ".join([t.name for t in tools])
        ) | llm | StrOutputParser()
        self.perform_chain = (RunnableParallel(
            completion=_perform_chain, prompt_value=_perform_task_prompt.partial(
                tools=render_text_description(list(tools)),
                tool_names=", ".join([t.name for t in tools])
            )
        ) | RunnableLambda(lambda x: _retry_error_parser.parse_with_prompt(completion=x["completion"],
                                                                           prompt_value=x["prompt_value"])))

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        log.debug("perform task:{}", input)
        task = input["task"]
        messages: list[dict[str, str]] = input["messages"]
        task_status = input.get("task_status", None)
        # context = input["context"]
        # 第一次进入status == None, 不为None，就是第二次进入
        if task_status == "completed":
            return input
        elif task_status == "interrupt":
            response = self.perform_chain.invoke({
                "input": task,
                "context": "".join([message["task_response"] for message in messages]),
                "intermediate_action": [AIMessage(content=input["ask_human"]),
                                        HumanMessage(content=input["human_feedback"])]
            })
            log.debug("response:{}", response)
        else:
            # status == None
            response = self.perform_chain.invoke({
                "input": task,
                "context": "".join([message["task_response"] for message in messages]),
            })
            log.debug("response:{}", response)

        if response["action"] == "ask_human":
            return {
                "task": task,
                "task_result": None,
                "task_status": "interrupt",
                "ask_human": response["action_content"],
                "human_feedback": None,
            }
        elif response["action"] == "Final Answer":
            return {
                "task": task,
                "task_result": response["action_content"] if "action_content" in response else "我无法得到结果",
                "task_status": "completed",
                "ask_human": None,
                "human_feedback": None,
            }
        elif response["action"] in self.tool_map:
            action_input = response["action_content"]
            # TODO 得到工具的响应后要重新回答该问题?
            tool_response = self.tool_map[response["action"]].invoke(action_input, config)
            return {
                "task": task,
                "task_result": tool_response,
                "task_status": "completed",
                "ask_human": None,
                "human_feedback": None,
            }


def perform_task_service(
        tools: list[BaseTool],
        perform_prompt: BasePromptTemplateInterface
) -> Runnable:
    return TaskPerformService(
        tools,
        perform_prompt
    )
