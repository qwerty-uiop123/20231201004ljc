from rest_framework import serializers
from .models import Post, PostImage, Reply, ReplyImage, PostLike, ReplyLike, PostFavorite, PostViewHistory
from users.models import User
from tiebas.models import Tieba

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order', 'created_at']

class ReplyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyImage
        fields = ['id', 'image', 'order', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.CharField(source='author.avatar', read_only=True)
    tieba_name = serializers.CharField(source='tieba.name', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author', 'author_name', 'author_avatar',
            'tieba', 'tieba_name', 'like_count', 'reply_count', 'is_liked', 'is_favorited',
            'images', 'is_anonymous', 'is_top', 'is_essence', 'status', 'created_at', 'updated_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(user=request.user, post=obj).exists()
        return False
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostFavorite.objects.filter(user=request.user, post=obj).exists()
        return False

class PostDetailSerializer(PostSerializer):
    replies = serializers.SerializerMethodField()
    
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['replies']
    
    def get_replies(self, obj):
        replies = Reply.objects.filter(post=obj, parent__isnull=True).order_by('created_at')
        return ReplySerializer(replies, many=True, context=self.context).data

class ReplySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.CharField(source='author.avatar', read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    images = ReplyImageSerializer(many=True, read_only=True)
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Reply
        fields = [
            'id', 'content', 'author', 'author_name', 'author_avatar', 'post', 'parent',
            'like_count', 'is_liked', 'images', 'children', 'is_anonymous', 'created_at'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ReplyLike.objects.filter(user=request.user, reply=obj).exists()
        return False
    
    def get_children(self, obj):
        children = Reply.objects.filter(parent=obj).order_by('created_at')
        return ReplySerializer(children, many=True, context=self.context).data

class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tieba', 'is_anonymous', 'images']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)
        
        # 保存图片
        for i, image_data in enumerate(images_data):
            PostImage.objects.create(post=post, image=image_data, order=i)
        
        return post

class ReplyCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False
    )
    
    class Meta:
        model = Reply
        fields = ['content', 'post', 'parent', 'is_anonymous', 'images']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        reply = Reply.objects.create(**validated_data)
        
        # 保存图片
        for i, image_data in enumerate(images_data):
            ReplyImage.objects.create(reply=reply, image=image_data, order=i)
        
        return reply

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'created_at']

class ReplyLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyLike
        fields = ['id', 'user', 'reply', 'created_at']

class PostFavoriteSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_author = serializers.CharField(source='post.author.username', read_only=True)
    
    class Meta:
        model = PostFavorite
        fields = ['id', 'user', 'post', 'post_title', 'post_author', 'created_at']

class PostViewHistorySerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_author = serializers.CharField(source='post.author.username', read_only=True)
    
    class Meta:
        model = PostViewHistory
        fields = ['id', 'user', 'post', 'post_title', 'post_author', 'viewed_at']