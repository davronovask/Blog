from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post
from .serializers import PostSerializer


class PostListCreateAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        """
        Получить список всех постов. Можно фильтровать по заголовку с помощью параметра ?search=.
        """
        search = request.query_params.get('search', '')
        posts = Post.objects.filter(title__icontains=search).order_by('-created_at')
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


class LikePostAPIView(APIView):
    """
    Лайк или дизлайк поста. Возвращает только количество лайков.
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
        else:
            post.likes.add(user)

        return Response({"likes_count": post.likes.count()}, status=status.HTTP_200_OK)