import requests
import urllib3
import json
from config import API_KEY,URL
from tools import TOOLS
import logging
logger = logging.getLogger(__name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def chat_with_stream(messages):
    # 改成流式输出，主要是改变AI最终回答
    # -------------- 固定模版 --------------
    headers = {"Authorization": f"Bearer {API_KEY}",
               "Content-Type": "application/json"
               }  # 声明AI的接入密钥和AI的交流类型

    data = {"model": "deepseek-chat",
            "messages": messages,
            "stream": True}  # 声明AI调用那个模型，接入消息，需要调用的工具
    try:
        response = requests.post(URL, headers=headers, json=data, verify=False, timeout=60, stream=True)
        if response.status_code != 200:
            return {"error": f"HTTP{response.status_code}:{response.text}"}
    except Exception as e:
        return {"error": f"网络错误{e}"}
    full_reply = ""
    for line in response.iter_lines():
        if line:
            try:
                line_str = line.decode("utf-8").removeprefix("data: ")
                if line_str.strip() == "[DONE]":
                    break
                json_object = json.loads(line_str)
                chunk = json_object['choices'][0]['delta'].get('content')
                if chunk:
                    full_reply += chunk
                    print(chunk, end="", flush=True)
            except json.decoder.JSONDecodeError:
                logger.warning(f"JSON解析失败:{line_str[:100]}")
    print()
    return full_reply


def chat_with_tool(messages):
    # -------------- 固定模版 --------------
    headers = {"Authorization": f"Bearer {API_KEY}",
               "Content-Type": "application/json"
               }  # 声明AI的接入密钥和AI的交流类型

    data = {"model": "deepseek-chat",
            "messages": messages,
            "tools": TOOLS}  # 声明AI调用那个模型，接入消息，需要调用的工具
    try:
        response = requests.post(URL, headers=headers, json=data, verify=False, timeout=30)
        if response.status_code != 200:
            return {"error": f"HTTP{response.status_code}:{response.text}"}
        # 接入网址、验证通过证明，声明需要那种类型的AI以及AI需要完成的工作、绕过警告、超时检验
        return response.json()  # 转换成json格式
    except Exception as e:
        logger.error(f"chat_with_tool网络错误:{e}")
        return {"error": f"网络错误{e}"}
    # ----------------------------------------
