from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import ProfileAPIView, RegisterAPIView, LoginAPIView
from posts.views import PostListCreateAPIView, LikePostAPIView


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # Swagger UI

    path('swagger/docs/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    path('api/v1/register/', RegisterAPIView.as_view(), name='register'),
    path('api/v1/login/', LoginAPIView.as_view(), name='login'),
    path('api/v1/profile/', ProfileAPIView.as_view()),    # Профиль (нужен токен)
    path('api/v1/posts/', PostListCreateAPIView.as_view()),  # Лента + создать пост
    path('api/v1/posts/<int:post_id>/like/', LikePostAPIView.as_view(), name='like-post'), #лайк и анлайк
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
