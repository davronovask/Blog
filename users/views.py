from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import AuthSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class AuthAPIView(APIView):

    """
    Регистрация и логин пользователя через один эндпоинт.

    Метод POST:
    - Если пользователь с таким email уже существует и пароль верный — возвращается токен (вход).
    - Если пользователь не найден — создаётся новый пользователь и выдается токен (регистрация).
    """
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({
                'email': user.email,
                'token': token.key
            }, status=201)

        if not user.check_password(password):
            return Response({'error': 'Неверный пароль'}, status=400)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'email': user.email,
            'token': token.key
        }, status=200)


class ProfileAPIView(APIView):
    """
    Получение профиля авторизованного пользователя.

    Метод GET:
    - Требуется авторизация по токену.
    - Возвращает email текущего пользователя.

    Заголовки:
    - Authorization: Token <токен>

    Ответ:
    - email: email текущего пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"email": request.user.email})
