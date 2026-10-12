import os
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("请设置环境变量 OPENAI_API_KEY")
BASE_URL = os.environ.get("OPENAI_BASE_URL")
if not BASE_URL:
    raise ValueError("请设置环境变量 OPENAI_BASE_URL")
URL = f"{BASE_URL}/chat/completions"
MAX_HISTORY = 20