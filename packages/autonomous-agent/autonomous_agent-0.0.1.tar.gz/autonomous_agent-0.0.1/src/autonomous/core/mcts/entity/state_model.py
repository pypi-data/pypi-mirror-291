from typing import TypedDict, List

from autonomous.core.mcts.entity.evaluation_model import Evaluation
from autonomous.core.mcts.entity.strategy_model import Strategy


class State(TypedDict):
    root: bytes  # 蒙特卡洛树根节点
    best_candidate: bytes  # 当前最优候选节点, 所有节点都已经展开(因为每次扩展后都会进行全部模拟和评估)
    human_input_task: str  # 需要解决的问题或者需要执行的任务.
    objectives: str  # 从用户的任务提取的目标
    objective_requirements: str  # 从用户的任务提取的关键需求
    strategies: List[Strategy]  # 当前最优节点，后续的随机策略(可以设置为3个)
    evaluations: List[Evaluation]  # 对该节点所有策略和执行结果分别进行评估的评估结果
    resolved: bool  # 目标问题是否解决
    ask_human: str  # 需人工提供信息
    human_feedback: str  # 人类反馈的信息
