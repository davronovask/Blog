from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Post
from .serializers import PostSerializer


class PostListCreateAPIView(APIView):
    """
    Представление для получения списка постов и создания нового поста.
    GET — возвращает ленту постов, с опциональным поиском по заголовку (?search=).
    POST — создаёт новый пост. Требуется авторизация.
    """
    permission_classes = [permissions.IsAuthenticated]

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
        """
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikePostAPIView(APIView):
    """
    Представление для лайка/дизлайка поста по его ID.
    Если пользователь уже поставил лайк — убирает его. Иначе — добавляет.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """
        Лайкнуть или убрать лайк с поста по его ID.
        """
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"message": "Unliked"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"message": "Liked"}, status=status.HTTP_200_OK)
