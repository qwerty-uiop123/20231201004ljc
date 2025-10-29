from rest_framework import serializers
from .models import TiebaCategory, Tieba, TiebaMember, TiebaFollow, TiebaAnnouncement, TiebaRule
from users.models import User

class TiebaCategorySerializer(serializers.ModelSerializer):
    tieba_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = TiebaCategory
        fields = ['id', 'name', 'description', 'icon', 'tieba_count', 'created_at']

class TiebaSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    is_followed = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = Tieba
        fields = [
            'id', 'name', 'description', 'avatar', 'banner', 'category', 'category_name',
            'member_count', 'post_count', 'is_public', 'is_official', 'is_followed', 'is_member',
            'created_at', 'updated_at'
        ]
    
    def get_is_followed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return TiebaFollow.objects.filter(user=request.user, tieba=obj).exists()
        return False
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return TiebaMember.objects.filter(user=request.user, tieba=obj).exists()
        return False

class TiebaDetailSerializer(TiebaSerializer):
    announcements = serializers.SerializerMethodField()
    rules = serializers.SerializerMethodField()
    
    class Meta(TiebaSerializer.Meta):
        fields = TiebaSerializer.Meta.fields + ['announcements', 'rules']
    
    def get_announcements(self, obj):
        announcements = TiebaAnnouncement.objects.filter(tieba=obj, is_active=True).order_by('-created_at')[:5]
        return TiebaAnnouncementSerializer(announcements, many=True).data
    
    def get_rules(self, obj):
        rules = TiebaRule.objects.filter(tieba=obj, is_active=True).order_by('order')
        return TiebaRuleSerializer(rules, many=True).data

class TiebaMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    
    class Meta:
        model = TiebaMember
        fields = ['id', 'user', 'username', 'avatar', 'tieba', 'role', 'joined_at', 'last_active_at']

class TiebaFollowSerializer(serializers.ModelSerializer):
    tieba_name = serializers.CharField(source='tieba.name', read_only=True)
    tieba_avatar = serializers.CharField(source='tieba.avatar', read_only=True)
    
    class Meta:
        model = TiebaFollow
        fields = ['id', 'tieba', 'tieba_name', 'tieba_avatar', 'created_at']

class TiebaAnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = TiebaAnnouncement
        fields = ['id', 'tieba', 'title', 'content', 'author', 'author_name', 'is_active', 'created_at', 'updated_at']

class TiebaRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiebaRule
        fields = ['id', 'tieba', 'title', 'content', 'order', 'is_active', 'created_at']

class TiebaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tieba
        fields = ['name', 'description', 'category', 'avatar', 'banner', 'is_public']
    
    def validate_name(self, value):
        if Tieba.objects.filter(name=value).exists():
            raise serializers.ValidationError("贴吧名称已存在")
        return value

class TiebaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tieba
        fields = ['description', 'avatar', 'banner', 'is_public']