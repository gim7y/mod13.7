from django_filters import FilterSet
from .models import Post, Comment


# создаём фильтр
class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = ('cat', 'author', 'time_update', 'content')


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ('post', 'author', 'text', 'accepted')
