from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    # 对话相关
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('conversations/create/', views.ConversationCreateView.as_view(), name='conversation-create'),
    path('conversations/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    
    # 消息相关
    path('conversations/<int:pk>/messages/', views.PrivateMessageListView.as_view(), name='message-list'),
    path('messages/create/', views.PrivateMessageCreateView.as_view(), name='message-create'),
    path('messages/mark-read/', views.mark_messages_as_read, name='mark-messages-read'),
    
    # 私信发送
    path('send/', views.send_direct_message, name='send-direct-message'),
    
    # 系统通知
    path('notifications/', views.SystemNotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.SystemNotificationDetailView.as_view(), name='notification-detail'),
    
    # 用户屏蔽
    path('blocks/', views.UserBlockListView.as_view(), name='block-list'),
    path('blocks/create/', views.UserBlockCreateView.as_view(), name='block-create'),
    path('blocks/<int:pk>/delete/', views.UserBlockDeleteView.as_view(), name='block-delete'),
    
    # 未读数量
    path('unread-count/', views.unread_count, name='unread-count'),
]