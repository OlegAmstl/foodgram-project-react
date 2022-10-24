from django.db import models


class Tag(models.Model):
    '''Класс для тегов к рецепту.'''

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название',
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX',
        help_text='Цвет в HEX',
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Уникальный слаг',
        help_text='Уникальный слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)
        constraints = (
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(color__length__gt=0),
                name='\n%(app_label)s_%(class)s_color is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(slug__length__gt=0),
                name='\n%(app_label)s_%(class)s_slug is empty\n',
            ),
        )

    def __str__(self):
        return f'Tag: {self.slug}-{self.color}'
