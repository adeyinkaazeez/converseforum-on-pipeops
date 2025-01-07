from typing import TYPE_CHECKING, Any, cast

from django.utils.functional import SimpleLazyObject

from .models import Message

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from django.http.request import HttpRequest


def inbox(request: 'HttpRequest') -> dict[str, Any]:
    """Provide the count of unread messages for an authenticated user."""
    if request.user.is_authenticated:
        return {'postman_unread_count': SimpleLazyObject(lambda: Message.objects.inbox_unread_count(cast('AbstractBaseUser', request.user)))}
    else:
        return {}
