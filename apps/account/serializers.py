from datetime import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.account.models import User, UserToken


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password], help_text=password_validators_help_texts)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        if password1 != password2:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validated_data.pop('password2')
        user = super(UserRegisterSerializer, self).create(validated_data)
        user.set_password(password1)
        user.save()
        return user


class SendEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email does not exist')
        return attrs


class VerifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    token = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['email', 'token']

    def validate(self, attrs):
        email = attrs.get('email')
        token = attrs.get('token')
        if UserToken.objects.filter(user__email=email).exists():
            user_token = UserToken.objects.filter(user__email=email).last()
            if user_token.is_used:
                raise ValidationError('Verification code already exists')
            if token != user_token.token:
                raise ValidationError('Token does not match')
            user_token.is_user = True
            user = User.objects.get(email=email)
            user.is_active = True
            user_token.save()
            user.save()
            return attrs
        raise ValidationError('Email already verified')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['created_date'] = user.created_date.strftime('%d.%m.%Y %H:%M:%S ')
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, validators=[validate_password])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if self.context['request'].user.check_password(old_password):
            if old_password == password:
                raise serializers.ValidationError('Current must not equal to new password')
            if password == password2:
                return attrs
            raise ValidationError('Password do not match')
        raise ValidationError('Old password does not match')

    def create(self, validated_data):
        password = validated_data.get('password')
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if self.context['request'].user.check_password(password):
            raise serializers.ValidationError('Current must not equal to new password')
        if password == password2:
            return attrs
        raise ValidationError('Passwords do not match')

    def create(self, validated_data):
        password = validated_data.get('password')
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'avatar', 'is_staff', 'modified_date', 'created_date')
