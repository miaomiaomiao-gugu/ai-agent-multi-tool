import requests


def get_ip_info():
    url = "https://ipinfo.io/json"
    try:
        response = requests.get(url,verify=False,timeout=10)
        data = response.json()
        ip = data['ip']
        country = data['country']
        city = data['city']
        loc = data['loc']
        return f"当前ip:{ip},当前国家:{country},当前城市:{city},当前坐标:{loc}"
    except Exception as e:
        return f"返回失败{e}"