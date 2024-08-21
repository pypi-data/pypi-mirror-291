from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface
from autonomous.infra.settings import settings
from tests.fake_tools import ask_human

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
    "row_factory": dict_row,
}

pool = ConnectionPool(
    # Example configuration
    conninfo=str(settings.db_url),
    max_size=20,
    kwargs=connection_kwargs
)

evaluation_current_task_system_message = """\
严格遵循下面提供的评估标准来对当前行动和结果进行评估.

评估标准 (评分, 0-100):
- 一致性: 评估当前行动的结果是否为当前行动的回复? 如果当前行动执行结果的内容完全是当前行动的答复, 不存在任何不相关的内容, 则给40分. 否则给0分.
- 完整性: 评估当前行动的结果是否完成行动的要求没有遗漏? 如果是则给予20分,否则给予0分.
- 重要性: 评估当前行动及其结果对解决给定问题是否具有促进作用?如果对解决给定问题有直接的巨大促进作用则给40分, 如果有间接作用则给1分, 如果没有明显促进作用则给0分.

评估步骤:
1. 仔细阅读用户给定的最终需要解决的问题, 确保你完全理解了给定问题.
2. 按照评估标准的各项要求, 对当前行动及其结果进行各项独立评分, 并给出你的评判依据.
3. 根据上述给予的各项的分数进行相加求出总分数.

给定最终需要解决的目标问题(简称给定问题)如下: 
{human_input_task}
"""
evaluation_current_task_format_instruction_message = """\
回复我时, 必须采用以下模式格式化的 JSON Markdown 代码片段:
```
{{
    "evaluation": string, \\ Your evaluation about current task and response
    "score": int \\ Total addictive score 
}}
```
"""
evaluation_current_task_human_message = """
Current Action:
```
{task}
```

Response to Current Action:
```
{task_response}
```

严格遵循评估标准来对当前行动及其结果进行评估.

按照格式指令要求回复(JSON格式, 回复内容中必须包含evaluation, score字段).
"""


class TestCurrentBasePromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", evaluation_current_task_system_message),
            ("system", evaluation_current_task_format_instruction_message),
            ("human", evaluation_current_task_human_message),
        ])


evaluation_solution_system_message = """
严格遵循下面提供的评估标准来对由用户提供的多个行动和响应组成的解决方案进行评估. 不要编造答案, 对于你无法回答的问题, 你直接回复你不知道.

评估标准(评分: 0-100):
- 完成质量: 如果解决方案完全满足解决给定问题的所有要求则给予40分, 如果大部分满足要求给予20分, 其他情况给予0分.
- 目标一致性: 解决方案来评估如果完全满足给定问题的全部目标则给40分, 如果大部分满足则给20分, 其他情况则给0分.
- 给定问题是否完全解决: 如果解决方案完全解决了给定问题则给20分, 否则给0分.

评估步骤:
1. 仔细阅读用户给定的最终需要解决的问题, 以确保你完全理解了给定的问题.
2. 按照评估标准的各项要求, 对提供的解决方案进行各项独立评分, 并给出你的评判依据.
3. 根据上述给予的各项的分数进行相加求出总分数.
4. 提供的解决方案是否完全解决了给定的问题, 并且解决给定问题的所有要求被全部满足?
"""

evaluation_solution_format_instruction_message = """
回复我时, 必须采用以下模式格式化的 JSON Markdown 代码片段:
```
{{
    "evaluation": string, \\ Your evaluation about current task and response
    "score": int, \\ Total addictive score
    "is_solved": bool \\ Whether the given problem have been solved entirely
}}
```
"""

evaluation_solution_human_message = """
遵循评估标准, 对由历史记录中多个行动及其响应组成的解决方案进行评估. 返回给我评估结果.

按照格式指令要求回复(JSON格式, 回复内容中必须包含evaluation, score, is_solved字段).

给定的问题是: 
```
{human_input_task}
```

给定问题的要求是: 
```
{requirements}
```
"""


class TestSolutionBasePromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", evaluation_solution_system_message),
            ("system", evaluation_solution_format_instruction_message),
            ("human", evaluation_solution_human_message),
            MessagesPlaceholder("intermediate_steps", optional=True),
        ])


cu = TestCurrentBasePromptTemplate()
so = TestSolutionBasePromptTemplate()

# evaluation_current_prompt_template
# evaluation_solution_prompt_template
# sub_objective_prompt_template
# next_action_prompt_template
# knowledge_retrieve_prompt_template
# perform_prompt_template
# ask_human_prompt_template
config = {
    "recursion_limit": 100,
    "configurable": {
        "thread_id": "50016",
        "tools": [ask_human],
        "evaluation_current_prompt_template": cu,
        "evaluation_solution_prompt_template": so
    }
}
