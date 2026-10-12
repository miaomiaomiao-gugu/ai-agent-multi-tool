def calculator(expression):
    # ----白名单检查避免eval恶意操作--------
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        return "表达式包含不允许的字符"
    # ------------------------------------
    try:
        result = eval(expression)
        return f"{expression}={result}"
    except Exception as e:
        return f"计算失败{e}"

