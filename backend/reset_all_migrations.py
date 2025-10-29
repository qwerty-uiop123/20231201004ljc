import sqlite3
import os

# 连接到数据库
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("开始重置迁移记录...")
    
    # 删除所有应用的迁移记录
    cursor.execute("DELETE FROM django_migrations WHERE app IN ('users', 'admin', 'auth', 'contenttypes', 'sessions', 'posts', 'tiebas', 'chat');")
    print("已删除所有应用的迁移记录")
    
    # 提交更改
    conn.commit()
    
    # 验证删除
    cursor.execute("SELECT app, name FROM django_migrations;")
    remaining = cursor.fetchall()
    print(f"剩余的迁移记录: {remaining}")
    
    conn.close()
    print("所有迁移记录已重置，现在可以重新运行迁移")
else:
    print('数据库文件不存在')