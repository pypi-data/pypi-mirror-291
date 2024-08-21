from langchain_openai import ChatOpenAI

from autonomous.infra.settings import settings

llm = ChatOpenAI(
    openai_api_base=settings.llm_url,
    # openai_api_base=f"https://dashscope.aliyuncs.com/compatible-mode/v1",
    # openai_api_base=f"http://192.168.1.201:18000/v1",
    # openai_api_key="sk-87ff28ecb3dd43aeae1096879b2c20f7",
    openai_api_key="EMPTY",
    # logprobs=True,
    # top_logprobs=1,
    model=settings.llm_model_name,
    # model="qwen-max",
    streaming=False,
    temperature=0.0,
    default_headers={"x-request-type": "Capability", "x-heliumos-capability": "llm general-inference"},
    max_tokens=settings.llm_tokens,
    # max_tokens=4096,
    verbose=False,
    # model_kwargs={"extra_body":{"guided-decoding-backend": "lm-format-enforcer"}},
    top_p=0.8
)

vlm = ChatOpenAI(
    openai_api_base=settings.vlm_url,
    # openai_api_base=f"http://192.168.1.201:9000/v1",
    # openai_api_base=f"https://dashscope.aliyuncs.com/compatible-mode/v1",
    # openai_api_base=f"http://192.168.1.201:9000/v1",
    # openai_api_key="sk-87ff28ecb3dd43aeae1096879b2c20f7",
    openai_api_key="EMPTY",
    # logprobs=True,
    # top_logprobs=1,
    model=settings.vlm_model_name,
    # model="qwen-max",
    temperature=0.0,
    default_headers={"x-request-type": "Capability", "x-heliumos-capability": "llm general-inference"},
    # max_tokens=settings.INFERENCE_MAX_TOKENS,
    max_tokens=settings.vlm_tokens,
    # verbose=True,
    top_p=0.8
)
