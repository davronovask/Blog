from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from users.views import AuthAPIView, ProfileAPIView
from posts.views import PostListCreateAPIView, LikePostAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Документация API для блог-сайта",
        default_version='v1',
        description=(
            "API для блог-сайта включает:\n"
            "- Регистрацию и логин на одном эндпоинте\n"
            "- Просмотр профиля (по токену)\n"
            "- Получение ленты и создание публикаций\n"
            "- Лайки/анлайки публикаций\n"
            "- Поиск постов по заголовку (title)\n"
        ),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # Swagger UI

    path('swagger/docs/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('api/v1/users/', AuthAPIView.as_view()),         # Регистрация + логин
    path('api/v1/profile/', ProfileAPIView.as_view()),    # Профиль (нужен токен)
    path('api/v1/posts/', PostListCreateAPIView.as_view()),  # Лента + создать пост
    path('api/v1/posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='like-post'), #лайк и анлайк
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
