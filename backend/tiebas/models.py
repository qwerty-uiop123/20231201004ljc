from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TiebaCategory(models.Model):
    """贴吧分类"""
    name = models.CharField(max_length=50, verbose_name='分类名称')
    description = models.TextField(max_length=200, blank=True, verbose_name='分类描述')
    icon = models.CharField(max_length=100, blank=True, verbose_name='分类图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '贴吧分类'
        verbose_name_plural = '贴吧分类'
        ordering = ['sort_order', 'created_at']
    
    def __str__(self):
        return self.name

class Tieba(models.Model):
    """贴吧模型"""
    
    # 基本信息
    name = models.CharField(max_length=50, unique=True, verbose_name='贴吧名称')
    title = models.CharField(max_length=100, verbose_name='贴吧标题')
    description = models.TextField(max_length=500, blank=True, verbose_name='贴吧描述')
    avatar = models.ImageField(upload_to='tieba_avatars/', null=True, blank=True, verbose_name='贴吧头像')
    banner = models.ImageField(upload_to='tieba_banners/', null=True, blank=True, verbose_name='贴吧横幅')
    
    # 分类信息
    category = models.ForeignKey(TiebaCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='分类')
    
    # 统计信息
    member_count = models.IntegerField(default=0, verbose_name='成员数')
    post_count = models.IntegerField(default=0, verbose_name='帖子数')
    today_post_count = models.IntegerField(default=0, verbose_name='今日帖子数')
    
    # 贴吧设置
    is_public = models.BooleanField(default=True, verbose_name='是否公开')
    join_need_approval = models.BooleanField(default=False, verbose_name='加入需要审核')
    post_need_approval = models.BooleanField(default=False, verbose_name='发帖需要审核')
    
    # 管理信息
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tiebas', verbose_name='创建者')
    moderators = models.ManyToManyField(User, related_name='moderated_tiebas', blank=True, verbose_name='吧务团队')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '贴吧'
        verbose_name_plural = '贴吧'
        ordering = ['-member_count', '-created_at']
    
    def __str__(self):
        return self.title

class TiebaMember(models.Model):
    """贴吧成员"""
    
    MEMBER_ROLES = [
        ('member', '普通成员'),
        ('moderator', '小吧主'),
        ('admin', '大吧主'),
    ]
    
    MEMBER_STATUS = [
        ('pending', '待审核'),
        ('active', '正常'),
        ('banned', '封禁'),
        ('left', '已退出'),
    ]
    
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='members', verbose_name='贴吧')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tieba_memberships', verbose_name='用户')
    
    # 成员信息
    role = models.CharField(max_length=20, choices=MEMBER_ROLES, default='member', verbose_name='角色')
    status = models.CharField(max_length=20, choices=MEMBER_STATUS, default='active', verbose_name='状态')
    level = models.IntegerField(default=1, verbose_name='贴吧等级')
    experience = models.IntegerField(default=0, verbose_name='贴吧经验')
    
    # 签到信息
    sign_in_count = models.IntegerField(default=0, verbose_name='签到次数')
    last_sign_in = models.DateTimeField(null=True, blank=True, verbose_name='最后签到时间')
    continuous_sign_in = models.IntegerField(default=0, verbose_name='连续签到天数')
    
    # 时间戳
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '贴吧成员'
        verbose_name_plural = '贴吧成员'
        unique_together = ('tieba', 'user')
        ordering = ['-role', '-experience', 'joined_at']
    
    def __str__(self):
        return f"{self.user} - {self.tieba}"

class TiebaFollow(models.Model):
    """贴吧关注"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tieba_follows', verbose_name='用户')
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='followers', verbose_name='贴吧')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='关注时间')
    
    class Meta:
        verbose_name = '贴吧关注'
        verbose_name_plural = '贴吧关注'
        unique_together = ('user', 'tieba')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} 关注 {self.tieba}"

class TiebaAnnouncement(models.Model):
    """贴吧公告"""
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='announcements', verbose_name='贴吧')
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发布者')
    is_pinned = models.BooleanField(default=False, verbose_name='是否置顶')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '贴吧公告'
        verbose_name_plural = '贴吧公告'
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return self.title

class TiebaRule(models.Model):
    """贴吧规则"""
    tieba = models.ForeignKey(Tieba, on_delete=models.CASCADE, related_name='rules', verbose_name='贴吧')
    title = models.CharField(max_length=200, verbose_name='规则标题')
    content = models.TextField(verbose_name='规则内容')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '贴吧规则'
        verbose_name_plural = '贴吧规则'
        ordering = ['sort_order', 'created_at']
    
    def __str__(self):
        return self.title