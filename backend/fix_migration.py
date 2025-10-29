import sqlite3
import os

# 连接到数据库
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 删除users应用的迁移记录
    cursor.execute("DELETE FROM django_migrations WHERE app='users';")
    print("已删除users应用的迁移记录")
    
    # 提交更改
    conn.commit()
    
    # 验证删除
    cursor.execute("SELECT app, name FROM django_migrations WHERE app='users';")
    remaining = cursor.fetchall()
    print(f"剩余的users迁移记录: {remaining}")
    
    conn.close()
    print("迁移记录已重置，现在可以重新运行迁移")
else:
    print('数据库文件不存在')