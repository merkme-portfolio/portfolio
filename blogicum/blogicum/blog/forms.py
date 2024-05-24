from django import forms
from django.contrib.auth import get_user_model
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма на основе модели Post. Отображаем все поля, кроме автора."""

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    """Форма на основе модели Comment. Отображаем только поле текст."""

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    """Форма на основе модели User. Даем возможность отредактировать данные."""

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff'
        )
