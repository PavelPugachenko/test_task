from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re


def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Пароль должен быть не менее 8 символов.")
    if not re.search(r'\d', value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


def validate_email_domain(value):
    validate_email(value)
    allowed_domains = ['mail.ru', 'yandex.ru']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f"Разрешены только домены: {', '.join(allowed_domains)}.")


def validate_title_forbidden_words(value):
    forbidden = ['ерунда', 'глупость', 'чепуха']
    if any(word in value.lower() for word in forbidden):
        raise ValidationError(f"Заголовок не должен содержать слова: {', '.join(forbidden)}.")


def validate_author_age(instance):
    if instance.author.age is None:
        raise ValidationError("Не указана дата рождения автора.")
    if instance.author.age < 18:
        raise ValidationError("Автор должен быть старше 18 лет.")