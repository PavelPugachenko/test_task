from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r"^\+?7?\d{10,11}$", "Неверный формат номера")],
    )
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Решение конфликта с auth.User
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="posts_user_set",
        blank=True,
        help_text="Группы, к которым принадлежит пользователь.",
        verbose_name="Группы",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="posts_user_set",
        blank=True,
        help_text="Специфические разрешения для этого пользователя.",
        verbose_name="Разрешения",
    )

    def __str__(self):
        return self.username

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.post.title}"
