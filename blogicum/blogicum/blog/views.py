"""Модуль views приложения blog."""
from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm, UserForm

# Количество постов на главной странице
POST_SHOW_ON_PAGE = 10


def profile(request, username):
    """Профиль пользователя."""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, POST_SHOW_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class UserEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


def post_detail(request, pk):
    """Возвращаем всю информацию по конкретному посту."""
    template_detail = 'blog/detail.html'
    post = get_object_or_404(Post, pk=pk)
    if not request.user.is_authenticated or request.user != post.author:
        post = get_object_or_404(
            Post,
            pk=pk,
            pub_date__date__lte=datetime.now(),
            is_published=True,
            category__is_published=True
        )
    context = {
        'post': post
    }
    context['form'] = CommentForm()
    context['comments'] = post.comments.all()
    return render(request, template_detail, context)


def category_posts(request, category_slug):
    """
    Возвращаем список постов по категории.

    Посты отсортированы в обратном порядке.
    """
    template_category = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        pub_date__date__lte=datetime.now(),
        is_published=True,
        category__slug=category_slug
    )
    paginator = Paginator(posts, POST_SHOW_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category
    }
    return render(request, template_category, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class AuthorTest(UserPassesTestMixin):
    """Проверяем, совпадает ли пользователь с автором запроса."""

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', pk=post.pk)


class PostUpdateView(LoginRequiredMixin, AuthorTest, UpdateView):
    """Редактирование поста. Наследуется от кастомного класса AuthorTest."""

    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, AuthorTest, DeleteView):
    """Удаление поста. Наследуется от кастомного класса AuthorTest."""

    model = Post
    success_url = reverse_lazy('blog:index')


class IndexView(ListView):
    """Главная страница."""

    model = Post
    paginate_by = POST_SHOW_ON_PAGE
    queryset = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        pub_date__date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )


@login_required
def add_comment(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', pk=post_id)
    return render(request, 'blog/comment.html')


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        raise Http404
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_id)
    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        raise Http404
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', pk=post_id)
    context = {
        'comment': comment,
    }
    return render(request, 'blog/comment.html', context)
