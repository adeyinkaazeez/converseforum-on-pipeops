from django.conf import settings
from django.urls import re_path
if getattr(settings, 'POSTMAN_I18N_URLS', False):
    from django.utils.translation import pgettext_lazy
else:
    def pgettext_lazy(context: str, message: str): return message

from .api_views import AjaxUnreadCountView

app_name = 'api'
urlpatterns = [
    re_path(pgettext_lazy('postman_url', r'^unread-count/$'), AjaxUnreadCountView.as_view(), name='unread-count'),
]
