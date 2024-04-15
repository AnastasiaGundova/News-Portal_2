
# Register your models here.
from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment
from modeltranslation.admin import TranslationAdmin


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating')
    list_filter = ('created_at', 'title', 'rating')
    search_fields = ('title', 'category')


class TransCategoryAdmin(PostAdmin, TranslationAdmin):
    model = Category


class TransPostAdmin(PostAdmin, TranslationAdmin):
    model = Post


admin.site.register(Category, TransCategoryAdmin)
admin.site.register(Author)
admin.site.register(Post, TransPostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)


