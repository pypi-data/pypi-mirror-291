from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from autonomous.infra.llm.llms import llm

prompt = PromptTemplate.from_template("""解答我给你的问题, 将原问题和答案回复给我.
Question: {question}
""")


chain = prompt | llm | StrOutputParser()

inputs = [{
    "question": "1+8 是多少?"
}, {
    "question": "中国的首都是哪儿?"
}, {
    "question": "112 * 22 是多少?"
}, {
    "question": "112 / 0 是多少?"
}, {
    "question": "任何一个初等函数，是否都能找到它的反函数?"
}]
for _ in range(20):
    resp = chain.batch(inputs=inputs)
    print(resp)
