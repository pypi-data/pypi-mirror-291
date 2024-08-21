from typing import Literal, Optional

from pydantic.v1 import BaseModel, Field


class Strategy(BaseModel):
    task: str = Field(title="task", description="需要执行的任务")
    task_status: Optional[Literal["completed", "interrupt"]] = Field(title="task_status", description="需要执行的任务")
    task_result: Optional[str] = Field(title="task_result", description="任务的最终结果")
    ask_human: Optional[str] = Field(title="ask_human", description="询问人类获取额外信息")
    human_feedback: Optional[str] = Field(title="human_feedback", description="人类反馈的信息")
