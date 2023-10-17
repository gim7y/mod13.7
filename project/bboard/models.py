from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')

    CAT = {
        ('Tanks', 'Танки'),
        ('Heals', 'Хилы'),
        ('Damage dealers', 'ДД'),
        ('Dealers', 'Торговцы'),
        ('Guild masters', 'Гилдмастеры'),
        ('Quest givers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potion masters', 'Зельевары'),
        ('Spell masters', 'Мастера заклинаний')
    }

    cat = models.CharField(max_length=22, choices=CAT, verbose_name='Категория')
    title = models.CharField(max_length=256, verbose_name='Заголовок', blank=True)
    content = RichTextUploadingField(default='', verbose_name='Текст поста')
    datetime_creation = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', default=None, verbose_name='Картинка поста', blank=True)
    time_update = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    is_published = models.BooleanField(default=True)

    # @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def preview(self):
        return self.content[0:123] + '...'

    def __str__(self):
        return f'№:{self.pk}, текст: {self.title} -{self.content[0:123]}'

    def get_absolute_url(self):
        return f'/{self.pk}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='К посту')
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE, verbose_name='Автор отклика')
    text = models.TextField(verbose_name='Комментарий')
    datetime_creation = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, blank=True, verbose_name='Коммент принят')
    
    def get_absolute_url(self):
        return reverse('comment', kwargs={'pk': self.pk})

    def __str__(self):
        return f'No{self.pk} - {self.author}--{self.text}'

    def is_accepted(self):
        if True:
            self.accepted = True
        else:
            self.accepted = False   # self.rejected = True
        return self.instance
