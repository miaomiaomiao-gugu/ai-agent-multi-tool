import requests


def get_weather(city):
    url = f"http://wttr.in/{city}"
    params = {"format":"j1"}
    try:
        response = requests.get(url,params=params,verify=False,timeout=10)
        data = response.json()
        current = data["current_condition"][0]
        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        return (f"{city}当前天气:{desc},"
                f"气温{temp}°C,湿度{humidity}%")
    except Exception as e:
        return f"天气查询失败:{e}"