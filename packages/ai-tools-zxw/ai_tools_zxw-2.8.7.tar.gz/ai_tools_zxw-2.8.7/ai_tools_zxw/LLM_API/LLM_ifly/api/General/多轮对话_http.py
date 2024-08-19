# 导入SDK，发起请求
from typing import List
from openai import OpenAI
from ai_tools_zxw.LLM_API import LLM
from ai_tools_zxw.LLM_API.config import ifly_api_key, ifly_secret_key


# wss://xingcheng-api.cn-huabei-1.xf-yun.com/v1.1/chat
class GetLLMResponse(LLM):
    chat_history = [
        # {"role": "system", "content": "你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"} , # 设置对话背景或者模型角色
        # {"role": "user", "content": "你是谁"},  # 用户的历史问题
        # {"role": "assistant", "content": "....."} , # AI的历史回答结果
        # # ....... 省略的历史对话
        # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
    ]

    def __init__(self, model="generalv3.5", base_url="https://spark-api-open.xf-yun.com/v1"):
        self.model = model
        self.client = OpenAI(
            # 控制台获取key和secret拼接，假使APIKey是key123456，APISecret是secret123456
            api_key=f"{ifly_api_key}:{ifly_secret_key}",
            base_url=base_url  # 指向讯飞星火的请求地址
        )

    def __del__(self):
        self.client.close()

    def chat(self, input_content: str, single_chat=False) -> str:
        # 1. 设置聊天记录
        chat_history = self._check_length(self._set_text("user", input_content))
        if single_chat is True:
            chat_history = chat_history[-1:]
            print("采用单次对话模式: ", len(chat_history))

        # 2. 发起请求
        completion = self.client.chat.completions.create(
            model=self.model,  # 指定请求的版本
            messages=chat_history
        )
        res = self._set_text("assistant", completion.choices[0].message.content)
        return res[-1]["content"]

    def 添加上下文(self, role, content):
        """
        :param role: system, user, assistant
        :param content:
        :return:
        """
        self._set_text(role, content)

    def 清除所有上下文(self):
        self.chat_history = []

    def _set_text(self, role, content) -> List[dict]:
        json_con = {"role": role, "content": content}
        self.chat_history.append(json_con)
        return self.chat_history

    def _check_length(self, text):
        while self.__get_length(text) > 8000:
            del text[0]
        return text

    @staticmethod
    def __get_length(text: List[dict]):
        length = 0
        for content in text:
            temp = content["content"]
            leng = len(temp)
            length += leng
        return length


if __name__ == '__main__':
    # General
    get_response = GetLLMResponse()
    a = get_response.chat("请帮我写一份情书")
    print(a)

    # selfLLM - 无效
    # selfLLM = GetLLMResponse(model="xscnllama2")
    # b = selfLLM.get("你的基础模型是什么？")
    # print(b)
