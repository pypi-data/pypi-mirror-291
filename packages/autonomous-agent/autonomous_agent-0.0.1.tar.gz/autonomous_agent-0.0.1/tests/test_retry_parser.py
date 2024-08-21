from langchain.output_parsers import OutputFixingParser, RetryWithErrorOutputParser
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableLambda
from pydantic.v1 import BaseModel, Field

from autonomous.infra.llm.llms import llm

template = """Based on the user question, provide an Action and Action Input for what step should be taken.
{format_instructions}
Question: {query}
Response:"""


class Action(BaseModel):
    action: str = Field(description="action to take")
    action_input: str = Field(description="input to the action")


class Action2(BaseModel):
    action: str = Field(description="action to take")


parser = JsonOutputParser(pydantic_object=Action)
parser3 = JsonOutputParser(pydantic_object=Action2)
prompt = PromptTemplate(
    template=template,
    input_variables=["query"],
    partial_variables={"format_instructions": parser3.get_format_instructions()},
)
prompt2 = ChatPromptTemplate.from_messages([
    ("system", """
    Based on the user question, provide an Action and Action Input for what step should be taken.
{format_instructions}"""),
    ("human", """Question: {query}
Response:""")
]).partial(format_instructions=parser3.get_format_instructions())
prompt_value = prompt.format_prompt(query="who is leo di caprios gf?")
print(prompt_value)

# 1. 返回 str
# 2. 转换 Json

# Action json
retry_error_parser = RetryWithErrorOutputParser.from_llm(llm, parser)

# output string
chain = prompt2 | llm | StrOutputParser()


main_chain = RunnableParallel(
    completion=chain, prompt_value=prompt2
) | RunnableLambda(lambda x: retry_error_parser.parse_with_prompt(**x))

resp = main_chain.invoke({
    "query": "who is leo di caprios gf?"
})

print(resp)
# bad_response = '{"action": "search"}'
# parser.parse(bad_response)

fix_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
# resp = fix_parser.parse(bad_response)
# print(resp)

# retry_parser = RetryOutputParser.from_llm(parser=parser, llm=llm)
# resp = retry_parser.parse_with_prompt(bad_response, prompt_value)
# print(resp)
#
# retry_error_parser = RetryWithErrorOutputParser.from_llm(llm, parser)
# resp = retry_error_parser.parse_with_prompt(bad_response, prompt_value)
# print(resp)
