"""
蒙特卡洛树搜索
TreeState
"""
import pickle

from autonomous.core.mcts.autonomous_agent import AutonomousAgent
from autonomous.core.mcts.entity.node_model import Node
from tests.test_config import pool
from tests.fake_tools import ask_human
# objectives = """将客户提交的企业信息中的指定字段与从官方渠道获取的企业信息的指定字段进行比对, 必须回复给我最后的比对的结果, 而不是一个对比的流程. 指定的字段为: '企业名称','企业类型','企业注册国家或地区','企业注册地址','企业所属行业','企业的成立日期','企业有效期','企业法人','企业的营业执照号码','企业股东'."""
# objectives = """在数学上9.11与9.9哪个大?"""
# objectives = """帮我写一篇关于如何防止土地沙漠化的论文, 你必须给我一篇8000字的完整的论文!"""
# objectives = """ln(x) 与 e^x 的函数图像是关于什么对称的?"""
# objectives = """任何一个初等函数，是否都能找到它的反函数?"""
# objectives = """12个球一个天平，现知道只有一个和其它的重量不同，问怎样称才能用三次就找到那个重量不同的球?"""
# objectives = """从前有一位老钟表匠，为一个教堂装一只大钟。他年老眼花，把长短针装配错了，短针走的速度反而是长针的12倍。装配的时候是上午6点，他把短针指在“6 ”上，长针指在“12”上。老钟表匠装好就回家去了。人们看这钟一会儿7点，过了不一会儿就8点了，都很奇怪，立刻去找老钟表匠。等老钟表匠赶到，已经是下午7点多钟。他掏出怀表来一对，钟准确无误，疑心人们有意捉弄他，一生气就回去了。这钟还是8点、9点地跑，人们再去找钟表匠。老钟表匠第二天早晨8点多赶来用表一对，仍旧准确无误。请你想一想，老钟表匠第一次对表的时候是7点几分？第二次对表又是8点几分？"""
objectives = "帮我做一个小米公司官方宣传的视频的剧本, 内容包含小米公司的愿景, 公司大事记, 公司的产品. 你必须提供一个完整的剧本, 字数不少于1000字"
# objectives = "帮我做一篇关于中国和日本的文化和技术的对比，字数在1000字左右"
# objectives = f"帮我做一篇演员沈腾和演员马丽的人生历程，字数不少于5000字"
# objectives = f"帮我写一篇小米雷军的发展史，字数不少于5000字"
# objectives = f"帮我写一个武侠小说"


# fb = "主角是一个性格豪爽,行侠仗义的男性(类似仙剑奇侠转里面的李逍遥), 故事起点在余杭镇(是一个虚拟的地方). 整个故事都是虚拟的, 黑暗势力很大, 他们的战斗方式要奇幻类似仙剑奇侠传那种, 主要动机是找到自己失去的记忆和爱人. 我想表达的主题是‘爱与决心’"
# fb = "主角性格豪爽, 时代是虚拟的中国古代"
# fb = "我希望你写一个完整的小说,你可以分段写."
# fb = "我对小米的技术创新感兴趣, 我希望视频的风格是用户体验分享"
fb = "你自己编写就行, 不用问我"
request_id = "200000000003"
tools = [ask_human]
autonomous_agent = AutonomousAgent(
    pool=pool,
    tools=tools
)

response = autonomous_agent.invoke(
    {
        "request_id": request_id,
        "human_input": fb,
        "resume": True,
    }
)
# print(response)
root: Node = pickle.loads(response["root"])
if root.is_resolved:
    print(root.get_best_solution().get_trajectory())
else:
    ask_human = response["ask_human"]
    print(ask_human)
