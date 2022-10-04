from django.contrib import admin

from .models import Tag, Ingredient, Recipe, AmountIngredient


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'color',
        'slug'
    )
    search_fields = ('title',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'unit'
    )
    search_fields = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
        'cooking_time'
    )
    search_fields = (
        'title',
        'author'
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredient)
