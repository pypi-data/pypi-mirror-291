from langchain_core.messages import BaseMessage, ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from autonomous.core.mcts.prompts.interface.prompt_template_interface import BasePromptTemplateInterface

evaluation_current_task_system_prompt_template = """\
You will be provided a problem and an action couple with response\
Your task is to evaluate the action coupled with response quality to the problem. 

You MUST Strictly follow the evaluation criteria and evaluation steps provided below to evaluate the the action coupled with response.

evaluation criteria(addictive score: 0-5 score):

- Correctness: Award 1 point if the response is correct to action, otherwise give 0 point.
- Completeness: Award 1 point if the response is complete, otherwise give 0 point.
- Importance: Award 1 point if the response lead to given problem solved, otherwise give 0 point.
- Relevance: Award 1 point if the action coupled with response is relate to given problem. otherwise give 0 point.
- Detailed: Award 1 point if response is detailed, otherwise give 0 point.

evaluation steps:

1. Read given the problem,   an action couple with response carefully to ensure that you fully understand all those information.
2. According to each item of the evaluation criteria, independently award point to the provided action and response.
3. Calculate the total score by summing scores given above.
"""
evaluation_current_task_format_instruction_message = """\
When respond to me, you must use the following instruction.
```
{{
    "evaluation": string, \\ Your evaluation about current task and response.
    "score": int \\ Total addictive score, the value of score MUST be integer!
}}
```
"""
evaluation_current_task_human_prompt_template = """
Problem: 
```
{human_input_task}
```

Action:
```
{task}
```

Response:
```
{task_response}
```

Evaluate the action coupled with response and respond the completed evaluation feedback to me. 使用中文回复.

Remember: you MUST follow format instruction to respond to me, the response should be valid JSON Markdown snippet \
code, including evaluation, score fields. 

Evaluation feedback to the action coupled with response:
"""


class EvaluationCurrentPromptTemplate(BasePromptTemplateInterface):

    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", evaluation_current_task_system_prompt_template),
            ("system", evaluation_current_task_format_instruction_message),
            ("human", evaluation_current_task_human_prompt_template),
        ])


evaluation_solution_system_prompt_template = """
You will be provided a problem, requirements of this problem and a solution to the problem which consisting of multiple steps in sequence. \
Your task is to evaluate the solution quality to the problem. 

You MUST Strictly follow the evaluation criteria and evaluation steps provided below to evaluate the solution.

evaluation criteria(addictive score: 0-5 score):

- Solved: Award 1 point if the solution solves the given problem entirely, 0 points are given otherwise.
- Completeness: Award 1 point if the solution is comprehensive and requires no further action to be taken, otherwise give 0 point.
- Detailed: Award 1 point if the solution is detailed, otherwise give 0 point.
- Fulfillment: Award 1 point if the solution fully meets all the requirements of the given problem, otherwise give 0 point.
- Consistency: Award 1 points if the solution fully meets all the objectives of the given problem, otherwise give 0 point.

evaluation steps:

1. Read given the problem, requirements of the problem and solution to the problem carefully to ensure that you fully understand all those information.
2. According to each item of the evaluation criteria, independently award point to the provided solution.
3. Calculate the total score by summing scores given above.
4. Judge whether does the solution solve the given problem entirely, and fully satisfy all the requirements of the given problem?
"""

evaluation_solution_format_instruction_message = """
When respond to me, you must use the following instruction.

{format_instruction}
"""

evaluation_solution_human_input_prompt_template = """
Blow are given problem, requirements of the problem and solution to the problem which consisting of multiple steps in sequence.

Problem: 
```
{human_input_task}
```

Requirements of the problem: 
```
{requirements}
```
"""

evaluation_solution_human_instruction_prompt_template = """
Evaluate the solution and respond the completed evaluation feedback to me. 使用中文回复.

Remember: you MUST follow format instruction to respond to me, the response should be valid JSON Markdown snippet \
code, including evaluation, score, is_solved fields. 

Evaluation feedback to the solution:
"""


class EvaluationSolutionPromptTemplate(BasePromptTemplateInterface):
    def generate_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", evaluation_solution_system_prompt_template),
            ("system", evaluation_solution_format_instruction_message),
            ("human", evaluation_solution_human_input_prompt_template),
            MessagesPlaceholder("solution_steps", optional=True),
            ("human", evaluation_solution_human_instruction_prompt_template)
        ])


def format_solution_steps(messages: list[dict]) -> list[BaseMessage]:
    history_actions: list[BaseMessage] = []
    for message in messages:
        history_actions.append(
            ChatMessage(content=f"""\nAction: \n{message["task"]} \n\nResponse: \n{message["task_response"]}""",
                        role="Solution Step"))
    return history_actions
