# 通过当前局面估算下一步行动空间.
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface

sub_objective_system_message = """
你是一个专业问题分析专家, 你有全面的知识. 你善于发现和总结出给定问题的核心目标的关键需求, 并将问题拆分为一个一个的子问题和子目标, 通过完成这些子目标来最终解决给定的问题. 你需要重点关注给定问题的核心目标和关键需求.

需要解决的问题:
{human_input_task}
"""
sub_objective_human_message = """
仔细阅读给定问题, 确保完全理解给定的问题的最终目标, 根据当前问题解决的进度, 重新生成多个还未达成的子目标. 返回给我优先级最高的1个子目标.

仅仅需要你回复新的子目标内容, 不要回复其他信息.

回复格式要求:
```
Sub Objective: 
子目标的详细内容
```

让我们一步一步思考.
"""


class SubObjectivePromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", sub_objective_system_message),
            MessagesPlaceholder(variable_name="history_actions", optional=True),
            ("human", sub_objective_human_message)
        ])


next_action_system_message = """
你是一个知识全面的助理. 你关注历史行动和结果. 你总是通过历史的行动及其响应来规划接下来的行动.

需要解决的问题:
{human_input_task}
"""
next_action_human_message = """
仔细阅读给定问题, 确保完全理解给定的问题, 根据历史最后一次行动及其响应来生成下一步行动.

生成要求:
1. 行动中的任务要单一. 对于复杂的任务要拆成多个简单的独立的行动.
2. 行动要明确,清晰的说明对解决问题有什么作用.

仅仅需要回复行动的详细内容, 不要执行该行动, 不要回复其他信息.

回复格式要求:
```
Action: 
行动的详细内容
```

让我们一步一步思考.
"""


class NextActionPromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", next_action_system_message),
            MessagesPlaceholder(variable_name="history_actions", optional=True),
            ("human", next_action_human_message)
        ])


knowledge_retrieve_system_message = """
你是一个专业问题分析专家, 你善于为解决问题进行充分的信息检索. 为了解决给定问题, 你总是规划出信息检索行动.

需要解决的问题:
{human_input_task}
"""
knowledge_retrieve_human_message = """
仔细阅读给定问题, 确保完全理解给定的问题的最终目标. 根据历史行动和结果生成接下来一步的信息检索行动.

信息检索行动内容要求:
1. 行动只能包含信息检索.
2. 一个行动只能检索一个内容.
3. 行动要明确,清晰说明需要检索什么信息,以及检索该信息对解决问题的作用.

仅仅回复行动的详细内容, 不要执行该行动, 不要回复其他信息.

回复的格式要求:
```
Action: 
行动的详细内容
```

让我们一步一步思考.
"""


class KnowledgeRetrievePromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", knowledge_retrieve_system_message),
            MessagesPlaceholder(variable_name="history_actions", optional=True),
            ("human", knowledge_retrieve_human_message)
        ])


def format_history_actions(messages: list[dict]) -> list[BaseMessage]:
    history_actions: list[BaseMessage] = []
    for message in messages:
        history_actions.append(AIMessage(content=f"Action: \n{message['task']}", ))
        history_actions.append(HumanMessage(content=f"{message['task_response']}"))
    return history_actions
