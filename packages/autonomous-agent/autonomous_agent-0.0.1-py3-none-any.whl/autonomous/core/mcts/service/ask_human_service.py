from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface
from autonomous.infra.llm.llms import llm


def create_ask_human_service(ask_human_prompt: BasePromptTemplateInterface) -> Runnable:
    ask_human_prompt = ask_human_prompt.generate_prompt_template()
    return ask_human_prompt | llm | StrOutputParser()
