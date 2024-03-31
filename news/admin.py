
# Register your models here.
from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating')
    list_filter = ('created_at', 'title', 'rating')
    search_fields = ('title', 'category')


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
