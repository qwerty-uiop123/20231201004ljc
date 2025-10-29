import sqlite3
import os

# 连接到数据库
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 获取所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print('数据库中的表:')
    for table in tables:
        print(f'  - {table[0]}')
    
    # 检查是否有users_user表
    user_tables = [table[0] for table in tables if 'user' in table[0].lower()]
    print(f'\n包含user的表: {user_tables}')
    
    # 检查django_migrations表
    if 'django_migrations' in [table[0] for table in tables]:
        cursor.execute("SELECT app, name FROM django_migrations WHERE app='users';")
        user_migrations = cursor.fetchall()
        print(f'\nusers应用的迁移记录: {user_migrations}')
    
    conn.close()
else:
    print('数据库文件不存在')