import math
from collections import deque
from typing import Optional, List, Any

from pydantic.v1 import BaseModel

from autonomous.core.mcts.entity.evaluation_model import Evaluation


class Node(BaseModel):
    """
    蒙特卡洛树节点定义
    """
    parent: Optional['Node'] = None
    children: List['Node'] = []
    visits: int = 0
    value: float = 0.0
    task: Optional[str] = None
    task_response: Optional[str] = None
    evaluation: Optional[Evaluation] = None
    depth: int = 0
    is_resolved: bool = False

    def __init__(self, /, **data: Any) -> None:
        super().__init__(**data)
        self.depth: int = self.parent.depth + 1 if self.parent is not None else 1
        self.is_resolved = self.evaluation.found_solution if self.evaluation else False
        if self.is_resolved:
            self._mark_tree_as_resolved()

    @property
    def height(self) -> int:
        """Check for how far we've rolled out the tree."""
        if self.children:
            return 1 + max([child.height for child in self.children])
        return 1

    # @property
    # def is_resolved(self) -> bool:
    #     return self._is_resolved

    def _get_all_children(self) -> list['Node']:
        """广度遍历，获取该节点下所有孩子节点,返回list
        """
        all_children_nodes = []  #
        nodes = deque()  # 需要遍历的节点, 使用双向队列
        nodes.append(self)  # 从自身开始
        while nodes:
            node = nodes.popleft()  # 取第一个
            all_children_nodes.extend(node.children)
            for n in node.children:  # 下一级
                nodes.append(n)
        return all_children_nodes

    def get_best_child(self) -> Optional['Node']:
        """取当前节点最优的子节点
        """
        if not self.children:
            return None
        all_nodes = self._get_all_children()
        return max(all_nodes, key=lambda child: child.upper_confidence_bound())

    def upper_confidence_bound(self, exploration_weight: float = 0.3) -> float:
        """Upper Confidence bound applied to Trees(UCT) - 信任度上限树算法, 具体公式

        """
        if self.parent is None:
            raise ValueError("Cannot obtain UCT from root node")
        if self.visits == 0:
            return self.value
        # exploitation 部分, 即"获胜率", 使用该节点总奖励/总访问次数.
        average_reward = self.value / self.visits
        # exploration 部分, 即"探索性", 鼓励访问为探索的子结点
        exploration_term = math.sqrt(math.log(self.parent.visits) / self.visits)
        # print(f"average_reward={average_reward}, exploration_term={exploration_term}")
        return average_reward + exploration_weight * exploration_term

    def get_best_solution(self):
        if self.is_resolved:
            all_nodes = [self] + self._get_all_children()
            # TODO 有可能出现最后一步解决方案的分数不太高(需要适当提高当任务解决时该步骤的分数,或者调整下面的算法),导致高分在非叶子节点.
            best_node = max(all_nodes, key=lambda node: int(node.is_resolved) * node.value)
            return best_node
        else:
            return self.get_best_child()

    def _mark_tree_as_resolved(self):
        parent = self.parent
        while parent:
            parent.is_resolved = True
            parent = parent.parent

    def back_propagate(self):
        """反向传播, 设置本节点visits和value, 并将本节点得到回报反向传播给上级节点，一直到root"""
        reward: float = self.evaluation.normalized_score
        node = self
        while node:
            node.visits += 1
            node.value = (node.value * (node.visits - 1) + reward) / node.visits
            node = node.parent

    def get_messages(self, include_reflections: bool = True) -> dict:
        if include_reflections:
            return {
                "task": self.task,
                "task_response": self.task_response,
                "evaluation": self.evaluation.evaluation
            }

        return {
            "task": self.task,
            "task_response": self.task_response,
        }

    def get_trajectory(self, include_reflections: bool = True) -> list[dict]:
        """Get messages representing this search branch."""
        messages = []
        node = self
        while node:
            messages.append(
                node.get_messages(include_reflections=include_reflections)
            )
            node = node.parent
        # Reverse the final back-tracked trajectory to return in the correct order
        return messages[::-1]  # root solution, reflection, child 1, ...

    def update_task_response(self, new_task_response: str):
        """ update task_response """
        self.task_response = new_task_response
