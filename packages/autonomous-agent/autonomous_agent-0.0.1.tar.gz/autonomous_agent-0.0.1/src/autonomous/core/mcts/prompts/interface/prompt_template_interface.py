from abc import ABC

from langchain_core.prompts import ChatPromptTemplate


class BasePromptTemplateInterface(ABC):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        ...
