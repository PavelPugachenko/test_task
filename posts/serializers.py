from rest_framework import serializers
from .models import User, Post, Comment
from .validators import (
    validate_password,
    validate_email_domain,
    validate_title_forbidden_words,
    validate_author_age
)
from django.contrib.auth.password_validation import validate_password as django_validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'phone',
            'birth_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_email(self, value):
        validate_email_domain(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'comments', 'created_at', 'updated_at']
        read_only_fields = ['author']

    def validate_title(self, value):
        validate_title_forbidden_words(value)
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(author=user, **validated_data)
        validate_author_age(post)
        return post

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        validate_author_age(instance)  # Проверяем возраст при обновлении
        return instance