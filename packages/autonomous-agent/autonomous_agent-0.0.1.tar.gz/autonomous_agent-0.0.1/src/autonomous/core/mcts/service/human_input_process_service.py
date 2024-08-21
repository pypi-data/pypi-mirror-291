from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableParallel

from autonomous.core.mcts.prompts.human_input_process_prompt import extract_objective_prompt, extract_requirement_prompt, \
    extract_background_prompt, extract_domain_prompt
from autonomous.infra.llm.llms import llm


def create_extract_objective_requirements_service() -> Runnable:
    objective_chain = extract_objective_prompt | llm | StrOutputParser()
    requirement_chain = extract_requirement_prompt | llm | StrOutputParser()
    domain_chain = extract_domain_prompt | llm | StrOutputParser()
    background_chain = extract_background_prompt | llm | StrOutputParser()
    return RunnableParallel(
        objectives=objective_chain,
        requirements=requirement_chain,
        domains=domain_chain,
        backgrounds=background_chain
    )
