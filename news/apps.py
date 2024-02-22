from django.apps import AppConfig
import redis


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals


red = redis.Redis(
    host='redis-17793.c253.us-central1-1.gce.cloud.redislabs.com',
    port=17793,
    password='wgX10rxHoy4kB687xoQgMANyIxISsxIL'
)

