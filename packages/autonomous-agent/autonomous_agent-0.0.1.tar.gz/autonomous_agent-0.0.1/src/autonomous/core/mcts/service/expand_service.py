from typing import Any

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, Runnable, RunnableParallel

from autonomous.core.mcts.prompts.expand_prompts import format_history_actions
from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface
from autonomous.infra.llm.llms import llm


class PredictActionOutputParser(StrOutputParser):
    def parse(self, text: str) -> str:
        striped_text = text.strip().strip("```").strip("\n")
        action_prefix = "Action:"
        if not striped_text.startswith(action_prefix):
            raise OutputParserException(f"Could not parse LLM Output: {text}")
        action_str = striped_text[len(action_prefix):]
        return action_str.strip()
        # return text


class PredictSubObjectiveOutputParser(StrOutputParser):
    def parse(self, text: str) -> str:
        striped_text = text.strip().strip("```").strip("\n")
        action_prefix = "Sub Objective:"
        if not striped_text.startswith(action_prefix):
            raise OutputParserException(f"Could not parse LLM Output: {text}")
        action_str = striped_text[len(action_prefix):]
        return action_str.strip()


def sub_objective_chain(sub_objective_prompt: BasePromptTemplateInterface):
    return RunnablePassthrough.assign(
        history_actions=lambda x: format_history_actions(x["history_actions"])
    ) | sub_objective_prompt.generate_prompt_template() | llm | PredictSubObjectiveOutputParser()


def next_action_chain(next_action_prompt: BasePromptTemplateInterface):
    return RunnablePassthrough.assign(
        history_actions=lambda x: format_history_actions(x["history_actions"])
    ) | next_action_prompt.generate_prompt_template() | llm | PredictActionOutputParser()


def knowledge_retrieve_chain(knowledge_retrieve_prompt: BasePromptTemplateInterface):
    return RunnablePassthrough.assign(
        history_actions=lambda x: format_history_actions(x["history_actions"])
    ) | knowledge_retrieve_prompt.generate_prompt_template() | llm | PredictActionOutputParser()


def actions_output(multi_viewpoint: Any) -> list[str]:
    return [multi_viewpoint["sub_objective"], multi_viewpoint["action"], multi_viewpoint["retrieve"]]


def create_expand_service(
        sub_objective_prompt: BasePromptTemplateInterface,
        next_action_prompt: BasePromptTemplateInterface,
        knowledge_retrieve_prompt: BasePromptTemplateInterface
) -> Runnable:
    """扩展节点:
    TODO 后续需要通过对目标问题的分析后，加载目标问题领域的知识，然后获取该问题在目标领域里面的可能的行动空间(先验经验)
    """
    _sub_objective_chain = sub_objective_chain(sub_objective_prompt)
    _next_action_chain = next_action_chain(next_action_prompt)
    _knowledge_retrieve_chain = knowledge_retrieve_chain(knowledge_retrieve_prompt)
    return RunnableParallel(sub_objective=_sub_objective_chain, action=_next_action_chain,
                            retrieve=_knowledge_retrieve_chain) | actions_output
