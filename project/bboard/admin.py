from django.contrib import admin

from .forms import PostForm
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'time_update', 'cat', 'content')
    list_filter = ('datetime_creation', 'cat')
    search_fields = ('author', 'content', 'cat')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_id', 'datetime_creation', 'text', 'accepted')
    list_filter = ('datetime_creation', 'author', 'accepted')
    search_fields = ('post', 'author', 'text', 'accepted')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
