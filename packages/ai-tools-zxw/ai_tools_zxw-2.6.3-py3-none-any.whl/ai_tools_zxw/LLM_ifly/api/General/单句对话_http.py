# 导入SDK，发起请求
from openai import OpenAI
from ai_tools_zxw.LLM_ifly.api.config import api_key, api_secret, appid


# wss://xingcheng-api.cn-huabei-1.xf-yun.com/v1.1/chat
class GetLLMResponse:
    def __init__(self, model="generalv3.5", base_url="https://spark-api-open.xf-yun.com/v1"):
        self.model = model
        self.client = OpenAI(
            # 控制台获取key和secret拼接，假使APIKey是key123456，APISecret是secret123456
            api_key=f"{api_key}:{api_secret}",
            base_url=base_url  # 指向讯飞星火的请求地址
        )

    def get(self, input_content: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,  # 指定请求的版本
            messages=[
                {
                    "role": "user",
                    "content": input_content
                }
            ]
        )
        return completion.choices[0].message.content


if __name__ == '__main__':
    # General
    get_response = GetLLMResponse()
    a = get_response.get("请帮我写一份情书")
    print(a)

    # selfLLM - 无效
    # selfLLM = GetLLMResponse(model="xscnllama2")
    # b = selfLLM.get("你的基础模型是什么？")
    # print(b)
