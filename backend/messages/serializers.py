from rest_framework import serializers
from .models import Conversation, PrivateMessage, MessageAttachment, ConversationParticipant, SystemNotification, UserBlock
from users.models import User

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'file_name', 'file_size', 'file_type', 'created_at']

class PrivateMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    sender_avatar = serializers.CharField(source='sender.avatar', read_only=True)
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = PrivateMessage
        fields = [
            'id', 'conversation', 'sender', 'sender_name', 'sender_avatar',
            'content', 'type', 'attachments', 'is_read', 'created_at'
        ]

class ConversationParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)
    
    class Meta:
        model = ConversationParticipant
        fields = [
            'id', 'user', 'username', 'avatar', 'conversation',
            'is_muted', 'is_blocked', 'unread_count', 'last_read_at'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    participants = ConversationParticipantSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'title', 'type', 'participants', 'last_message',
            'message_count', 'unread_count', 'last_message_at', 'created_at'
        ]
    
    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-created_at').first()
        if last_message:
            return PrivateMessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            participant = obj.participants.filter(user=request.user).first()
            return participant.unread_count if participant else 0
        return 0

class ConversationDetailSerializer(ConversationSerializer):
    messages = serializers.SerializerMethodField()
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages']
    
    def get_messages(self, obj):
        messages = obj.messages.order_by('created_at')
        return PrivateMessageSerializer(messages, many=True).data

class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    
    class Meta:
        model = Conversation
        fields = ['title', 'type', 'participant_ids']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # 添加参与者
        for user_id in participant_ids:
            user = User.objects.get(id=user_id)
            ConversationParticipant.objects.create(
                conversation=conversation,
                user=user
            )
        
        return conversation

class PrivateMessageCreateSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(),
        required=False
    )
    
    class Meta:
        model = PrivateMessage
        fields = ['conversation', 'content', 'type', 'attachments']
    
    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        message = PrivateMessage.objects.create(**validated_data)
        
        # 保存附件
        for attachment_data in attachments_data:
            MessageAttachment.objects.create(message=message, file=attachment_data)
        
        # 更新对话的最后消息时间
        message.conversation.update_last_message()
        
        return message

class SystemNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemNotification
        fields = ['id', 'recipient', 'title', 'content', 'type', 'is_read', 'created_at']

class UserBlockSerializer(serializers.ModelSerializer):
    blocked_username = serializers.CharField(source='blocked.username', read_only=True)
    
    class Meta:
        model = UserBlock
        fields = ['id', 'blocker', 'blocked', 'blocked_username', 'created_at']

class MarkMessagesAsReadSerializer(serializers.Serializer):
    message_ids = serializers.ListField(
        child=serializers.IntegerField()
    )

class SendMessageSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()
    content = serializers.CharField()
    type = serializers.ChoiceField(choices=['text', 'image', 'file'], default='text')