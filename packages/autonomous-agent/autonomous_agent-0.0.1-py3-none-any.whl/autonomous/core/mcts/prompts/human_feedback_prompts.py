from langchain_core.prompts import ChatPromptTemplate

feedback_extract_system_message = """
从用户反馈的信息中提取和给定问题有关的知识和信息. 并将提取出的知识和信息回复给我.

让我们一步一步思考.
"""

feedback_extract_human_message = """
这是给定的问题:
{question}

这是用户基于给定问题的响应信息:
{human_feedback}
"""

feedback_extract_prompt = ChatPromptTemplate.from_messages([
    ("system", feedback_extract_system_message),
    ("human", feedback_extract_human_message)
])
