from django.urls import path
from .views import PostListView, PostDetail, PostEdit, PostCreate, PostDelete, CommentSearchView, CommentView, \
    AddComment, CommentFormView, comment_del, change_status

app_name = 'bboard'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='detail'),
    path('commform/', CommentFormView.as_view(), name='comment_form'),
    path('create/', PostCreate.as_view(), name='create'),
    path('edit/<int:pk>/', PostEdit.as_view(), name='edit'),
    path('delete/<int:pk>/', PostDelete.as_view(), name='delete'),
    path('comm/', CommentSearchView.as_view(), name='comments'),
    path('comment/<int:pk>/', CommentView.as_view(), name='comment'),
    path('add_comm/', AddComment.as_view(), name='add_comment'),  # ad-comment
    path('comm/delete/<int:com_pk>/', comment_del, name='del_comm'),
    path('change/<int:com_pk>/', change_status, name='change_status')
]
