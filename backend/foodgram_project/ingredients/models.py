from django.db import models


class MeasurementUnit(models.Model):
    '''Размерность игридиентов.'''

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название',
        unique=True,
    )

    class Meta:
        verbose_name = 'Размерность'
        verbose_name_plural = 'Размерности'
        ordering = ('name',)

    def __str__(self):
        return f'Размерность: {self.name}'


class Ingredient(models.Model):
    '''Модель для ингредиентов.'''

    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Название',
    )
    measurement_unit = models.ForeignKey(
        MeasurementUnit,
        on_delete=models.CASCADE,
        null=True,
        related_name='ingredients',
        verbose_name='Размерность',
        help_text='Размерность',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_for_ingredient'
            ),
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            models.CheckConstraint(
                check=models.Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'Ингредиент: {self.name}'
