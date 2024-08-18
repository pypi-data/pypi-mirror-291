"""
# File       : chat.py
# Time       ：2024/8/18 下午4:15
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
import os
import qianfan
from ai_tools_zxw.LLM_API.config import baidu_access_key, baidu_secret_key

# 通过环境变量初始化认证信息
# 【推荐】使用安全认证AK/SK鉴权
# 替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_ACCESS_KEY"] = baidu_access_key
os.environ["QIANFAN_SECRET_KEY"] = baidu_secret_key

chat_comp = qianfan.ChatCompletion()

# 多轮对话
resp = chat_comp.do(model="ERNIE-4.0-8K-Latest", messages=[{
    "role": "user",
    "content": "你好"
},
    {
        "role": "assistant",
        "content": "你好，请问有什么我可以帮助你的吗？无论你需要什么帮助，我都会尽力回答你的问题或提供帮助。"
    },
    {
        "role": "user",
        "content": "北京有哪些美食"
    },
])
print(resp["body"])
