from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponsePermanentRedirect

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View, DeleteView, FormView
from .filters import PostFilter, CommentFilter
from .forms import PostForm, CommentForm, CommentAddForm
from .models import Post, Comment
from .utils import DataMixin


class PostListView(ListView):
    model = Post
    template_name = 'bboard/post_list.html'  # post_list.html'
    context_object_name = 'posts'
    ordering = ['-datetime_creation']
    form = PostForm
    paginate_by = 4

    def get_queryset(self):
        queryset = PostFilter(self.request.GET, super().get_queryset()).qs
        # фильтрация queryset-ом
        return queryset

    def get_context_data(self, **kwargs):  # забираем отфильтрованные
        # объекты переопределяя метод get_context_data у
        # наследуемого класса - полиморфизм
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DataMixin, DetailView):  # DataMixin
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'bboard/detail.html'
    queryset = Post.objects.all()
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = CommentAddForm
        return context

class CommentFormView(FormView):
    form_class = CommentForm
    success_url = '/'  # '/'

    def form_valid(self, form, *args, **kwargs):
        form.instanse.post = self.kwargs.get('pk')
        form.instance.post_id = self.kwargs['post_pk']
        form.instance.user = self.request.user
        self.object = form.save()
        return super(CommentFormView, self).form_valid(form)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'bboard/post_create.html'
    form_class = PostForm
    # permission_required = ('bboard.create',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = User.objects.get(id=self.request.user.id)
        post.save()
        return redirect('/')


class PostEdit(DataMixin, UpdateView):  # DataMixin, IsAuthorMixin
    model = Post
    form_class = PostForm
    template_name = 'bboard/post_edit.html'
    context_object_name = 'post'
    success_url = '/'

    # get_object вместо queryset для получения инфо об obj редактирования
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена!')
        return super().form_valid(form)


class PostDelete(DeleteView):  # PermissionRequiredMixin
    template_name = 'bboard/delete.html'
    queryset = Post.objects.all()
    success_url = '/'
    permission_required = ('bboard.delete',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class CommentSearchView(DataMixin, ListView):  # DataMixin
    """replies for using in account"""
    model = Comment
    template_name = 'bboard/comments.html'  # v 'bboard/my_comments.html' v 'bboard/comments.html'
    context_object_name = 'comments'  # 'finded_comments'
    ordering = '-datetime_creation'
    # permission_required = ('comment')
    paginate_by = 5

    def get_queryset(self):
        queryset = CommentFilter(self.request.GET, super().get_queryset()).qs  # фильтрация queryset-ом
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        # вписываем наш фильтр в контекст
        return context

    # def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data
    #     # у наследуемого класса - полиморфизм
    #     context = super().get_context_data(**kwargs)
    #     user_id = self.request.user.id
    #     context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
    #     context['new_comment'] = Comment.objects.filter(post__author=user_id).filter(rejected=False).filter(accepted=False)
    #     context['del_comment'] = Comment.objects.filter(post__author=user_id).filter(rejected=True)
    #     context['add_comment'] = Comment.objects.filter(post__author=user_id).filter(accepted=True)
    #     return context


class CommentView(DetailView):  #DataMixin
    """detail of reply"""
    model = Comment
    template_name = 'bboard/comment.html'
    context_object_name = 'comment'
    paginate_by = 4


class AddComment(DataMixin, CreateView):   # LoginRequiredMixin, DataMixin
    """ for add reply at details"""
    model = Comment
    form_class = CommentAddForm
    context_object_name = 'comment'
    ordering = ['datetime_creation']
    template_name = 'bboard/add_comment.html'
    # permission_required = ('bboard.add_comment')
    success_url = '/comm'


class CommentAccepted(DataMixin, View):  # IsAuthorMixin
    def get(self, request, *args, **kwargs):
        com_pk = kwargs['com_pk']

        comment = Comment.objects.get(pk=com_pk)
        comment.accepted = True
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentRejected(DataMixin, View):  # IsAuthorMixin
    def get(self, request, *args, **kwargs):
        com_pk = kwargs['com_pk']

        comment = Comment.objects.get(pk=com_pk)
        comment.accepted = False
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


def comment_del(request, com_pk):
    comment = get_object_or_404(Comment, pk=com_pk)
    comment.delete()
    return redirect('bboard:comments')


def change_status(request, com_pk):
    """Change status of comments"""
    comment = get_object_or_404(Comment, pk=com_pk)
    comment.accepted = False if comment.accepted else True
    comment.save()
    return redirect('bboard:comments')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
