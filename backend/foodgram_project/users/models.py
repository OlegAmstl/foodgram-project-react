from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''Класс User вместо стандартного.'''

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Фамилия',
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        help_text='Уникальный юзернейм',
        max_length=150,
        unique=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class SubscribeUser(models.Model):
    '''Класс для отображения подписок пользователя.'''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='subscribes',
        verbose_name='Подписки пользователя',
        help_text='Подписки пользователя'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='subscribe',
        verbose_name='Автор',
        help_text='Автор, на которого подписаны'
    )

    class Meta:
        verbose_name = 'Подписка пользователя'
        verbose_name_plural = 'Подписки пользователя'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~(models.Q(user=models.F('author'))),
                name='user_is_not_author'
            ),
        )

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.author.username}'
