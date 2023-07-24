from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """Модель поста"""
    title = models.CharField(max_length=100, verbose_name='Заголовок', db_index=True)
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    update_at = models.DateTimeField(auto_now=True, verbose_name='Обнавлено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    is_publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at", "title"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Category(models.Model):
    """Модель категории для поста"""
    title = models.CharField(max_length=100, db_index=True, verbose_name="Название", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
