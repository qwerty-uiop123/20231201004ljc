from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型"""
    
    # 基本信息
    nickname = models.CharField(max_length=50, verbose_name='昵称')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    level = models.IntegerField(default=1, verbose_name='等级')
    experience = models.IntegerField(default=0, verbose_name='经验值')
    
    # 用户统计
    post_count = models.IntegerField(default=0, verbose_name='发帖数')
    reply_count = models.IntegerField(default=0, verbose_name='回帖数')
    follow_count = models.IntegerField(default=0, verbose_name='关注数')
    follower_count = models.IntegerField(default=0, verbose_name='粉丝数')
    
    # 用户设置
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    website = models.URLField(blank=True, verbose_name='个人网站')
    
    # 社交信息
    weibo = models.CharField(max_length=100, blank=True, verbose_name='微博')
    qq = models.CharField(max_length=20, blank=True, verbose_name='QQ号')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nickname or self.username

class UserFollow(models.Model):
    """用户关注关系"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='关注者')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='被关注者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')
    
    class Meta:
        verbose_name = '用户关注'
        verbose_name_plural = '用户关注'
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower} 关注 {self.following}"

class UserSettings(models.Model):
    """用户设置"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings', verbose_name='用户')
    
    # 通知设置
    email_notifications = models.BooleanField(default=True, verbose_name='邮件通知')
    push_notifications = models.BooleanField(default=True, verbose_name='推送通知')
    private_message_notifications = models.BooleanField(default=True, verbose_name='私信通知')
    
    # 隐私设置
    show_online_status = models.BooleanField(default=True, verbose_name='显示在线状态')
    show_post_count = models.BooleanField(default=True, verbose_name='显示发帖数')
    allow_private_messages = models.BooleanField(default=True, verbose_name='允许私信')
    
    # 主题设置
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', '浅色'),
        ('dark', '深色'),
        ('auto', '自动')
    ], verbose_name='主题')
    
    # 语言设置
    language = models.CharField(max_length=10, default='zh-hans', choices=[
        ('zh-hans', '简体中文'),
        ('zh-hant', '繁体中文'),
        ('en', 'English')
    ], verbose_name='语言')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户设置'
        verbose_name_plural = '用户设置'
    
    def __str__(self):
        return f"{self.user} 的设置"