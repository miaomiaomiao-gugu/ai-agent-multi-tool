import json
from agent.history import trim_history
from agent.llm import chat_with_tool,chat_with_stream
from tools import TOOL_FUNCTIONS
import logging
from agent.storage import init_db,create_session, save_message,list_sessions,load_messages
logger = logging.getLogger(__name__)


def run_agent():
    init_db()  #接入数据库建表
    sessions = list_sessions()
    print(sessions)
    if sessions:
        session_id = sessions[0]["id"]  #加载最近的会话
        messages = load_messages(session_id)  #接收到返回对话的内容
        print(f"已加载历史对话{session_id}")
    else:
        session_id = create_session("新对话")
        messages = []
        print(f"已创建新会话{session_id}")
    system_msg = {"role":"system","content":"你是一个中文助手。你可以：查时间、做数学运算、查天气,查当前国家、城市、ip,遇到需要这些信息的问题，主动调用对应工具。"}
    if not messages or messages[0]["role"] != "system":  #补齐初始会话的消息
        messages.insert(0,system_msg)
    print("\n1.输入问题(正常AI对话、计算、查时间、天气、当前国家的ip、城市)\n2.exit：退出程序\n3.clear：清除历史记录\n4.history：显示当前的消息数量"
          "\n5.session:显示会话数量\n6.new:创建新对话\n7.load <id> 加载已有对话")
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
        elif use_input == "session":
            all_sessions = list_sessions()
            if not all_sessions:
                print("暂无会话记录")
            else:
                print(f"总共{len(all_sessions)}条会话记录")
                for s in all_sessions:
                    print(f"id:{s['id']},title:{s['title']},time:{s['created_at']}")
            continue
        elif use_input == "new":
            created_new_session = input("请输入新对话名称:").strip()
            session_id = create_session(created_new_session)
            messages = [{"role":"system","content":"你是一个中文助手。你可以：查时间、做数学运算、查天气,查当前国家、城市、ip,遇到需要这些信息的问题，主动调用对应工具。"}]
            # 上述这条（messages）相当于直接覆盖了
            print(f"已新建会话{session_id}:{created_new_session}")
            continue
        elif use_input.split() and use_input.split()[0] == "load":
           # use_input_load = input("请输入你要加载的对话(例如:load x):").strip()
           parts = use_input.split()
           if len(parts) != 2:
              print("用法:load <id>,例如 load 3")
              continue
           try:
                new_id = int(parts[1])
           except ValueError:
              print("id 必须是数字！")
              continue
           ids = [s["id"]for s in list_sessions()]
           if new_id not in ids:
              print(f"未找到会话{new_id}")
              continue
           session_id = new_id
           messages = load_messages(session_id)
           system_msg = {"role": "system", "content": "你是一个中文助手。你可以：查时间、做数学运算、查天气,查当前国家、城市、ip,遇到需要这些信息的问题，主动调用对应工具。"}
           if not messages or messages[0]["role"] != "system":
              messages.insert(0, system_msg)
           print(f"已加载会话 #{session_id}，共 {len(messages)} 条消息")
           continue
        user_msg = {"role": "user", "content": use_input}
        messages.append(user_msg)
        save_message(session_id,user_msg)
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
            save_message(session_id,message)
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
                tool_msg = {"role": "tool", "tool_call_id": tool_call["id"], "content": str(tool_result)}
                messages.append(tool_msg)
                save_message(session_id,tool_msg)
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
        assistant_msg = {"role": "assistant", "content": reply}
        messages.append(assistant_msg)  #执行结束回到外部大循环
        save_message(session_id,assistant_msg)
        # ---------- ---------------------------------