from django.db import models
from django.utils import timezone

class BlogPost(models.Model):
    title = models.CharField(max_length=255)  # Заголовок статьи
    content = models.TextField()  # Содержимое статьи
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Изображение
    views = models.PositiveIntegerField(default=0)  # Количество просмотров
    created_at = models.DateTimeField(default=timezone.now)  # Дата публикации

    def __str__(self):
        return self.title
