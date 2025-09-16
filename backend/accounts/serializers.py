from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},  # 密码不返回给前端
            'email': {'required': True}
        }

    def validate(self, attrs):
        # 验证两次输入的密码是否一致
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次密码输入不一致"})
        return attrs

    def create(self, validated_data):
        # 移除password2字段（数据库中不需要）
        validated_data.pop('password2')
        # 创建用户（Django会自动加密密码）
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """用于用户详情的序列化器"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')  # 只返回安全的字段
        read_only_fields = fields  # 详情接口通常不允许修改，全部设为只读