from django.db import models
from django.contrib.auth import get_user_model
from tiebas.models import Tieba

User = get_user_model()

class Post(models.Model):
    """帖子模型"""
    
    POST_TYPES = [
        ('normal', '普通帖'),
        ('question', '提问帖'),
        ('discussion', '讨论帖'),
        ('share', '分享帖'),
        ('announcement', '公告帖'),
    ]
    
    POST_STATUS = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('pending', '待审核'),
        ('rejected', '已拒绝'),
        ('deleted', '已删除'),
    ]
    
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='帖子标题')
    content = models.TextField(verbose_name='帖子内容')
    type = models.CharField(max_length=20, choices=POST_TYPES, default='normal', verbose_name='帖子类型')
    status = models.CharField(max_length=20, choices=POST_STATUS, default='published', verbose_name='帖子状态')
    
    # 关联信息
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='posts', verbose_name='所属贴吧')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='作者')
    
    # 统计信息
    view_count = models.IntegerField(default=0, verbose_name='浏览数')
    reply_count = models.IntegerField(default=0, verbose_name='回复数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    favorite_count = models.IntegerField(default=0, verbose_name='收藏数')
    
    # 帖子设置
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    is_essence = models.BooleanField(default=False, verbose_name='是否精华')
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名')
    allow_reply = models.BooleanField(default=True, verbose_name='允许回复')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    
    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = '帖子'
        ordering = ['-is_pinned', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['tieba', 'status', 'created_at']),
            models.Index(fields=['author', 'status', 'created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = models.DateTimeField(auto_now_add=True)
        super().save(*args, **kwargs)

class PostImage(models.Model):
    """帖子图片"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='帖子')
    image = models.ImageField(upload_to='post_images/', verbose_name='图片')
    caption = models.CharField(max_length=200, blank=True, verbose_name='图片说明')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '帖子图片'
        verbose_name_plural = '帖子图片'
        ordering = ['sort_order', 'created_at']
    
    def __str__(self):
        return f"{self.post.title} - 图片"

class Reply(models.Model):
    """回复模型"""
    
    REPLY_STATUS = [
        ('published', '已发布'),
        ('pending', '待审核'),
        ('deleted', '已删除'),
    ]
    
    # 基本信息
    content = models.TextField(verbose_name='回复内容')
    status = models.CharField(max_length=20, choices=REPLY_STATUS, default='published', verbose_name='回复状态')
    
    # 关联信息
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies', verbose_name='帖子')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', verbose_name='作者')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='父回复')
    
    # 楼层信息
    floor = models.IntegerField(default=0, verbose_name='楼层')
    
    # 统计信息
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    
    # 回复设置
    is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '回复'
        verbose_name_plural = '回复'
        ordering = ['floor', 'created_at']
        indexes = [
            models.Index(fields=['post', 'status', 'created_at']),
            models.Index(fields=['author', 'status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.post.title} - 回复{self.floor}"
    
    def save(self, *args, **kwargs):
        if not self.floor:
            # 自动计算楼层
            last_reply = Reply.objects.filter(post=self.post).order_by('-floor').first()
            self.floor = last_reply.floor + 1 if last_reply else 1
        super().save(*args, **kwargs)

class ReplyImage(models.Model):
    """回复图片"""
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='images', verbose_name='回复')
    image = models.ImageField(upload_to='reply_images/', verbose_name='图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '回复图片'
        verbose_name_plural = '回复图片'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.reply.post.title} - 回复图片"

class PostLike(models.Model):
    """帖子点赞"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='帖子')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    class Meta:
        verbose_name = '帖子点赞'
        verbose_name_plural = '帖子点赞'
        unique_together = ('post', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} 点赞 {self.post}"

class ReplyLike(models.Model):
    """回复点赞"""
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='likes', verbose_name='回复')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_likes', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    class Meta:
        verbose_name = '回复点赞'
        verbose_name_plural = '回复点赞'
        unique_together = ('reply', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} 点赞 {self.reply}"

class PostFavorite(models.Model):
    """帖子收藏"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites', verbose_name='帖子')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_favorites', verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        verbose_name = '帖子收藏'
        verbose_name_plural = '帖子收藏'
        unique_together = ('post', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} 收藏 {self.post}"

class PostViewHistory(models.Model):
    """帖子浏览历史"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='view_history', verbose_name='帖子')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_view_history', verbose_name='用户')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    
    class Meta:
        verbose_name = '帖子浏览历史'
        verbose_name_plural = '帖子浏览历史'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} 浏览 {self.post}"