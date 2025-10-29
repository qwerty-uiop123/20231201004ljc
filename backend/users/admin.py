from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserSettings, UserFollow

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'nickname', 'email', 'level', 'post_count', 'is_active']
    list_filter = ['is_active', 'is_staff', 'level']
    search_fields = ['username', 'nickname', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('贴吧信息', {'fields': ('nickname', 'avatar', 'level', 'experience')}),
        ('用户统计', {'fields': ('post_count', 'reply_count', 'follow_count', 'follower_count')}),
        ('个人资料', {'fields': ('bio', 'location', 'website', 'weibo', 'qq')}),
    )

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'language', 'email_notifications']
    list_filter = ['theme', 'language', 'email_notifications']
    search_fields = ['user__username', 'user__nickname']

@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']