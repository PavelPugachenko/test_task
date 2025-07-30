from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@mail.ru",
            password="12345678",
            birth_date="2000-01-01"
        )

    def test_user_age(self):
        self.assertEqual(self.user.age, 24)  # зависит от года

    def test_post_creation(self):
        post = Post.objects.create(
            title="Тест",
            content="Содержание",
            author=self.user
        )
        self.assertEqual(post.author, self.user)


from django.test import TestCase

# Create your tests here.
