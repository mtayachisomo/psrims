# users/serializers.py

from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
from .models import User, Role, UserRole, Permission, RolePermission, Position, UserPosition
from institutions.models import InstitutionUser
from institutions.serializers import InstitutionSerializer, InstitutionListSerializer

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'updated_at', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered with us.")
        return value

    def create(self, validated_data):
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
        )
        user.set_password(password)
        user.save()

        send_mail(
            'Your Account Password',
            f'Hello {user.first_name},\n\nYour Public Sector Reforms account has been created. Here is your password: {password}\n\nPlease change your password after logging in.',
            'crispinemtaya867@gmail.com',
            [user.email],
            fail_silently=False,
        )
        
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'updated_at', 'created_at']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    institutions = InstitutionListSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'updated_at', 'created_at', 'deleted', 'institutions']



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both email and password are required")

        data['user'] = user
        data['tokens'] = self.get_tokens(data)
        return data

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        if 'refresh_token' not in attrs:
            raise serializers.ValidationError("Refresh token is required.")
        return attrs

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new passwords do not match.")
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("No user is associated with this email address."))
        return value

    def save(self):
        request = self.context.get('request')
        user = User.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        password_reset_url = f"{request.scheme}://{request.get_host()}/users/password-reset-confirm/{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Hello, {user.first_name}.\n\nYou can reset your password by clicking the link below:\n{password_reset_url}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("The new passwords do not match.")
        
        return data

class RoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'created_at', 'updated_at']

class UserRoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_role = UserRole.objects.create(**validated_data)
        return user_role

class UserRoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'created_at', 'updated_at']
        
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'permission_code', 'description', 'created_at', 'updated_at']

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'created_at', 'updated_at']
        
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'position', 'created_at', 'updated_at', 'deleted']

class PositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'position']
        
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'position', 'created_at', 'updated_at', 'deleted']

class UserPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition
        fields = ['id', 'user', 'position', 'created_at', 'updated_at', 'deleted']

class UserPositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPosition
        fields = ['id', 'user', 'position', 'created_at', 'updated_at', 'deleted']

    def create(self, validated_data):
        user_position = UserPosition.objects.create(**validated_data)
        return user_position
    
class UserDetailSerializer(serializers.ModelSerializer):
    institutions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'institutions', 'roles', 'positions']

    def get_institutions(self, obj):
        institution_users = InstitutionUser.objects.filter(user=obj)
        institutions = [iu.institution for iu in institution_users]
        return InstitutionSerializer(institutions, many=True).data


    def get_roles(self, obj):
            roles = UserRole.objects.filter(user=obj)
            role_data = UserRoleSerializer(roles, many=True).data
            for role in role_data:
                role_id = role['role']
                role_obj = Role.objects.get(id=role_id)
                role['role'] = RoleSerializer(role_obj).data
            return role_data

    def get_positions(self, obj):
        positions = UserPosition.objects.filter(user=obj)
        position_data = UserPositionSerializer(positions, many=True).data
        for position in position_data:
            position_id = position['position']
            position_obj = Position.objects.get(id=position_id)
            position['position'] = PositionSerializer(position_obj).data
        return position_data