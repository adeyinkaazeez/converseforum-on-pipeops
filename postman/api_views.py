from functools import wraps
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Callable, cast

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from .models import Message

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from django.http.request import HttpRequest
    _ViewBase = View
else:
    _ViewBase = object

never_cache_m = method_decorator(never_cache)


class HttpResponseUnauthorized(HttpResponse):
    status_code = HTTPStatus.UNAUTHORIZED


def auth_required(func: Callable[['HttpRequest', Any, Any], HttpResponse]):
    @wraps(func)
    def wrapper(request: 'HttpRequest', *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return HttpResponseUnauthorized()
    return wrapper
auth_required_m = method_decorator(auth_required)


class AjaxMixin(_ViewBase):
    """Common code to Ajax calls."""

    @never_cache_m
    @auth_required_m
    def dispatch(self, *args: Any, **kwargs: Any):
        return super().dispatch(*args, **kwargs)


class AjaxUnreadCountView(AjaxMixin, View):
    """Return the number of unread messages for a user."""
    http_method_names = ['get']

    def get(self, request: 'HttpRequest', *args: Any, **kwargs: Any):
        return JsonResponse({'unread_count': Message.objects.inbox_unread_count(cast('AbstractBaseUser', request.user))})
