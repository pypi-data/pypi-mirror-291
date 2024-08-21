from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface

perform_task_system_message = """
为了全面且准确的回复用户, 你可以要求用户使用最合适的方式获取有助于回答用户原始问题的信息, 用户可以使用的工具有:
{tools}
"""

perform_task_format_instruction_message = """
回复我时，必须以下两种格式之一输出回复.

**Option 1:**
如果你希望用户使用工具来获取更丰富的信息,请使用此选项. 采用以下格式化的 JSON Markdown 代码片段:
```json
{{
    "action": string, \\ The action to take. action MUST be one of {tool_names}!
    "action_content": $INPUT \\ The input to the action.
}}
```

**Option 2:**
如果你认为你有充足的信息来直接来回复用户, 请使用此选项. 采用以下格式化的 JSON Markdown 代码片段:
```json
{{
    "action": "Final Answer", \\ text MUST be 'Final Answer'!
    "action_content": string \\ You should put what you want to return to use here. Don't put double quotes mark(") in the content!
}}
```
"""
perform_task_context_message = """
你可以参考如下信息:

{context}
"""
perform_task_human_message = """
这是用户的输入
{input}

思考步骤:
1. 深入理解用户的输入信息, 分析出用户输入中存在模糊的/不完整的/不具体的信息.
2. 如果用户的输入有模糊的/不完整的/不具体的信息时, 优先要求用户使用工具来获取更充分的上下文信息. 否则直接回复用户.

(记住: 按照回复格式指令惊醒回复, 回复的内容必须是有效的JSON格式, 必须包含action和action_content字段)
"""


class PerformPromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", perform_task_system_message),
            ("system", perform_task_format_instruction_message),
            ("system", perform_task_context_message),
            ("human", perform_task_human_message),
            MessagesPlaceholder(variable_name="intermediate_action", optional=True)
        ])
