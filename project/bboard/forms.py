from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, CharField, Form, Textarea, TextInput

from .models import Post, Comment


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # self.fields['cat'] = forms.ModelChoiceField(label='Пост', empty_label='ghj')

    class Meta:
        model = Post
        fields = ('title', 'cat', 'content', 'image',)
        widgets = {'title': forms.TextInput(attrs={'size': '80'}),
                   'image': forms.FileInput(attrs={'size': '40'}),
                   }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = 'Отклик'


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", "author", "post")

    def __init__(self, *args, **kwargs):
        super(CommentAddForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = 'Новый отклик'
