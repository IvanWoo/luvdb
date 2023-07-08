from django import template
from django.db.models import Q

register = template.Library()


@register.filter
def is_following(user, other_user):
    return user.following.filter(followed=other_user).exists()


@register.filter
def is_blocking(user, other_user):
    return user.blocking.filter(blocked=other_user).exists()
