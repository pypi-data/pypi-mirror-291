from typing import Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.runnables.utils import Input, Output

from autonomous.core.mcts.prompts.human_feedback_prompts import feedback_extract_prompt
from autonomous.infra.llm.llms import llm


class HumanFeedbackExtractService(Runnable):
    def __init__(self):
        self.feedback_extract_chain = feedback_extract_prompt | llm | StrOutputParser()

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        task = input["task"]
        feedback = input["feedback"]
        if task["task_status"] == "completed":
            return task

        ask_human_question = task["ask_human"]
        response = self.feedback_extract_chain.invoke({
            "question": ask_human_question,
            "human_feedback": feedback
        })
        return {
            "task": task["task"],
            "task_status": task["task_status"],
            "task_result": task["task_result"],
            "ask_human": task["ask_human"],
            "human_feedback": response
        }


def create_feedback_extract_service():
    return HumanFeedbackExtractService()
