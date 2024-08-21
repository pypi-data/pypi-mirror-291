from pydantic.v1 import BaseModel, Field


class Evaluation(BaseModel):
    evaluation: str = Field(title="evaluation", description="你的评估推理过程")
    score: int = Field(title="score", description="得出评估的总分")
    found_solution: bool = Field(title="found_solution", description="给定需要解决的问题是否完全解决?")

    @property
    def normalized_score(self) -> float:
        return self.score / 10.0
