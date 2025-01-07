from datetime import timedelta
from typing import Any, TYPE_CHECKING, cast

from django.core.management.base import BaseCommand
from django.db.models import Max, Count, F, Q
from django.utils.timezone import now

from postman.models import Message

if TYPE_CHECKING:
    from django.core.management.base import CommandParser

ARGUMENT_ARGS = ('-d', '--days')
ARGUMENT_KWARGS: dict[str, Any] = {'default': 30 }


class Command(BaseCommand):
    help = """Can be run as a cron job or directly to clean out old data from the database:
  Messages or conversations marked as deleted by both sender and recipient,
  more than a minimal number of days ago."""
    def add_arguments(self, parser: 'CommandParser'):
        parser.add_argument(*ARGUMENT_ARGS, type=int,
            help='The minimal number of days a message is kept marked as deleted, '
                 'before to be considered for real deletion [default: %(default)s]',
            **ARGUMENT_KWARGS)

    # no more NoArgsCommand and handle_noargs with Dj >= 1.8
    def handle(self, *args: Any, **options: Any):
        verbose = int(cast(Any, options.get('verbosity')))  # discard unexpected None
        days = cast(int, options.get('days'))  # discard unexpected None
        date = now() - timedelta(days=days)
        if verbose >= 1:
            self.stdout.write("Erase messages and conversations marked as deleted before {0}".format(date))
        # for a conversation to be candidate, all messages must satisfy the criteria
        tpks = Message.objects.filter(thread__isnull=False).values('thread').annotate(
                cnt=Count('pk'),
                s_max=Max('sender_deleted_at'),    s_cnt=Count('sender_deleted_at'),
                r_max=Max('recipient_deleted_at'), r_cnt=Count('recipient_deleted_at')
            ).order_by().filter(
                s_cnt=F('cnt'), r_cnt=F('cnt'), s_max__lte=date, r_max__lte=date
            ).values_list('thread', flat=True)
        Message.objects.filter(
            Q(thread__in=tpks) |
            Q(thread__isnull=True, sender_deleted_at__lte=date, recipient_deleted_at__lte=date)
        ).delete()
