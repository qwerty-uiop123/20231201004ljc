from django.contrib import admin
from .models import Post, PostImage, Reply, ReplyImage, PostLike, ReplyLike, PostFavorite, PostViewHistory

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'tieba', 'author', 'type', 'status', 'view_count', 'reply_count', 'created_at']
    list_filter = ['type', 'status', 'tieba', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['view_count', 'reply_count', 'like_count', 'favorite_count']
    list_editable = ['status']

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'caption', 'sort_order', 'created_at']
    list_filter = ['post__tieba']
    search_fields = ['post__title', 'caption']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'floor', 'status', 'like_count', 'created_at']
    list_filter = ['status', 'post__tieba']
    search_fields = ['content']

@admin.register(ReplyImage)
class ReplyImageAdmin(admin.ModelAdmin):
    list_display = ['reply', 'created_at']
    list_filter = ['reply__post__tieba']

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username']

@admin.register(ReplyLike)
class ReplyLikeAdmin(admin.ModelAdmin):
    list_display = ['reply', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['reply__post__title', 'user__username']

@admin.register(PostFavorite)
class PostFavoriteAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username']

@admin.register(PostViewHistory)
class PostViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'user__username']