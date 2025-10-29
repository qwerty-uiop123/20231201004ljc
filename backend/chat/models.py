from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    """私信对话"""
    
    CONVERSATION_TYPES = [
        ('private', '私信'),
        ('group', '群聊'),
    ]
    
    # 基本信息
    title = models.CharField(max_length=200, blank=True, verbose_name='对话标题')
    type = models.CharField(max_length=20, choices=CONVERSATION_TYPES, default='private', verbose_name='对话类型')
    
    # 参与者
    participants = models.ManyToManyField(User, related_name='conversations', verbose_name='参与者')
    
    # 统计信息
    message_count = models.IntegerField(default=0, verbose_name='消息数')
    unread_count = models.IntegerField(default=0, verbose_name='未读消息数')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    last_message_at = models.DateTimeField(null=True, blank=True, verbose_name='最后消息时间')
    
    class Meta:
        verbose_name = '私信对话'
        verbose_name_plural = '私信对话'
        ordering = ['-last_message_at', '-updated_at']
    
    def __str__(self):
        if self.title:
            return self.title
        participants = self.participants.all()[:3]
        names = [user.nickname or user.username for user in participants]
        return ', '.join(names)
    
    def update_last_message(self):
        """更新最后消息时间和统计信息"""
        last_message = self.messages.order_by('-created_at').first()
        if last_message:
            self.last_message_at = last_message.created_at
            self.message_count = self.messages.count()
            self.save()

class PrivateMessage(models.Model):
    """私信消息"""
    
    MESSAGE_TYPES = [
        ('text', '文本'),
        ('image', '图片'),
        ('file', '文件'),
        ('system', '系统消息'),
    ]
    
    # 基本信息
    content = models.TextField(verbose_name='消息内容')
    type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text', verbose_name='消息类型')
    
    # 关联信息
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name='对话')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    
    # 消息状态
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    
    class Meta:
        verbose_name = '私信消息'
        verbose_name_plural = '私信消息'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.sender} -> {self.conversation}: {self.content[:50]}"

class MessageAttachment(models.Model):
    """消息附件"""
    message = models.ForeignKey(PrivateMessage, on_delete=models.CASCADE, related_name='attachments', verbose_name='消息')
    file = models.FileField(upload_to='message_attachments/', verbose_name='附件文件')
    file_name = models.CharField(max_length=255, verbose_name='文件名')
    file_size = models.IntegerField(default=0, verbose_name='文件大小')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        verbose_name = '消息附件'
        verbose_name_plural = '消息附件'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.message} - {self.file_name}"

class ConversationParticipant(models.Model):
    """对话参与者状态"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='participant_status', verbose_name='对话')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_status', verbose_name='用户')
    
    # 参与者状态
    is_muted = models.BooleanField(default=False, verbose_name='是否静音')
    is_blocked = models.BooleanField(default=False, verbose_name='是否屏蔽')
    unread_count = models.IntegerField(default=0, verbose_name='未读消息数')
    last_read_at = models.DateTimeField(null=True, blank=True, verbose_name='最后阅读时间')
    
    # 时间戳
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name='加入时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '对话参与者状态'
        verbose_name_plural = '对话参与者状态'
        unique_together = ('conversation', 'user')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user} - {self.conversation}"

class SystemNotification(models.Model):
    """系统通知"""
    
    NOTIFICATION_TYPES = [
        ('post_reply', '帖子回复'),
        ('post_like', '帖子点赞'),
        ('reply_like', '回复点赞'),
        ('follow', '用户关注'),
        ('tieba_join', '贴吧加入'),
        ('tieba_announcement', '贴吧公告'),
        ('system', '系统消息'),
    ]
    
    # 基本信息
    title = models.CharField(max_length=200, verbose_name='通知标题')
    content = models.TextField(verbose_name='通知内容')
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='system', verbose_name='通知类型')
    
    # 关联信息
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='接收者')
    
    # 关联对象（可选）
    related_post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联帖子')
    related_reply = models.ForeignKey('posts.Reply', on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联回复')
    related_tieba = models.ForeignKey('tiebas.Tieba', on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联贴吧')
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                                    related_name='sent_notifications', verbose_name='关联用户')
    
    # 通知状态
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '系统通知'
        verbose_name_plural = '系统通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.recipient} - {self.title}"

class UserBlock(models.Model):
    """用户屏蔽"""
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users', verbose_name='屏蔽者')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_by', verbose_name='被屏蔽者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='屏蔽时间')
    
    class Meta:
        verbose_name = '用户屏蔽'
        verbose_name_plural = '用户屏蔽'
        unique_together = ('blocker', 'blocked')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.blocker} 屏蔽 {self.blocked}"