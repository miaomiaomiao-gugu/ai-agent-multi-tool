import json
from agent.history import trim_history
from agent.llm import chat_with_tool,chat_with_stream
from tools import TOOL_FUNCTIONS
import logging
logger = logging.getLogger(__name__)


def run_agent():
    messages = [{"role": "system", "content": "你是一个中文助手。你可以：查时间、做数学运算、查天气,查当前国家、城市、ip,遇到需要这些信息的问题，主动调用对应工具。"}]
    print("\n1.输入问题(正常AI对话、计算、查时间、天气、当前国家的ip、城市)\n2.exit：退出程序\n3.clear：清除历史记录\n4.history：显示当前的消息数量")
    while True:
        use_input = input("\n你:").strip()
        logger.info(f"用户输入:{use_input}")
        if use_input == "exit":
            logger.info(f"用户退出程序")
            print("退出成功")
            break
        elif use_input == "clear":
            logger.info(f"用户清除记录")
            messages = [messages[0]]
            print("历史记录已清除")
            continue  # 程序继续往下走
        elif use_input == "history":
            print(f"当前的消息数量为:{len(messages)}")
            continue
        messages.append({"role": "user", "content": use_input})

        # -------- 检查调用是否成功-----------
        messages = trim_history(messages)
        result = chat_with_tool(messages)  # 第一次请求AI响应
        if "error" in result:
            logger.error(f"API错误: {result['error']}")
            print(f"{result['error']}")
            break
        message = result["choices"][0]["message"]  # 主要信息提取
        while message.get("tool_calls"):
            messages.append(message)
            if message.get("content") is None:
                message["content"] = ""
            for tool_call in message["tool_calls"]:  # 筛选信息
                function_name = tool_call['function']['name']
                arguments = json.loads(tool_call["function"]["arguments"])
                print(f"调用成功:{function_name}")
                logger.info(f"AI已调用工具:{function_name},{arguments}")
            # --------------------------------------

            # ----------执行工具----------------------
                if function_name in TOOL_FUNCTIONS:
                    try:
                        tool_result = TOOL_FUNCTIONS[function_name](**arguments)
                    except Exception as e:
                        tool_result = f"错误{e}"
                else:
                    tool_result = "未知函数"
                print(f"工具返回:{tool_result}")
                logger.info(f"工具返回:{tool_result}")
                messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": str(tool_result)})
            result = chat_with_tool(messages)  #第二次请求ai响应，让ai检查是否有工具来判断是否继续执行while循环
            if "error" in result:
                logger.error(f"API错误: {result['error']}")
                print(f"{result['error']}")
                break
            message = result["choices"][0]["message"]
            #  --------------------------------------

        #  -------------组织回答-------------------
        messages = trim_history(messages)
        print("AI:",end="",flush=True)
        reply = chat_with_stream(messages)  #第三次请求流式ai响应输出结果
        if isinstance(reply, dict) and "error" in reply:
            logger.error(f"API错误: {reply['error']}")
            print(f"{reply['error']}")
            break
        logger.info(f"已记录AI回答{reply}")
        messages.append({"role": "assistant", "content": reply})  #执行结束回到外部大循环
        # -------------------------------------------