from tools.calculator import calculator
from tools.get_time import get_time
from tools.get_ip_info import get_ip_info
from tools.get_weather import get_weather


TOOL_FUNCTIONS = {
    "calculator":calculator,
    "get_time":get_time,
    "get_ip_info":get_ip_info,
    "get_weather":get_weather
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取当前日期以及时间",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "进行基础的数学运算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 23*45 或 (100+50)/3"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {"type":"function",
     "function":{
         "name":"get_ip_info",
         "description":"获取当前的地区、城市、ip",
         "parameters":{
             "type":"object",
             "properties":{},
             "required":[]
         }
     }}]