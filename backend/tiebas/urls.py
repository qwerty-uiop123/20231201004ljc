from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # 贴吧分类
    path('categories/', views.TiebaCategoryListView.as_view(), name='tieba-category-list'),
    
    # 贴吧列表和创建
    path('', views.TiebaListView.as_view(), name='tieba-list'),
    path('create/', views.TiebaCreateView.as_view(), name='tieba-create'),
    
    # 贴吧详情和更新
    path('<int:pk>/', views.TiebaDetailView.as_view(), name='tieba-detail'),
    path('<int:pk>/update/', views.TiebaUpdateView.as_view(), name='tieba-update'),
    
    # 贴吧成员操作
    path('<int:pk>/join/', views.TiebaJoinView.as_view(), name='tieba-join'),
    path('<int:pk>/leave/', views.TiebaLeaveView.as_view(), name='tieba-leave'),
    path('<int:pk>/follow/', views.TiebaFollowView.as_view(), name='tieba-follow'),
    path('<int:pk>/unfollow/', views.TiebaUnfollowView.as_view(), name='tieba-unfollow'),
    
    # 贴吧成员列表
    path('<int:pk>/members/', views.TiebaMemberListView.as_view(), name='tieba-member-list'),
    
    # 贴吧公告和规则
    path('<int:pk>/announcements/', views.TiebaAnnouncementListView.as_view(), name='tieba-announcement-list'),
    path('<int:pk>/rules/', views.TiebaRuleListView.as_view(), name='tieba-rule-list'),
    
    # 用户相关的贴吧
    path('user/followed/', views.user_followed_tiebas, name='user-followed-tiebas'),
    path('user/joined/', views.user_joined_tiebas, name='user-joined-tiebas'),
]