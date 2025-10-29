from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from .models import Conversation, PrivateMessage, MessageAttachment, ConversationParticipant, SystemNotification, UserBlock
from .serializers import (
    ConversationSerializer, ConversationDetailSerializer, ConversationCreateSerializer,
    PrivateMessageSerializer, PrivateMessageCreateSerializer, SystemNotificationSerializer,
    UserBlockSerializer, MarkMessagesAsReadSerializer, SendMessageSerializer
)
from users.models import User

class ConversationListView(generics.ListAPIView):
    """获取对话列表"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 获取用户参与的所有对话
        return Conversation.objects.filter(
            participant_status__user=self.request.user
        ).prefetch_related('participants', 'participant_status', 'participant_status__user').order_by('-last_message_at')

class ConversationDetailView(generics.RetrieveAPIView):
    """获取对话详情"""
    serializer_class = ConversationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # 只能获取用户参与的对话
        return Conversation.objects.filter(participants__user=self.request.user)
    
    def get(self, request, *args, **kwargs):
        # 标记对话为已读
        conversation = self.get_object()
        participant = conversation.participants.filter(user=request.user).first()
        if participant:
            participant.mark_as_read()
        
        return super().get(request, *args, **kwargs)

class ConversationCreateView(generics.CreateAPIView):
    """创建对话"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        # 添加当前用户为参与者
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=self.request.user
        )

class PrivateMessageListView(generics.ListAPIView):
    """获取对话的消息列表"""
    serializer_class = PrivateMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        conversation = get_object_or_404(Conversation, id=self.kwargs['pk'])
        # 检查用户是否参与该对话
        if not conversation.participants.filter(user=self.request.user).exists():
            return PrivateMessage.objects.none()
        
        return PrivateMessage.objects.filter(conversation=conversation).order_by('created_at')

class PrivateMessageCreateView(generics.CreateAPIView):
    """发送消息"""
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        # 检查用户是否参与该对话
        if not conversation.participants.filter(user=self.request.user).exists():
            raise serializers.ValidationError("您不是该对话的参与者")
        
        # 检查是否被对方屏蔽
        for participant in conversation.participants.exclude(user=self.request.user):
            if UserBlock.objects.filter(blocker=participant.user, blocked=self.request.user).exists():
                raise serializers.ValidationError("您已被对方屏蔽，无法发送消息")
        
        serializer.save(sender=self.request.user)

class SystemNotificationListView(generics.ListAPIView):
    """获取系统通知列表"""
    serializer_class = SystemNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SystemNotification.objects.filter(recipient=self.request.user).order_by('-created_at')

class SystemNotificationDetailView(generics.RetrieveAPIView):
    """获取系统通知详情"""
    serializer_class = SystemNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SystemNotification.objects.filter(recipient=self.request.user)
    
    def get(self, request, *args, **kwargs):
        # 标记通知为已读
        notification = self.get_object()
        notification.mark_as_read()
        
        return super().get(request, *args, **kwargs)

class UserBlockListView(generics.ListAPIView):
    """获取用户屏蔽列表"""
    serializer_class = UserBlockSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserBlock.objects.filter(blocker=self.request.user)

class UserBlockCreateView(generics.CreateAPIView):
    """屏蔽用户"""
    queryset = UserBlock.objects.all()
    serializer_class = UserBlockSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        blocked_user = serializer.validated_data['blocked']
        
        # 检查是否已经屏蔽
        if UserBlock.objects.filter(blocker=self.request.user, blocked=blocked_user).exists():
            raise serializers.ValidationError("已经屏蔽该用户")
        
        # 不能屏蔽自己
        if blocked_user == self.request.user:
            raise serializers.ValidationError("不能屏蔽自己")
        
        serializer.save(blocker=self.request.user)

class UserBlockDeleteView(generics.DestroyAPIView):
    """取消屏蔽用户"""
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        blocked_user = get_object_or_404(User, id=kwargs['pk'])
        block = get_object_or_404(UserBlock, blocker=request.user, blocked=blocked_user)
        
        block.delete()
        return Response({'message': '取消屏蔽成功'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_messages_as_read(request):
    """标记消息为已读"""
    serializer = MarkMessagesAsReadSerializer(data=request.data)
    if serializer.is_valid():
        message_ids = serializer.validated_data['message_ids']
        messages = PrivateMessage.objects.filter(
            id__in=message_ids,
            conversation__participants__user=request.user
        )
        
        for message in messages:
            message.mark_as_read(request.user)
        
        return Response({'message': '标记成功'}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_direct_message(request):
    """发送私信"""
    serializer = SendMessageSerializer(data=request.data)
    if serializer.is_valid():
        recipient = get_object_or_404(User, id=serializer.validated_data['recipient_id'])
        content = serializer.validated_data['content']
        message_type = serializer.validated_data['type']
        
        # 检查是否被对方屏蔽
        if UserBlock.objects.filter(blocker=recipient, blocked=request.user).exists():
            return Response({'error': '您已被对方屏蔽，无法发送消息'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 查找或创建对话
        conversation = Conversation.objects.filter(
            type='private',
            participant_status__user=request.user
        ).filter(
            participant_status__user=recipient
        ).distinct().first()
        
        if not conversation:
            # 创建新的私信对话
            conversation = Conversation.objects.create(type='private')
            ConversationParticipant.objects.create(conversation=conversation, user=request.user)
            ConversationParticipant.objects.create(conversation=conversation, user=recipient)
        
        # 发送消息
        message = PrivateMessage.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
            type=message_type
        )
        
        # 更新对话的最后消息时间
        conversation.update_last_message()
        
        return Response(PrivateMessageSerializer(message).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_count(request):
    """获取未读消息和通知数量"""
    # 未读私信数量 - 通过ConversationParticipant模型获取
    unread_messages = ConversationParticipant.objects.filter(
        user=request.user
    ).aggregate(total_unread=Sum('unread_count'))
    
    # 未读系统通知数量
    unread_notifications = SystemNotification.objects.filter(
        recipient=request.user, is_read=False
    ).count()
    
    return Response({
        'unread_messages': unread_messages['total_unread'] or 0,
        'unread_notifications': unread_notifications
    })