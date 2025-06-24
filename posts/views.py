from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from users.views import User
from .models import Post
from .serializers import PostSerializer

@extend_schema(
    responses=PostSerializer(many=True),
    description="Получить список постов. Можно фильтровать по `nickname` в query-параметрах. Пример(/?nickname=...)"
)

class PostListCreateAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        nickname = request.query_params.get('nickname')
        posts = Post.objects.all()
        if nickname:
            try:
                user = User.objects.get(nickname=nickname)
                posts = posts.filter(author=user)
            except User.DoesNotExist:
                return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        posts = posts.order_by('-created_at')  # сортировка по дате (сначала новые)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """
        Создать новый пост. Требуется авторизация.
                - Поля тела запроса:
            - title
            - content
            - profession
            - image
        """
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={
        200: OpenApiTypes.OBJECT,
        404: {"error": "Post not found"}
    },
    description="Лайк/дизлайк поста"
)
class LikePostAPIView(APIView):
    """
    Лайк или дизлайк поста. Возвращает количество лайков и статус is_liked.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            is_liked = False
        else:
            post.likes.add(user)
            is_liked = True

        return Response({
            "likes_count": post.likes.count(),
            "is_liked": is_liked
        }, status=status.HTTP_200_OK)