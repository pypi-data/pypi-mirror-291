import json

import json_repair
from pydantic.v1 import BaseModel


# class TestObject(BaseModel):
#     title: str = Field(title="title", description="回复的标题")
#     content: str = Field(title="content", description="回复的内容")
#
#
# response_schemas = [
#     ResponseSchema(name="content", description="回复的内容"),
#     ResponseSchema(
#         type="$INPUT",
#         name="title",
#         description="回复的标题",
#     ),
# ]
# output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
#
# print(output_parser.get_format_instructions())
#
# prompt = ChatPromptTemplate.from_messages([
#     ("system", """
# {instruction}
#     """),
#     ("human", """
# Question: {question}
# """),
#
# ])
#
# outpt =JsonOutputParser(pydantic_object=TestObject)
# chain = prompt.partial(instruction=output_parser.get_format_instructions()) | llm | output_parser
# resp = chain.invoke({
#     "question": "帮我写一个给孩子高中三年的规划吧!"
# })
#
# print(resp)

class Action(BaseModel):
    action: str
    action_content: str


test_string = """
{"action": "hello", "action_content": "world, "\"wangweimin"\""}
"""
ss = json_repair.repair_json(test_string, skip_json_loads=True)

print(ss)
ss = json_repair.loads(test_string)
print(ss)

json.loads(ss)
