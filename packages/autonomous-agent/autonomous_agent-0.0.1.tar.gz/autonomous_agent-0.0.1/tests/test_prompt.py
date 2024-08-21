from langchain_core.messages import BaseMessage, ChatMessage
from langchain_core.output_parsers import StrOutputParser

from autonomous.core.mcts.prompts.expand_prompts import sub_objective_prompt, knowledge_retrieve_prompt, next_action_prompt
from autonomous.core.mcts.prompts.human_input_process_prompt import extract_key_objectives_prompt, \
    extract_objective_requirements_prompt
from autonomous.core.mcts.service.human_input_process_service import create_extract_objective_requirements_service
from autonomous.infra.llm.llms import llm

chain1 = extract_key_objectives_prompt | llm | StrOutputParser()
chain2 = extract_objective_requirements_prompt | llm | StrOutputParser()
chain3 = create_extract_objective_requirements_service()
chain4 = sub_objective_prompt | llm | StrOutputParser()
chain5 = knowledge_retrieve_prompt | llm | StrOutputParser()
chain6 = next_action_prompt | llm | StrOutputParser()
# print(chain1.invoke({"objectives": "帮我做一个小米公司官方宣传的视频的剧本, 内容包含小米公司的愿景, 公司大事记, 公司的产品. 你必须提供一个完整的剧本,不能只包含一个剧本大纲, 字数不少于1000字"}))
# print(chain2.invoke({"objectives": "帮我做一个小米公司官方宣传的视频的剧本, 内容包含小米公司的愿景, 公司大事记, 公司的产品. 必须提供一个完整的剧本,不能只包含一个剧本大纲, 字数不少于3000字"}))
# print(chain2.invoke({"objectives": "12个球一个天平，现知道只有一个和其它的重量不同，问怎样称才能用三次就找到那个重量不同的球? 需要返回给我一个完整的解决办法!"}))
# print(chain3.invoke({"objectives": "帮我做一个小米公司官方宣传的视频的剧本, 内容包含小米公司的愿景, 公司大事记, 公司的产品. 必须提供一个完整的剧本,不能只包含一个剧本大纲, 字数不少于3000字"}))
actions = [
    {
        "action": "仔细阅读给定的问题, 分析出解决该问题的关键目标.",
        "response": "问题主要目标：撰写一个小米公司官方宣传视频的剧本，内容涵盖公司愿景、大事记和产品，要求剧本完整且详细，字数不少于3000字。"
    },

    {
        "action": "请编写一个简短的小米公司宣传视频脚本大纲，包括公司愿景、主要里程碑和产品亮点",
        "response": "大纲包括: 开头(200字)，公司愿景描述(600字), 主要里程碑和产品亮点(1000字) "
    },
    #
    # {
    #     "action": "搜索小米公司官方愿景的详细描述，以便在剧本中准确传达。",
    #     "response": "让每个人都能享受科技的乐趣和用户交朋友，做用户心中最酷的公司。"
    # },
    # {
    #     "action": "仔细阅读给定问题, 确保完全理解给定的问题的最终目标, 根据当前完成进度, 提出新的目标和要求.",
    #     "response": "根据小米公司的愿景、大事记和产品信息，撰写一个完整的宣传视频剧本，确保内容丰富、连贯，字数不少于3000字。剧本应包括引人入胜的开头，详细阐述公司愿景，接着列出关键里程碑，最后重点介绍小米的主要产品及其亮点。在编写过程中，要保持语言生动、富有感染力，以便吸引观众并传达小米的品牌价值。"
    # }
#     {
#         "action": "总结当前已经完成的工作, 按照给定问题, 推断要完成给定问题, 还需要收集哪些信息?",
#         "response": """
# 当前完成的工作:
# 1. 确定了剧本的结构和内容要求。
# 2. 提供了一个简短的剧本大纲，包括开头、公司愿景描述、主要里程碑和产品亮点。
#
# 为了完成一个完整的3000字的剧本，我们还需要收集以下信息:
# 1. 小米公司的详细愿景和使命陈述，确保准确传达公司的核心价值观。
# 2. 具体的公司大事记，包括重要日期、关键事件、里程碑产品发布等。
# 3. 小米主要产品的详细描述，包括产品名称、特点、创新之处以及它们如何改变市场或用户生活。
# 4. 小米公司文化、团队精神和用户反馈的实例，以增强故事的连贯性和情感共鸣。
# 5. 任何重要的市场数据、奖项或行业认可，以展示小米的影响力和成就。
# 6. 小米未来的发展计划或战略，以展示公司的前瞻性和成长潜力。
#
# 收集这些信息后，我们可以根据大纲逐步填充内容，确保剧本既全面又吸引人。
#         """
#     }
#     {
#         "action": "回顾小米公司的重要历史事件和里程碑。",
#         "response": """
# [画面切换至时间轴，展示小米公司的重要年份和事件。]
#
# 旁白（庄重而富有情感）：
# 2010年，小米科技在北京成立，带着“为发烧而生”的口号，小米的第一款智能手机小米1横空出世，以其高性价比震惊市场。
#
# [画面播放小米1发布会的片段，观众热烈的掌声和雷军的演讲。]
#
# 雷军（在发布会上）：
# 我们不追求利润，只希望让每个人都能用上好手机。
#
# [画面切换至小米2、3、4等历代手机的发布，展示小米在智能手机领域的快速迭代和创新。]
#
# 旁白（继续）：
# 小米2开启了小米的辉煌篇章，小米3的发布标志着小米正式进军中高端市场，小米4则以极致工艺赢得了全球赞誉。
#
# [画面过渡到小米电视、小米手环等生态链产品的发布，展示小米的多元化发展。]
#
# 旁白（激动）：
# 小米不仅仅是一家手机公司，我们打造的是一个智能生活生态系统，让科技触手可及。
#
# [画面展示小米在全球的足迹，包括进入印度、欧洲等市场，以及小米之家的开业。]
#
# 旁白（自豪）：
# 小米的足迹遍布全球，我们的产品走进了千家万户，小米，已经成为全球人民信赖的品牌。
#
# [画面回到现在，展示小米最新的产品和技术，如小米11系列、小米MIX Fold等。]
#
# 旁白（展望未来）：
# 小米，始终站在科技的前沿，不断探索，不断超越，为实现我们的愿景而努力。
#         """
#     }
]

history_template = """
Action: {action}
Observation: 
```
{response}
```
"""
def mee(actions: list)->list[BaseMessage]:
    messages: list[BaseMessage] = []
    for action in actions:
        messages.append(ChatMessage(content=f"\nAction: \n{action['action']}", role="Action Creator"))
        messages.append(ChatMessage(content=f"\nResponse: \n{action['response']}", role="Action Executor"))
    return messages


def mee2(actions: list)->str:
    st = "\n----\n".join([history_template.format(action=action['action'], response=action['response']) for action in actions])
    return st


resp = chain4.invoke({
    "objectives": "帮我做一个小米公司官方宣传的视频的剧本, 内容包含小米公司的愿景, 公司大事记, 公司的产品. 必须提供一个完整的剧本,不能只包含一个剧本大纲, 字数不少于3000字",
    # "history_actions": mee(actions)
    "history_actions": mee(actions=actions)
})


# print(resp.to_string())
print(resp)


# prompt2 = PromptTemplate.from_template("""
# 仔细阅读下列的行动集合, 对给出的下列的行动集合, 合并作用相同的行动, 修订出新的行动集合
# {actions}
#
# """)
#
# c = prompt2 | llm | StrOutputParser()
# resp = c.invoke({
#     "actions": ['\n开始撰写剧本，首先设定剧本标题和开场。', '\n制定剧本大纲，确定关键场景和信息点。', '\n确定剧本结构，包括开场、愿景阐述、大事记回顾、产品展示和结尾，确保内容丰富且连贯。', '\n确定剧本结构，包括开场、愿景阐述、大事记回顾、产品展示和结尾，每个部分都需要详细的内容和引人入胜的叙述。', '\n首先，为剧本设定一个基调，这将是鼓舞人心和创新的，以反映小米的品牌形象。然后，我会按照时间顺序安排大事记，从小米的创立开始，一直到最新的里程碑。在介绍产品时，我会突出每个产品的创新点和用户价值。为了保持剧本的连贯性，我会使用流畅的过渡语句。最后，剧本将以小米的愿景和对未来的展望结束。']
#
# })
#
# print(resp)