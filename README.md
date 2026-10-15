AI Agent 助手:
一个基于 DeepSeek API 的多工具 AI 助手，支持函数调用、流式输出、日志记录。
------------------------
功能:
查询当前时间
简易的数学计算
查询城市天气
查询自己的IP以及地理位置
支持一次调用多个工具
多会话管理
数据持久化
流式输出（打字机效果）
对话历史管理
日志记录
--------------------
技术栈:
Python 3
requests（HTTP 请求）
DeepSeek API（兼容 OpenAI 格式）
Function Calling
SQL
-----------------------
项目结构:
├── main.py # 入口
├── config.py # 配置
├── agent/
│ ├── core.py # Agent 主循环
│ ├── llm.py # API 调用
│ └── history.py # 历史管理
└── tools/
├── init.py # 工具注册
├── calculator.py
├── get_time.py
├── get_weather.py
└── get_ip_info.py
-------------------------
如何运行:
1.设置环境变量：
   OPENAI_API_KEY：你的 API Key
   OPENAI_BASE_URL:https://api.deepseek.com
2.安装依赖：
   bash
   pip install requests urllib3
-----------------------------
补充:期望可以以此作为基础模板来加入更多功能来实现有实际作用的任务
