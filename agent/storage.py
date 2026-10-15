import sqlite3
import os
import datetime
import json
DB_PATH = "data/agent.db"
# --------------------------


def init_db():  #建立初始表格
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    # ----------连接数据库---------
    conn = sqlite3.connect(DB_PATH)  #能直接定义/后的文件
    cursor = conn.cursor()
    # -----------------------------
    # ----------建表----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        created_at TEXT,
        updated_at TEXT
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        role TEXT,
        content TEXT,
        tool_calls TEXT,
        tool_call_id TEXT,
        created_at TEXT
        )        
    """)
    # --------------------------------
    # ----------结束保存----------------
    conn.commit()
    conn.close()
    # ----------------------------------


def create_session(title="新对话"):  #这个新对话是固定参数吗？
    # --------连接数据库-----------------
    conn = sqlite3.connect(DB_PATH)  # 能直接定义/后的文件
    cursor = conn.cursor()
    # ----------------------------
    # -------
    # -----------筛选数据-------------------
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO sessions(title,created_at,updated_at) VALUES(?,?,?)",
    (title,now_str,now_str))
    session_id = cursor.lastrowid
    # -------------------------------------
    # ---------结束保存----------------------
    conn.commit()
    conn.close()
    return session_id
    # -------------------------------------


def save_message(session_id,message):
    # ----------连接数据库-----------------
    conn = sqlite3.connect(DB_PATH)  # 能直接定义/后的文件
    cursor = conn.cursor()
    # ------------------------------------
    # ----------筛选数据--------------------
    role = message.get("role")
    content = message.get("content")
    if message.get("tool_calls"):
        tool_calls = json.dumps(message.get("tool_calls"))
    else:
        tool_calls = None
    tool_call_id = message.get("tool_call_id")
    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages(session_id,role,content,tool_calls,tool_call_id,created_at) VALUES(?,?,?,?,?,?)",
                   (session_id,role,content,tool_calls,tool_call_id,now_str))
    # -----------------------------------------
    # -----------结束保存------------------------
    conn.commit()
    conn.close()
    # ------------------------------------------


def load_messages(session_id):  # SQLITE数表据表的本质还是属于列表的形式
    # ---------连接数据库------------
    conn = sqlite3.connect(DB_PATH)  # 能直接定义/后的文件
    cursor = conn.cursor()
    # ------------------------------
    cursor.execute("SELECT * FROM messages WHERE session_id = ?",(session_id,))  #查询目标，参数
    rows = cursor.fetchall()  #取出所有会话id下的消息
    conn.close()  #当你不在需要对数据库进行下一步操作时可以通过调用conn.close()来进行关闭
    # -----------筛选列表-------------------
    result = []
    for row in rows:
        message = {"role":row[2]}  #为什么这里不需要做覆盖?
        if row[3] is not None:
            message["content"] = row[3]
        if row[4] is not None:
            message["tool_calls"] = json.loads(row[4])
        if row[5] is not None:
            message["tool_call_id"] = row[5]
        result.append(message)
    return result
   # -----------------------------------


def list_sessions():
    # -------连接数据库--------------
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # --------筛选列表---------------
    cursor.execute("SELECT id,title,created_at FROM sessions ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        session = {"id":row[0],"title":row[1],"created_at":row[2]}
        result.append(session)
    conn.close()
    return result
    # -----------------------

















