from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # 帖子列表和创建
    path('', views.PostListView.as_view(), name='post-list'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    
    # 帖子详情、更新和删除
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    # 帖子点赞和收藏
    path('<int:pk>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', views.PostUnlikeView.as_view(), name='post-unlike'),
    path('<int:pk>/favorite/', views.PostFavoriteView.as_view(), name='post-favorite'),
    path('<int:pk>/unfavorite/', views.PostUnfavoriteView.as_view(), name='post-unfavorite'),
    
    # 回复相关
    path('<int:pk>/replies/', views.ReplyListView.as_view(), name='post-reply-list'),
    path('replies/create/', views.ReplyCreateView.as_view(), name='reply-create'),
    path('replies/<int:pk>/like/', views.ReplyLikeView.as_view(), name='reply-like'),
    path('replies/<int:pk>/unlike/', views.ReplyUnlikeView.as_view(), name='reply-unlike'),
    
    # 用户相关的帖子
    path('user/posts/', views.user_posts, name='user-posts'),
    path('user/favorites/', views.user_favorites, name='user-favorites'),
    path('user/history/', views.user_view_history, name='user-view-history'),
]