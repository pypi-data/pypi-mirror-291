from typing import Optional

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableParallel, RunnableConfig, RunnableLambda, RunnablePassthrough
from langchain_core.runnables.utils import Input, Output
from loguru import logger as log
from pydantic.v1 import BaseModel, Field

from autonomous.core.mcts.prompts.evaluation_prompts import format_solution_steps
from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface
from autonomous.infra.llm.llms import llm
from autonomous.infra.parsers import RepairableJsonOutputParser


class CurrentTaskEvaluationOutput(BaseModel):
    evaluation: str = Field(title="feedback", description="详细的评估反馈")
    score: int = Field(title="score", description="得出评估的总分")


class SolutionEvaluationOutput(BaseModel):
    evaluation: str = Field(title="evaluation", description="Your evaluation feedback about solution.")
    score: int = Field(title="score", description="Total addictive score, the value of this field MUST be integer!")
    is_solved: bool = Field(title="is_solved",
                            description="does the solution solve the given problem entirely, and fully satisfied all the requirements of the given problem? the value MUST be true or false.")


class EvaluationService(Runnable):

    @staticmethod
    def combined_parser(response: dict) -> dict:
        current_task_evaluation = response["current_task_evaluation"]
        solution_evaluation = response["solution_evaluation"]
        log.debug("current_task_evaluation: {}", current_task_evaluation)
        log.debug("solution_evaluation: {}", solution_evaluation)
        return {
            "evaluation": f"{current_task_evaluation['evaluation']}\n\n{solution_evaluation['evaluation']}",
            "score": current_task_evaluation["score"] + solution_evaluation["score"],
            "found_solution": solution_evaluation["is_solved"] and (
                    current_task_evaluation["score"] + solution_evaluation["score"] >= 10)
        }

    def __init__(
            self,
            evaluation_current_prompt: BasePromptTemplateInterface,
            evaluation_solution_prompt: BasePromptTemplateInterface
    ):
        _current_parser = RepairableJsonOutputParser(
            pydantic_object=CurrentTaskEvaluationOutput
        )
        _current_retry_error_parser = RetryWithErrorOutputParser.from_llm(
            llm,
            _current_parser,
            max_retries=3
        )
        _evaluation_current_task_prompt = evaluation_current_prompt.generate_prompt_template()
        _current_chain = _evaluation_current_task_prompt | llm | StrOutputParser()
        _current_evaluation_chain = RunnableParallel(
            completion=_current_chain,
            prompt_value=_evaluation_current_task_prompt
        ) | RunnableLambda(lambda x: _current_retry_error_parser.parse_with_prompt(**x))

        _solution_parser = RepairableJsonOutputParser(
            pydantic_object=SolutionEvaluationOutput
        )
        _solution_retry_error_parser = RetryWithErrorOutputParser.from_llm(
            llm,
            _solution_parser,
            max_retries=3
        )
        _evaluation_all_tasks_prompt = RunnablePassthrough.assign(
            format_instruction=lambda
                x: _solution_parser.get_format_instructions()) | evaluation_solution_prompt.generate_prompt_template()
        _solution_chain = _evaluation_all_tasks_prompt | llm | StrOutputParser()
        _solution_evaluation_chain = RunnableParallel(
            completion=_solution_chain,
            prompt_value=_evaluation_all_tasks_prompt
        ) | RunnableLambda(lambda x: _solution_retry_error_parser.parse_with_prompt(**x))
        self.evaluation_chain = RunnableParallel(
            current_task_evaluation=_current_evaluation_chain,
            solution_evaluation=_solution_evaluation_chain) | self.combined_parser

    def invoke(self, input: Input, config: Optional[RunnableConfig] = None) -> Output:
        human_input_task = input["human_input_task"]
        current_task = input["task"]
        current_task_response = input["task_response"]
        messages = input["messages"] if "messages" in input else []
        messages.append({
            "task": current_task,
            "task_response": current_task_response
        })
        requirements = input["requirements"]
        response = self.evaluation_chain.invoke({
            "human_input_task": human_input_task,
            "task": current_task,
            "task_response": current_task_response,
            "solution_steps": format_solution_steps(messages),
            "requirements": requirements
        })
        return response


def create_evaluation_service(
        evaluation_current_prompt: BasePromptTemplateInterface,
        evaluation_solution_prompt: BasePromptTemplateInterface
) -> Runnable:
    """对当前任务的评估:
    判断是否解决了问题，需要单独步骤， 合在一起非常不稳定. 采用parallel
    """
    return EvaluationService(
        evaluation_current_prompt=evaluation_current_prompt,
        evaluation_solution_prompt=evaluation_solution_prompt
    )
