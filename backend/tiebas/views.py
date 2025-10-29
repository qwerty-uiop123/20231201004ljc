from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from .models import TiebaCategory, Tieba, TiebaMember, TiebaFollow, TiebaAnnouncement, TiebaRule
from .serializers import (
    TiebaCategorySerializer, TiebaSerializer, TiebaDetailSerializer,
    TiebaMemberSerializer, TiebaFollowSerializer, TiebaAnnouncementSerializer,
    TiebaRuleSerializer, TiebaCreateSerializer, TiebaUpdateSerializer
)

class TiebaCategoryListView(generics.ListAPIView):
    """获取贴吧分类列表"""
    queryset = TiebaCategory.objects.annotate(tieba_count=Count('tieba'))
    serializer_class = TiebaCategorySerializer
    permission_classes = [permissions.AllowAny]

class TiebaListView(generics.ListAPIView):
    """获取贴吧列表"""
    serializer_class = TiebaSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Tieba.objects.select_related('category').annotate(
            annotated_member_count=Count('members'),
            annotated_post_count=Count('posts')
        )
        
        # 搜索过滤
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        
        # 分类过滤
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 排序
        sort = self.request.query_params.get('sort', 'annotated_member_count')
        if sort == 'annotated_member_count':
            queryset = queryset.order_by('-annotated_member_count')
        elif sort == 'annotated_post_count':
            queryset = queryset.order_by('-annotated_post_count')
        elif sort == 'created_at':
            queryset = queryset.order_by('-created_at')
        
        return queryset

class TiebaDetailView(generics.RetrieveAPIView):
    """获取贴吧详情"""
    queryset = Tieba.objects.select_related('category').annotate(
        annotated_member_count=Count('members'),
        annotated_post_count=Count('posts')
    )
    serializer_class = TiebaDetailSerializer
    permission_classes = [permissions.AllowAny]

class TiebaCreateView(generics.CreateAPIView):
    """创建贴吧"""
    queryset = Tieba.objects.all()
    serializer_class = TiebaCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        tieba = serializer.save()
        # 创建贴吧后，自动成为贴吧管理员
        TiebaMember.objects.create(
            user=self.request.user,
            tieba=tieba,
            role='admin'
        )

class TiebaUpdateView(generics.UpdateAPIView):
    """更新贴吧信息"""
    queryset = Tieba.objects.all()
    serializer_class = TiebaUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只有贴吧管理员可以更新贴吧信息
        return Tieba.objects.filter(members__user=self.request.user, members__role='admin')

class TiebaJoinView(generics.CreateAPIView):
    """加入贴吧"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        tieba = get_object_or_404(Tieba, id=kwargs['pk'])
        
        # 检查是否已经是成员
        if TiebaMember.objects.filter(user=request.user, tieba=tieba).exists():
            return Response({'error': '已经是该贴吧成员'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查贴吧是否公开
        if not tieba.is_public:
            return Response({'error': '该贴吧不公开，无法加入'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 加入贴吧
        TiebaMember.objects.create(user=request.user, tieba=tieba, role='member')
        return Response({'message': '成功加入贴吧'}, status=status.HTTP_201_CREATED)

class TiebaLeaveView(generics.DestroyAPIView):
    """退出贴吧"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        tieba = get_object_or_404(Tieba, id=kwargs['pk'])
        membership = get_object_or_404(TiebaMember, user=request.user, tieba=tieba)
        
        # 检查是否是贴吧管理员（管理员不能退出，只能转让或删除贴吧）
        if membership.role == 'admin':
            return Response({'error': '贴吧管理员不能退出，请先转让管理员权限'}, status=status.HTTP_400_BAD_REQUEST)
        
        membership.delete()
        return Response({'message': '成功退出贴吧'}, status=status.HTTP_200_OK)

class TiebaFollowView(generics.CreateAPIView):
    """关注贴吧"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        tieba = get_object_or_404(Tieba, id=kwargs['pk'])
        
        # 检查是否已经关注
        if TiebaFollow.objects.filter(user=request.user, tieba=tieba).exists():
            return Response({'error': '已经关注该贴吧'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 关注贴吧
        TiebaFollow.objects.create(user=request.user, tieba=tieba)
        return Response({'message': '成功关注贴吧'}, status=status.HTTP_201_CREATED)

class TiebaUnfollowView(generics.DestroyAPIView):
    """取消关注贴吧"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        tieba = get_object_or_404(Tieba, id=kwargs['pk'])
        follow = get_object_or_404(TiebaFollow, user=request.user, tieba=tieba)
        
        follow.delete()
        return Response({'message': '成功取消关注'}, status=status.HTTP_200_OK)

class TiebaMemberListView(generics.ListAPIView):
    """获取贴吧成员列表"""
    serializer_class = TiebaMemberSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tieba = get_object_or_404(Tieba, id=self.kwargs['pk'])
        return TiebaMember.objects.filter(tieba=tieba).select_related('user')

class TiebaAnnouncementListView(generics.ListAPIView):
    """获取贴吧公告列表"""
    serializer_class = TiebaAnnouncementSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tieba = get_object_or_404(Tieba, id=self.kwargs['pk'])
        return TiebaAnnouncement.objects.filter(tieba=tieba, is_active=True).order_by('-created_at')

class TiebaRuleListView(generics.ListAPIView):
    """获取贴吧规则列表"""
    serializer_class = TiebaRuleSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tieba = get_object_or_404(Tieba, id=self.kwargs['pk'])
        return TiebaRule.objects.filter(tieba=tieba, is_active=True).order_by('order')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_followed_tiebas(request):
    """获取用户关注的贴吧列表"""
    followed_tiebas = TiebaFollow.objects.filter(user=request.user).select_related('tieba')
    serializer = TiebaFollowSerializer(followed_tiebas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_joined_tiebas(request):
    """获取用户加入的贴吧列表"""
    joined_tiebas = TiebaMember.objects.filter(user=request.user).select_related('tieba')
    serializer = TiebaMemberSerializer(joined_tiebas, many=True)
    return Response(serializer.data)