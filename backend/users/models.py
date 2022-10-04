from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Своя настройка модели User."""

    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Юзернейм пользователя',
        help_text='Введите логин'
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        help_text='Введите свое имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        help_text='Введите свою фамилию'
    )
    password = models.CharField(
        max_length=10,
        help_text='Введите пароль'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите свой email'
    )
    subscribe = models.ManyToManyField(
        verbose_name='Подписка',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
