from django.contrib import admin
from .models import TiebaCategory, Tieba, TiebaMember, TiebaFollow, TiebaAnnouncement, TiebaRule

@admin.register(TiebaCategory)
class TiebaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['sort_order', 'is_active']

@admin.register(Tieba)
class TiebaAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'category', 'member_count', 'post_count', 'is_public', 'created_at']
    list_filter = ['category', 'is_public', 'created_at']
    search_fields = ['name', 'title', 'description']
    filter_horizontal = ['moderators']
    readonly_fields = ['member_count', 'post_count']

@admin.register(TiebaMember)
class TiebaMemberAdmin(admin.ModelAdmin):
    list_display = ['tieba', 'user', 'role', 'status', 'level', 'joined_at']
    list_filter = ['role', 'status', 'tieba']
    search_fields = ['tieba__name', 'user__username']

@admin.register(TiebaFollow)
class TiebaFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'tieba', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'tieba__name']

@admin.register(TiebaAnnouncement)
class TiebaAnnouncementAdmin(admin.ModelAdmin):
    list_display = ['tieba', 'title', 'author', 'is_pinned', 'is_active', 'created_at']
    list_filter = ['is_pinned', 'is_active', 'tieba']
    search_fields = ['title', 'content']

@admin.register(TiebaRule)
class TiebaRuleAdmin(admin.ModelAdmin):
    list_display = ['tieba', 'title', 'sort_order', 'created_at']
    list_filter = ['tieba']
    search_fields = ['title', 'content']