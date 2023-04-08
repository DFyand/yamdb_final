from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
import datetime


class CustomUser(AbstractUser):
    """Модель кастомного пользователя с ролью и биографией"""
    class Role(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    role = models.CharField(
        _('role'),
        choices=Role.choices,
        default=Role.USER,
        max_length=20,
    )
    bio = models.TextField(
        _('bio'),
        blank=True,
        null=True,
    )
    confirmation_code = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанра"""
    name = models.CharField(_('name'), max_length=256)
    slug = models.SlugField(_('slug'), unique=True, max_length=50)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(_('name'), max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True,
    )
    description = models.TextField(
        _('description'), blank=True, null=True,
    )
    year = models.IntegerField(
        _('year'),
        validators=[
            MinValueValidator(
                1800,
                message='Нельзя добавить произведение раньше 1800 года'),
            MaxValueValidator(
                datetime.datetime.now().year,
                message='Год произведения не может быть больше текущего года'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва на произведение"""
    text = models.TextField(_('text'), )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(_('pub_date'), auto_now_add=True)
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='Оценка не может быть меньше 1'),
            MaxValueValidator(10, message='Оценка не может быть больше 10')
        ]
    )

    class Meta:
        ordering = ['-id']
        unique_together = ['title', 'author']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария на отзыв"""
    text = models.TextField(_('text'),)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(_('pub_date'), auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
