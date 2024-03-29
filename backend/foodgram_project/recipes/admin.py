from django.contrib import admin
from recipes.models import (Recipe, RecipeIngredientAmount, RecipeTag,
                            UserFavoriteRecipe, UserShoppingCart)


class TagInline(admin.TabularInline):
    '''Класс TagInline.'''

    model = RecipeTag
    extra = 3
    min_num = 1


class IngredientInline(admin.TabularInline):
    '''Класс IngredientInline.'''

    model = RecipeIngredientAmount
    extra = 3
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    '''Класс RecipeAdmin.'''

    inlines = (
        TagInline,
        IngredientInline,
    )
    list_display = (
        'pk',
        'author',
        'name',
        'text',
        'cooking_time',
        'added_in_favorites',
        'image',
    )
    list_editable = (
        'author',
        'name',
        'text',
        'cooking_time',
        'image',
    )
    list_filter = ('tags__name', 'author__username',)
    readonly_fields = ('added_in_favorites',)

    def added_in_favorites(self, obj):
        return obj.in_favorite.count()

    added_in_favorites.short_description = 'Добавлено в Избранные'


class RecipeTagAdmin(admin.ModelAdmin):
    '''Класс RecipeTagAdmin.'''

    list_display = (
        'pk',
        'recipe',
        'tag',
    )
    list_editable = (
        'recipe',
        'tag',
    )
    list_filter = ('tag', )


class RecipeIngredientAmountAdmin(admin.ModelAdmin):
    '''RecipeIngredientAmountAdmin.'''

    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    list_editable = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'recipe__name',
        'recipe__author__email',
        'recipe__author__username',
    )
    raw_id_fields = ('ingredient', 'recipe')


class UserFavoriteRecipeAdmin(admin.ModelAdmin):
    '''Класс UserFavoriteRecipeAdmin.'''

    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = (
        'user',
        'recipe',
    )
    search_fields = (
        'recipe__name',
        'recipe__author__email',
        'recipe__author__username',
    )


class UserShoppingCartAdmin(admin.ModelAdmin):
    '''Класс UserShoppingCartAdmin.'''

    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_editable = (
        'user',
        'recipe',
    )
    search_fields = (
        'recipe__name',
        'recipe__author__email',
        'recipe__author__username',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredientAmount, RecipeIngredientAmountAdmin)
admin.site.register(UserFavoriteRecipe, UserFavoriteRecipeAdmin)
admin.site.register(UserShoppingCart, UserShoppingCartAdmin)
