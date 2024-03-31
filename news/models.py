from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

article = 'A'
news = 'N'

POST_OPTIONS = [
    (news, "news"),
    (article, "article")
]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        comment_rating = 0
        posts_comments_rating = 0
        posts = Post.objects.filter(author=self)
        comments = Comment.objects.filter(user=self.user)
        posts_comments = Comment.objects.filter(post__author=self)

        for post in posts:
            post_rating += post.rating
        for comment in comments:
            comment_rating += comment.rating
        for p_comment in posts_comments:
            posts_comments_rating += p_comment.rating

        self.rating = (post_rating * 3) + comment_rating + posts_comments_rating

        self.save()


class Category(models.Model):
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=POST_OPTIONS, default="news")

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:125].strip() + "..."

    def __str__(self):
        return f'id - {self.pk}: {self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
