from django.contrib import admin
from .models import CustomUser, Genre, Category, Title, Review, Comment


class TitleAdmin (admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'description', 'year')
    search_fields = ('description',)
    list_editable = ('category',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


class CategoryAdmin (admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin (admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    empty_value_display = '-пусто-'


class CommentAdmin (admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')
    empty_value_display = '-пусто-'


class ReviewAdmin (admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


class CustomUserAdmin (admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'role', 'bio', 'first_name', 'last_name'
    )
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
