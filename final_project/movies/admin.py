from django.contrib import admin
from .models import Category, Movie, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'year', 'trailer', 'created', 'updated']
    list_filter = ['name', 'year', 'created', 'updated']
    list_editable = ['description', 'year', 'trailer']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Movie, MovieAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'movie', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
