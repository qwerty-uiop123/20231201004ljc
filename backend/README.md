# 百度贴吧 - 后端API服务

这是百度贴吧项目的Django后端API服务，提供用户认证、贴吧管理、帖子管理、消息系统等功能。

## 技术栈

- **框架**: Django 4.2.7 + Django REST Framework 3.14.0
- **认证**: JWT (JSON Web Token)
- **数据库**: SQLite (开发环境) / PostgreSQL (生产环境)
- **CORS**: django-cors-headers
- **文件存储**: Django内置文件存储

## 项目结构

```
backend/
├── tieba_backend/          # Django项目配置
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 主URL路由
│   └── wsgi.py             # WSGI配置
├── users/                  # 用户认证应用
├── tiebas/                 # 贴吧管理应用
├── posts/                  # 帖子管理应用
├── messages/               # 消息系统应用
├── manage.py               # Django管理脚本
├── requirements.txt        # Python依赖
└── .env.example            # 环境变量示例
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+和pip。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 环境配置

复制环境变量文件并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置你的配置：

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
python manage.py runserver
```

服务器将在 http://localhost:8000 启动。

## API接口文档

### 用户认证接口

- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户退出
- `GET /api/auth/profile/` - 获取用户资料
- `PUT /api/auth/profile/` - 更新用户资料
- `GET /api/auth/settings/` - 获取用户设置
- `PUT /api/auth/settings/` - 更新用户设置
- `POST /api/auth/password/change/` - 修改密码
- `POST /api/auth/follow/` - 关注用户
- `DELETE /api/auth/follow/` - 取消关注

### 贴吧接口

- `GET /api/tiebas/` - 获取贴吧列表
- `POST /api/tiebas/` - 创建贴吧
- `GET /api/tiebas/{id}/` - 获取贴吧详情
- `PUT /api/tiebas/{id}/` - 更新贴吧信息
- `POST /api/tiebas/{id}/join/` - 加入贴吧
- `POST /api/tiebas/{id}/leave/` - 退出贴吧

### 帖子接口

- `GET /api/posts/` - 获取帖子列表
- `POST /api/posts/` - 创建帖子
- `GET /api/posts/{id}/` - 获取帖子详情
- `PUT /api/posts/{id}/` - 更新帖子
- `DELETE /api/posts/{id}/` - 删除帖子
- `POST /api/posts/{id}/like/` - 点赞帖子
- `POST /api/posts/{id}/favorite/` - 收藏帖子

### 消息接口

- `GET /api/messages/conversations/` - 获取对话列表
- `POST /api/messages/conversations/` - 创建对话
- `GET /api/messages/conversations/{id}/` - 获取对话详情
- `GET /api/messages/conversations/{id}/messages/` - 获取消息列表
- `POST /api/messages/conversations/{id}/messages/` - 发送消息

## 数据库模型

### 用户系统
- `User` - 用户模型（扩展Django User）
- `UserSettings` - 用户设置
- `UserFollow` - 用户关注关系

### 贴吧系统
- `TiebaCategory` - 贴吧分类
- `Tieba` - 贴吧
- `TiebaMember` - 贴吧成员
- `TiebaFollow` - 贴吧关注
- `TiebaAnnouncement` - 贴吧公告
- `TiebaRule` - 贴吧规则

### 帖子系统
- `Post` - 帖子
- `PostImage` - 帖子图片
- `Reply` - 回复
- `ReplyImage` - 回复图片
- `PostLike` - 帖子点赞
- `ReplyLike` - 回复点赞
- `PostFavorite` - 帖子收藏
- `PostViewHistory` - 帖子浏览历史

### 消息系统
- `Conversation` - 对话
- `PrivateMessage` - 私信消息
- `MessageAttachment` - 消息附件
- `ConversationParticipant` - 对话参与者状态
- `SystemNotification` - 系统通知
- `UserBlock` - 用户屏蔽

## 开发指南

### 添加新的API接口

1. 在对应的应用中创建 `serializers.py` 定义序列化器
2. 在 `views.py` 中创建视图类
3. 在 `urls.py` 中配置路由
4. 运行测试确保接口正常工作

### 数据库迁移

当修改模型后，需要生成并应用迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 运行测试

```bash
python manage.py test
```

## 部署说明

### 生产环境配置

1. 设置 `DEBUG=False`
2. 配置生产数据库（如PostgreSQL）
3. 设置静态文件收集
4. 配置Web服务器（如Nginx + Gunicorn）

### 静态文件收集

```bash
python manage.py collectstatic
```

### 环境变量配置

生产环境需要配置以下环境变量：

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。