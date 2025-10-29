from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from .models import User, UserSettings, UserFollow
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserProfileUpdateSerializer, UserSettingsSerializer, UserFollowSerializer,
    PasswordChangeSerializer
)

class UserRegistrationView(APIView):
    """用户注册视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'message': '注册成功',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """用户登录视图"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 生成JWT token
            refresh = RefreshToken.for_user(user)
            
            # 可选：同时进行session登录
            login(request, user)
            
            return Response({
                'success': True,
                'message': '登录成功',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
        
        return Response({
            'success': False,
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    """用户退出登录视图"""
    
    def post(self, request):
        logout(request)
        return Response({
            'success': True,
            'message': '退出登录成功'
        })

class UserProfileView(APIView):
    """用户资料视图"""
    
    def get(self, request):
        """获取当前用户资料"""
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        })
    
    def put(self, request):
        """更新用户资料"""
        serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '资料更新成功',
                'user': UserSerializer(request.user).data
            })
        
        return Response({
            'success': False,
            'message': '资料更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserSettingsView(APIView):
    """用户设置视图"""
    
    def get(self, request):
        """获取用户设置"""
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings)
        return Response({
            'success': True,
            'settings': serializer.data
        })
    
    def put(self, request):
        """更新用户设置"""
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '设置更新成功',
                'settings': serializer.data
            })
        
        return Response({
            'success': False,
            'message': '设置更新失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    """密码修改视图"""
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # 验证旧密码
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'success': False,
                    'message': '旧密码错误'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 设置新密码
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'success': True,
                'message': '密码修改成功'
            })
        
        return Response({
            'success': False,
            'message': '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserFollowView(APIView):
    """用户关注视图"""
    
    def post(self, request):
        """关注用户"""
        serializer = UserFollowSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'success': False,
                    'message': '用户不存在'
                }, status=status.HTTP_404_NOT_FOUND)
            
            if request.user == target_user:
                return Response({
                    'success': False,
                    'message': '不能关注自己'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 检查是否已关注
            if UserFollow.objects.filter(follower=request.user, following=target_user).exists():
                return Response({
                    'success': False,
                    'message': '已关注该用户'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建关注关系
            UserFollow.objects.create(follower=request.user, following=target_user)
            
            return Response({
                'success': True,
                'message': '关注成功'
            })
        
        return Response({
            'success': False,
            'message': '关注失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """取消关注"""
        serializer = UserFollowSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            
            try:
                target_user = User.objects.get(id=user_id)
                follow = UserFollow.objects.get(follower=request.user, following=target_user)
                follow.delete()
                
                return Response({
                    'success': True,
                    'message': '取消关注成功'
                })
            except (User.DoesNotExist, UserFollow.DoesNotExist):
                return Response({
                    'success': False,
                    'message': '关注关系不存在'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'success': False,
            'message': '取消关注失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_username(request):
    """检查用户名是否可用"""
    username = request.GET.get('username')
    if not username:
        return Response({
            'success': False,
            'message': '用户名不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(username=username).exists()
    return Response({
        'success': True,
        'available': not exists,
        'message': '用户名已存在' if exists else '用户名可用'
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_email(request):
    """检查邮箱是否可用"""
    email = request.GET.get('email')
    if not email:
        return Response({
            'success': False,
            'message': '邮箱不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(email=email).exists()
    return Response({
        'success': True,
        'available': not exists,
        'message': '邮箱已存在' if exists else '邮箱可用'
    })