from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from .models import Post, PostImage, Reply, ReplyImage, PostLike, ReplyLike, PostFavorite, PostViewHistory
from .serializers import (
    PostSerializer, PostDetailSerializer, PostCreateSerializer, ReplySerializer,
    ReplyCreateSerializer, PostLikeSerializer, ReplyLikeSerializer, PostFavoriteSerializer,
    PostViewHistorySerializer
)
from tiebas.models import Tieba

class PostListView(generics.ListAPIView):
    """获取帖子列表"""
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'tieba').annotate(
            like_count=Count('likes'),
            reply_count=Count('replies')
        ).filter(status='published')
        
        # 贴吧过滤
        tieba_id = self.request.query_params.get('tieba', None)
        if tieba_id:
            queryset = queryset.filter(tieba_id=tieba_id)
        
        # 搜索过滤
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        
        # 排序
        sort = self.request.query_params.get('sort', 'created_at')
        if sort == 'created_at':
            queryset = queryset.order_by('-created_at')
        elif sort == 'like_count':
            queryset = queryset.order_by('-like_count')
        elif sort == 'reply_count':
            queryset = queryset.order_by('-reply_count')
        
        # 置顶帖子优先
        queryset = queryset.order_by('-is_top', '-created_at')
        
        return queryset

class PostDetailView(generics.RetrieveAPIView):
    """获取帖子详情"""
    queryset = Post.objects.select_related('author', 'tieba').annotate(
        annotated_like_count=Count('likes'),
        annotated_reply_count=Count('replies')
    ).filter(status='published')
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        # 记录浏览历史
        post = self.get_object()
        if request.user.is_authenticated:
            PostViewHistory.objects.create(user=request.user, post=post)
        
        return super().get(request, *args, **kwargs)

class PostCreateView(generics.CreateAPIView):
    """创建帖子"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # 检查用户是否是该贴吧的成员
        tieba = serializer.validated_data['tieba']
        if not tieba.is_public:
            # 对于非公开贴吧，需要检查成员身份
            from tiebas.models import TiebaMember
            if not TiebaMember.objects.filter(user=self.request.user, tieba=tieba).exists():
                raise serializers.ValidationError("您不是该贴吧的成员，无法发帖")
        
        serializer.save(author=self.request.user)

class PostUpdateView(generics.UpdateAPIView):
    """更新帖子"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只有帖子作者可以更新帖子
        return Post.objects.filter(author=self.request.user)

class PostDeleteView(generics.DestroyAPIView):
    """删除帖子"""
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只有帖子作者可以删除帖子
        return Post.objects.filter(author=self.request.user)

class PostLikeView(generics.CreateAPIView):
    """点赞帖子"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        
        # 检查是否已经点赞
        if PostLike.objects.filter(user=request.user, post=post).exists():
            return Response({'error': '已经点赞过该帖子'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 点赞
        PostLike.objects.create(user=request.user, post=post)
        return Response({'message': '点赞成功'}, status=status.HTTP_201_CREATED)

class PostUnlikeView(generics.DestroyAPIView):
    """取消点赞帖子"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        like = get_object_or_404(PostLike, user=request.user, post=post)
        
        like.delete()
        return Response({'message': '取消点赞成功'}, status=status.HTTP_200_OK)

class PostFavoriteView(generics.CreateAPIView):
    """收藏帖子"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        
        # 检查是否已经收藏
        if PostFavorite.objects.filter(user=request.user, post=post).exists():
            return Response({'error': '已经收藏过该帖子'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 收藏
        PostFavorite.objects.create(user=request.user, post=post)
        return Response({'message': '收藏成功'}, status=status.HTTP_201_CREATED)

class PostUnfavoriteView(generics.DestroyAPIView):
    """取消收藏帖子"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['pk'])
        favorite = get_object_or_404(PostFavorite, user=request.user, post=post)
        
        favorite.delete()
        return Response({'message': '取消收藏成功'}, status=status.HTTP_200_OK)

class ReplyCreateView(generics.CreateAPIView):
    """创建回复"""
    queryset = Reply.objects.all()
    serializer_class = ReplyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReplyLikeView(generics.CreateAPIView):
    """点赞回复"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        reply = get_object_or_404(Reply, id=kwargs['pk'])
        
        # 检查是否已经点赞
        if ReplyLike.objects.filter(user=request.user, reply=reply).exists():
            return Response({'error': '已经点赞过该回复'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 点赞
        ReplyLike.objects.create(user=request.user, reply=reply)
        return Response({'message': '点赞成功'}, status=status.HTTP_201_CREATED)

class ReplyUnlikeView(generics.DestroyAPIView):
    """取消点赞回复"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        reply = get_object_or_404(Reply, id=kwargs['pk'])
        like = get_object_or_404(ReplyLike, user=request.user, reply=reply)
        
        like.delete()
        return Response({'message': '取消点赞成功'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_posts(request):
    """获取用户发布的帖子列表"""
    posts = Post.objects.filter(author=request.user).select_related('tieba').annotate(
        like_count=Count('likes'),
        reply_count=Count('replies')
    ).order_by('-created_at')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_favorites(request):
    """获取用户收藏的帖子列表"""
    favorites = PostFavorite.objects.filter(user=request.user).select_related('post', 'post__tieba')
    serializer = PostFavoriteSerializer(favorites, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_view_history(request):
    """获取用户浏览历史"""
    history = PostViewHistory.objects.filter(user=request.user).select_related('post', 'post__tieba').order_by('-viewed_at')[:50]
    serializer = PostViewHistorySerializer(history, many=True)
    return Response(serializer.data)

class ReplyListView(generics.ListAPIView):
    """获取帖子的回复列表"""
    serializer_class = ReplySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return Reply.objects.filter(post=post, parent__isnull=True).select_related('author').annotate(
            like_count=Count('likes')
        ).order_by('created_at')