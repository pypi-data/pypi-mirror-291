from langchain_core.prompts import ChatPromptTemplate

extract_objective_system_message = """
深入理解用户输入的问题, 总结出用户输入问题的主要目标.

让我们一步一步思考.
"""

extract_objective_human_message = """
下面是用户输入的问题:
{human_input_task}

仅回复我主要目标的内容.
"""

extract_objective_prompt = ChatPromptTemplate.from_messages([
    ("system", extract_objective_system_message),
    ("human", extract_objective_human_message)
])

extract_requirement_system_message = """
深入理解用户输入的问题, 分析并总结出该问题的要求.
"""

extract_requirement_human_message = """
下面是用户输入的问题:
{human_input_task}

仅回复给我该问题的要求.
"""

extract_requirement_prompt = ChatPromptTemplate.from_messages([
    ("system", extract_requirement_system_message),
    ("human", extract_requirement_human_message)
])

extract_domain_system_message = """
深入理解用户的问题, 总结该问题的所涉及的领域.

让我们一步一步思考.
"""

extract_domain_human_message = """
下面是用户输入的问题:
{human_input_task}

仅回复我所涉及的领域即可.
"""

extract_domain_prompt = ChatPromptTemplate.from_messages([
    ("system", extract_domain_system_message),
    ("human", extract_domain_human_message)
])

extract_background_system_message = """
深入理解用户的问题, 总结出该问题所涉及的背景知识.
"""

extract_background_human_message = """
下面是用户输入的问题:
{human_input_task}

仅回复我所涉及的背景知识.
"""

extract_background_prompt = ChatPromptTemplate.from_messages([
    ("system", extract_background_system_message),
    ("human", extract_background_human_message)
])

ff = """
用户给定问题的目标:
```
{objectives}
```

用户给定问题的要求:
```
{requirements}
```

用户给定问题涉及的领域:
```
{domains}
```
"""


def format_objective(message: dict) -> str:
    return ff.format(**message)
