from rest_framework import serializers
from .models import Post
from drf_spectacular.utils import extend_schema_field

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    nickname = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'nickname',
            'content',
            'profession',
            'image',
            'created_at',
            'likes_count',
            'is_liked',
        ]
        read_only_fields = ['author', 'created_at']

    def get_nickname(self, obj):
        return obj.author.nickname

    @extend_schema_field(serializers.IntegerField())
    def get_likes_count(self, obj):
        return obj.likes.count()

    @extend_schema_field(serializers.BooleanField())
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False
