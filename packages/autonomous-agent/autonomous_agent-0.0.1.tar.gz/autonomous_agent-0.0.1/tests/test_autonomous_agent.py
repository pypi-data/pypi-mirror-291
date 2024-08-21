from autonomous.core.mcts.autonomous_agent import AutonomousAgent
from tests.fake_tools import ask_human
from tests.test_config import pool

objectives = "帮我做一个小米公司官方宣传的视频的剧本, 内容包含小米公司的愿景, 公司大事记, 公司的产品. 你必须提供一个完整的剧本, 字数不少于1000字"
request_id = "100000000003"
tools = [ask_human]

autonomous_agent = AutonomousAgent(
    pool=pool,
    tools=tools
)

autonomous_agent.invoke(
    {
        "request_id": request_id,
        "objectives": objectives
    }
)
