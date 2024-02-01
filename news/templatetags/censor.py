from django import template

register = template.Library()

censor_words = ['редиска', 'помидор']


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError()
    for word in value.split():
        word = word.lower()
        if word in censor_words:
            value = value.replace(word[1:], '*' * len(word[1:]))
    return value


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
