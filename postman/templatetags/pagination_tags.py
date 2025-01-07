"""
A mock of dj-pagination's pagination_tags.py that does nothing.

'pagination_tags' is a name from the dj-pagination application.
For convenience, the design of the default template set is done with the use of that application.
This mock will avoid failures in template rendering if the real application is not installed,
as it may be the case for the test suite run in a minimal configuration.

To deactivate this mock and use the real implementation, just make sure that 'dj_pagination' is declared
before 'postman' in the INSTALLED_APPS setting.
"""
from typing import Any

from django.template import Node, Library

register = Library()


class AutoPaginateNode(Node):
    def render(self, context: Any):
        return ''


@register.tag
def autopaginate(parser: Any, token: Any):
    return AutoPaginateNode()


class PaginateNode(Node):
    def render(self, context: Any):
        return ''


@register.tag
def paginate(parser: Any, token: Any):
    return PaginateNode()
