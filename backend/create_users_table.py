import sqlite3
import os

# 连接到数据库
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("开始创建users_user表...")
    
    # 创建users_user表的SQL语句
    create_table_sql = """
    CREATE TABLE "users_user" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "password" varchar(128) NOT NULL,
        "last_login" datetime NULL,
        "is_superuser" bool NOT NULL,
        "username" varchar(150) NOT NULL UNIQUE,
        "first_name" varchar(150) NOT NULL,
        "last_name" varchar(150) NOT NULL,
        "email" varchar(254) NOT NULL,
        "is_staff" bool NOT NULL,
        "is_active" bool NOT NULL,
        "date_joined" datetime NOT NULL,
        "nickname" varchar(50) NOT NULL,
        "avatar" varchar(100) NULL,
        "level" integer NOT NULL,
        "experience" integer NOT NULL,
        "post_count" integer NOT NULL,
        "reply_count" integer NOT NULL,
        "follow_count" integer NOT NULL,
        "follower_count" integer NOT NULL,
        "bio" text NOT NULL,
        "location" varchar(100) NOT NULL,
        "website" varchar(200) NOT NULL,
        "weibo" varchar(100) NOT NULL,
        "qq" varchar(20) NOT NULL,
        "created_at" datetime NOT NULL,
        "updated_at" datetime NOT NULL
    )
    """
    
    try:
        cursor.execute(create_table_sql)
        print("users_user表创建成功")
        
        # 创建关联表
        cursor.execute("""
        CREATE TABLE "users_user_groups" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED
        )
        """)
        print("users_user_groups表创建成功")
        
        cursor.execute("""
        CREATE TABLE "users_user_user_permissions" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "user_id" bigint NOT NULL REFERENCES "users_user" ("id") DEFERRABLE INITIALLY DEFERRED,
            "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED
        )
        """)
        print("users_user_user_permissions表创建成功")
        
        # 提交更改
        conn.commit()
        print("所有表创建成功，更改已提交")
        
    except Exception as e:
        print(f"创建表时出错: {e}")
        conn.rollback()
    
    conn.close()
else:
    print('数据库文件不存在')