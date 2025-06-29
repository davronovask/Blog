
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    search_fields = ('content', 'author__email')
    list_filter = ('created_at', 'profession')
    readonly_fields = ('created_at',)
