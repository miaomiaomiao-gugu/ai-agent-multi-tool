from config import MAX_HISTORY


def trim_history(messages):
    if len(messages) <= MAX_HISTORY:
        return messages
    return [messages[0]] + messages[-(MAX_HISTORY - 1):]  # 逆序查寻


