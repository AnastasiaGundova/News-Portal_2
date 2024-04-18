from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .tasks import post_notification, weekly_newsletter

from django.core.cache import cache

from django.utils import timezone

from django.shortcuts import redirect

import pytz

from django.utils.translation import gettext as _

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import *
from .models import *


class NewsViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type='N')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticlesViewset(viewsets.ModelViewSet):
    queryset = Post.objects.filter(type='A')
    serializer_class = ArticlesSerializer


class CategoryViewest(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AuthorViewest(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class Index(View):
    def get(self, request):
        models = Post.objects.all(), Category.objects.all()
        context = {
            'models': models,
        }
        return HttpResponse(render(request, 'index.html', context))


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('post_list')


class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostSearch(ListView):
    model = Post
    ordering = 'title'
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    success_url = '/home/news'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/home/articles/create/':
            post.type = 'A'
        elif self.request.path == '/home/news/create/':
            post.type = 'N'

        post.save()
        post_notification.delay(post.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/home/news/'
    permission_required = ('news.change_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/home/news/'
    permission_required = ('news.delete_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'prodected_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class CategoryListView(NewsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на категорию'

    return render(request, 'subscribe.html', {category: category, 'message': message})
