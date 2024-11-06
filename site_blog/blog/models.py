from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.admin import display


# post_id, pk


# Create your models here.

# blog_category


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # отображение названия таблицы в единственном числе
        verbose_name_plural = 'Категории'  # отображение названия таблицы во множественном числе


# media/

class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero/slider/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото слайдера'
        verbose_name_plural = 'Фото слайдера'


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name='Вопрос', unique=True)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


# admin
# post-1 admin -> null
# post-2 admin -> null
# post-3 admin -> null
# admin deleted

class Post(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    views = models.IntegerField(verbose_name='Кол-во просмотров', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    preview = models.ImageField(upload_to='posts/%Y-%m-%d/', verbose_name='Фото', blank=True, null=True)

    def __str__(self):
        return f'{self.name}: {self.created_at}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.pk})

    @display()
    def get_photos_for_admin(self):
        photos = self.gallery.all()
        photos_div_start = '<div class="d-flex">'
        photos_div_end = '</div>'

        photos_imgs = ''

        for photo in photos:
            photos_imgs += f'<img style="margin-right: 10px;" src="{photo.image.url}" width="50"  height="50" />'

        result = photos_div_start + photos_imgs + photos_div_end
        return mark_safe(result)


    def get_preview(self):
        if self.preview:
            return self.preview.url
        return False

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


# models.SET_NULL
# models.PROTECT
# post_1.gallery.all()

# id
#    gallery


def post_gallery_image_path(instance, filename):
    return f'post-{instance.post.id}/gallery/{filename}'


class PostGallery(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, verbose_name='Пост', related_name='gallery')
    image = models.ImageField(upload_to=post_gallery_image_path, verbose_name='Фото', blank=True, null=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пользователь')
    body = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.post}'

    class Meta:
        verbose_name='Комментарий'
        verbose_name_plural = 'Комментарии'


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=150)



class Like(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')

# Если нет значения, то добавляется значение Null
# Модель для задач

# ToDo
# title CharField
# description необязательным
# user
# created_at
# finish_date
# is_finished = False


# добавленную модель, зарегистрировать в админ панели
# добавить 3-4 задачи


# сделать функцию для отображения страницы
# сделать отдельную страницу, в которой отображаются задачи
# сделать отдельный столбец с выполненными задачами
# сделать отдельный столбец с невыполненными задачами

# сделать ссылку для перехода на страницу с задачами
