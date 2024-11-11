import sqlite3

# 1. 連接到 SQLite 資料庫（如果資料庫不存在，會自動創建）
conn = sqlite3.connect("testdb.sqlite")
cursor = conn.cursor()

# 2. 讀取並執行 SQL 文件
with open("testdb.sql", "r", encoding="utf-8") as sql_file:
    sql_script = sql_file.read()

# 3. 執行 SQL 語句
cursor.executescript(sql_script)

# 4. 提交更改並關閉連接
conn.commit()
conn.close()

print("SQLite 資料庫已成功創建並填充數據！")
