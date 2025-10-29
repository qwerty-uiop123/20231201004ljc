from django.urls import path
from . import views

urlpatterns = [
    # 认证相关
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # 用户资料
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('settings/', views.UserSettingsView.as_view(), name='settings'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    
    # 用户关注
    path('follow/', views.UserFollowView.as_view(), name='follow'),
    
    # 验证接口
    path('check-username/', views.check_username, name='check_username'),
    path('check-email/', views.check_email, name='check_email'),
]