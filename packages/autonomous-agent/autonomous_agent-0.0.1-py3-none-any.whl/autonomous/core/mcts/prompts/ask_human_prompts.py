from langchain_core.prompts import ChatPromptTemplate

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface

ask_human_system_message = """
仔细阅读并理解用户的问题, 对用户给定的问题进行总结, 生成一个专业并友好的问题来询问用户以获取用户的帮助. \
生成的问题要包含用户给定原始问题的全部信息, 并且尽可能给用户一些提示以方便用户回答. 生成问题时使用第一人称.

让我们一步一步思考.
"""
ask_human_human_message = """
给你的问题列表如下:
{questions}
"""


class AskHumanPromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", ask_human_system_message),
            ("human", ask_human_human_message),
        ])
