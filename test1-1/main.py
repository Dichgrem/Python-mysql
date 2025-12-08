import sqlite3

# 1. 数据库连接和初始化
DB_NAME = "spj_database.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


def execute_query(sql, fetch_results=False, description=""):
    """执行 SQL 语句并打印结果或描述。"""
    print(f"\n--- {description} ---")
    try:
        cursor.execute(sql)
        conn.commit()
        if fetch_results:
            results = cursor.fetchall()
            print(f"SQL: {sql.strip()}")
            if cursor.description:
                # 打印列名
                column_names = [desc[0] for desc in cursor.description]
                print(f"Columns: {column_names}")
            # 打印查询结果
            if results:
                for row in results:
                    print(row)
            else:
                print("Query returned no results.")
        else:
            print(f"SQL: {sql.strip()}")
            print(f"Operation successful. Rows affected: {cursor.rowcount}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        print(f"Failed SQL: {sql.strip()}")


# 2. 建表操作
print("## 🚀 步骤 1: 建立 SPJ 数据库表")
create_tables_sql = """
-- 供应商表 S
CREATE TABLE IF NOT EXISTS S (
    SNO CHAR(2) PRIMARY KEY,
    SNAME CHAR(10),
    STATUS INT,
    CITY CHAR(10)
);

-- 零件表 P
CREATE TABLE IF NOT EXISTS P (
    PNO CHAR(2) PRIMARY KEY,
    PNAME CHAR(10),
    COLOR CHAR(4),
    WEIGHT INT
);

-- 工程项目表 J
CREATE TABLE IF NOT EXISTS J (
    JNO CHAR(2) PRIMARY KEY,
    JNAME CHAR(10),
    CITY CHAR(10)
);

-- 供应情况表 SPJ (注意：SQLite 不支持真正的外键约束，但在 SQL 语法上可以保留)
CREATE TABLE IF NOT EXISTS SPJ (
    SNO CHAR(2),
    PNO CHAR(2),
    JNO CHAR(2),
    QTY INT,
    PRIMARY KEY (SNO, PNO, JNO)
);
"""
cursor.executescript(create_tables_sql)
conn.commit()
print("所有表创建/检查完毕。")

# 3. 插入数据
print("\n## 🔢 步骤 2: 插入图 2.13 中的数据")
# S表数据
S_data = [
    ("S1", "精益", 20, "天津"),
    ("S2", "盛锡", 10, "北京"),
    ("S3", "东方红", 30, "北京"),
    ("S4", "丰泰盛", 20, "天津"),
    ("S5", "为民", 30, "上海"),
]
# P表数据
P_data = [
    ("P1", "螺母", "红", 12),
    ("P2", "螺钉", "绿", 17),
    ("P3", "螺丝刀", "蓝", 14),
    ("P4", "螺丝刀", "红", 14),
    ("P5", "凸轮", "蓝", 40),
    ("P6", "齿轮", "红", 30),
]
# J表数据
J_data = [
    ("J1", "三建", "北京"),
    ("J2", "一汽", "长春"),
    ("J3", "弹簧厂", "天津"),
    ("J4", "造船厂", "天津"),
    ("J5", "机床厂", "唐山"),
    ("J6", "无线电厂", "常州"),
    ("J7", "半导体厂", "南京"),
]
# SPJ表数据 (根据图 2.13 插入部分)
SPJ_data = [
    ("S1", "P1", "J1", 200),
    ("S1", "P1", "J3", 100),
    ("S1", "P1", "J4", 700),
    ("S1", "P2", "J2", 100),
    ("S2", "P3", "J1", 400),
    ("S2", "P3", "J2", 200),
    ("S2", "P3", "J4", 500),
    ("S2", "P3", "J5", 400),
    ("S2", "P5", "J1", 400),
    ("S2", "P5", "J2", 100),
    ("S3", "P1", "J1", 200),
    ("S3", "P3", "J1", 200),
    ("S4", "P5", "J1", 100),
    ("S4", "P6", "J3", 300),
    ("S4", "P6", "J4", 200),
    ("S5", "P2", "J4", 100),
    ("S5", "P3", "J1", 200),
    ("S5", "P6", "J2", 200),
    ("S5", "P6", "J4", 500),
]

# 批量插入数据
cursor.executemany("INSERT OR IGNORE INTO S VALUES (?,?,?,?)", S_data)
cursor.executemany("INSERT OR IGNORE INTO P VALUES (?,?,?,?)", P_data)
# cursor.executemany("INSERT OR IGNORE INTO J VALUES (?,?,?,?)", J_data)
cursor.executemany("INSERT OR IGNORE INTO J VALUES (?,?,?)", J_data)
cursor.executemany("INSERT OR IGNORE INTO SPJ VALUES (?,?,?,?)", SPJ_data)
conn.commit()
print("数据插入完毕。")

# 4. 执行 SQL 查询和操作 (对应原题的③ - ⑪)
print("\n## 🔍 步骤 3: 执行 SQL 查询和操作")
# --- 查询操作 (③-⑦) ---

# ③ 找出使用供应商 S1 所供零件的工程代码。
sql_3 = """
SELECT DISTINCT JNO
FROM SPJ
WHERE SNO = 'S1';
"""
execute_query(
    sql_3, fetch_results=True, description="③ 找出使用供应商 S1 所供零件的工程代码"
)

# ④ 找出工程项目 J2 使用的各种零件的名称及其数量。
sql_4 = """
SELECT T1.PNAME, T2.QTY
FROM P AS T1 JOIN SPJ AS T2 ON T1.PNO = T2.PNO
WHERE T2.JNO = 'J2';
"""
execute_query(
    sql_4,
    fetch_results=True,
    description="④ 找出工程项目 J2 使用的各种零件的名称及其数量",
)

# ⑤ 找出上海厂商供应的所有零件代码。
sql_5 = """
SELECT DISTINCT T1.PNO
FROM SPJ AS T1 JOIN S AS T2 ON T1.SNO = T2.SNO
WHERE T2.CITY = '上海';
"""
execute_query(sql_5, fetch_results=True, description="⑤ 找出上海厂商供应的所有零件代码")

# ⑥ 找出使用上海产的零件的工程名称。（理解为上海供应商供应的零件）
sql_6 = """
SELECT DISTINCT T3.JNAME
FROM S AS T1
JOIN SPJ AS T2 ON T1.SNO = T2.SNO
JOIN J AS T3 ON T2.JNO = T3.JNO
WHERE T1.CITY = '上海';
"""
execute_query(sql_6, fetch_results=True, description="⑥ 找出使用上海产的零件的工程名称")

# ⑦ 找出没有使用天津产的零件的工程代码。（理解为没有使用天津供应商供应的零件）
sql_7 = """
SELECT JNO
FROM J
WHERE JNO NOT IN (
    SELECT T1.JNO
    FROM SPJ AS T1 JOIN S AS T2 ON T1.SNO = T2.SNO
    WHERE T2.CITY = '天津'
);
"""
execute_query(
    sql_7, fetch_results=True, description="⑦ 找出没有使用天津产的零件的工程代码"
)

# --- 更新/删除/插入操作 (⑧-⑪) ---

# ⑧ 把全部红色零件的颜色改成蓝色。
sql_8 = """
UPDATE P
SET COLOR = '蓝'
WHERE COLOR = '红';
"""
execute_query(sql_8, description="⑧ 把全部红色零件的颜色改成蓝色")

# ⑨ 把由 S5 供给 J2 的零件 P6 改为由 S3 供应。（注意：此记录 S5, P6, J2 存在于数据中）
sql_9 = """
UPDATE SPJ
SET SNO = 'S3'
WHERE SNO = 'S5' AND PNO = 'P6' AND JNO = 'J2';
"""
execute_query(sql_9, description="⑨ 把由 S5 供给 J2 的零件 P6 改为由 S3 供应")

# ⑩ 从供应商关系 S 中删除供应商 S2 的记录，并从供应情况关系 SPJ 中删除相应的记录。
sql_10_spj = "DELETE FROM SPJ WHERE SNO = 'S2';"
execute_query(sql_10_spj, description="⑩.1 从 SPJ 中删除 S2 相关的记录")

sql_10_s = "DELETE FROM S WHERE SNO = 'S2';"
execute_query(sql_10_s, description="⑩.2 从 S 中删除 S2 的记录")

# ⑪ 请将 (S2, J6, P4, 200) 插入供应情况关系。（按 SPJ(SNO, PNO, JNO, QTY) 顺序调整为 (S2, P4, J6, 200)）
sql_11 = """
INSERT INTO SPJ (SNO, PNO, JNO, QTY)
VALUES ('S2', 'P4', 'J6', 200);
"""
execute_query(sql_11, description="⑪ 将 (S2, P4, J6, 200) 插入 SPJ 关系")

# 5. 清理和关闭
conn.close()
print("\n数据库连接已关闭。")
