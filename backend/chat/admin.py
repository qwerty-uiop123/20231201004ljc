from django.contrib import admin
from .models import Conversation, PrivateMessage, MessageAttachment, ConversationParticipant, SystemNotification, UserBlock

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'message_count', 'unread_count', 'last_message_at', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['title']
    filter_horizontal = ['participants']

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['content', 'sender__username']

@admin.register(MessageAttachment)
class MessageAttachmentAdmin(admin.ModelAdmin):
    list_display = ['message', 'file_name', 'file_size', 'file_type', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['file_name', 'message__content']

@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'user', 'is_muted', 'is_blocked', 'unread_count', 'last_read_at']
    list_filter = ['is_muted', 'is_blocked']
    search_fields = ['conversation__title', 'user__username']

@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    search_fields = ['title', 'content', 'recipient__username']

@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blocker__username', 'blocked__username']