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
