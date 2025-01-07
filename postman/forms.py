"""
You may define your own custom forms, based or inspired by the following ones.

Examples of customization:
    recipients = CommaSeparatedUserField(label=("Recipients", "Recipient"),
        min=2,
        max=5,
        user_filter=my_user_filter,
        channel='my_channel',
    )
    can_overwrite_limits = False
    exchange_filter = staticmethod(my_exchange_filter)

"""
from typing import Any, TYPE_CHECKING

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.utils.translation import gettext, gettext_lazy as _

from .fields import CommaSeparatedUserField
from .models import Message, get_user_name
from .utils import WRAP_WIDTH
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

    from .models import AutoModeratorsAlias


class BaseWriteForm(forms.ModelForm):
    """The base class for other forms."""
    class Meta:
        model = Message
        fields = ('body',)
        widgets = {
          'body' : forms.widgets.Textarea(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Send message',
                                                             'cols': 300, 'rows': 5})
                  }

    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args: Any, **kwargs: Any):
        sender = kwargs.pop('sender', None)
        exchange_filter = kwargs.pop('exchange_filter', None)
        user_filter = kwargs.pop('user_filter', None)
        max = kwargs.pop('max', None)
        channel = kwargs.pop('channel', None)
        self.site = kwargs.pop('site', None)
        super().__init__(*args, **kwargs)

        self.instance.sender = sender if (sender and sender.is_authenticated) else None
        if exchange_filter:
            self.exchange_filter = exchange_filter
        if 'recipients' in self.fields:
            if user_filter and hasattr(self.fields['recipients'], 'user_filter'):
                self.fields['recipients'].user_filter = user_filter

            if getattr(settings, 'POSTMAN_DISALLOW_MULTIRECIPIENTS', False):
                max = 1
            if max is not None and hasattr(self.fields['recipients'], 'set_max') \
            and getattr(self, 'can_overwrite_limits', True):
                self.fields['recipients'].set_max(max)

            if channel and hasattr(self.fields['recipients'], 'set_arg'):
                self.fields['recipients'].set_arg(channel)

    error_messages = {
        'filtered': _("Writing to some users is not possible: {users}."),
        'filtered_user': _("{username}"),
        'filtered_user_with_reason': _("{username} ({reason})"),
    }
    def clean_recipients(self):
        """Check no filter prohibits the exchange."""
        recipients = self.cleaned_data['recipients']
        exchange_filter = getattr(self, 'exchange_filter', None)
        if exchange_filter:
            errors: list[str] = []
            filtered_names: list[str] = []
            recipients_list = recipients[:]
            for u in recipients_list:
                try:
                    reason = exchange_filter(self.instance.sender, u, recipients_list)
                    if reason is not None:
                        recipients.remove(u)
                        filtered_names.append(
                            self.error_messages[
                                'filtered_user_with_reason' if reason else 'filtered_user'
                            ].format(username=get_user_name(u), reason=reason)
                        )
                except forms.ValidationError as e:
                    recipients.remove(u)
                    errors.extend(e.messages)
            if filtered_names:
                errors.append(self.error_messages['filtered'].format(users=', '.join(filtered_names)))
            if errors:
                raise forms.ValidationError(errors)
        return recipients

    @atomic
    def _save(
        self,
        recipient: 'AbstractBaseUser | None' = None,
        parent: 'Message | None' = None,
        auto_moderators: 'AutoModeratorsAlias' = []
    ):
        """
        Save as many messages as there are recipients.

        Additional actions:
        - If it's a reply, build a conversation
        - Call auto-moderators
        - Notify parties if needed

        Return False if one of the messages is rejected.

        """
        recipients = self.cleaned_data.get('recipients', [])
        if parent and not parent.thread_id:  # at the very first reply, make it a conversation
            parent.thread = parent
            parent.save()
            # but delay the setting of parent.replied_at to the moderation step
        if parent:
            self.instance.parent = parent
            self.instance.thread_id = parent.thread_id
        initial_moderation = self.instance.get_moderation()
        initial_dates = self.instance.get_dates()
        initial_status = self.instance.moderation_status
        if recipient:
            if isinstance(recipient, get_user_model()) and recipient in recipients:
                recipients.remove(recipient)
            recipients.insert(0, recipient)
        is_successful = True
        for r in recipients:
            if isinstance(r, get_user_model()):
                self.instance.recipient = r
            else:
                self.instance.recipient = None
                self.instance.email = r
            self.instance.pk = None  # force_insert=True is not accessible from here
            self.instance.auto_moderate(auto_moderators)
            self.instance.clean_moderation(initial_status)
            self.instance.clean_for_visitor()
            super().save()
            if self.instance.is_rejected():
                is_successful = False
            self.instance.update_parent(initial_status)
            self.instance.notify_users(initial_status, self.site)
            # some resets for next reuse
            if not isinstance(r, get_user_model()):
                self.instance.email = ''
            self.instance.set_moderation(*initial_moderation)
            self.instance.set_dates(*initial_dates)
        return is_successful

    def save(self, *args: Any, **kwargs: Any):
        return self._save(*args, **kwargs)


class WriteForm(BaseWriteForm):
    """The form for an authenticated user, to compose a message."""
    # specify help_text only to avoid the possible default 'Enter text to search.' of ajax_select v1.2.5
    recipients = CommaSeparatedUserField(label=(_("Recipients"), _("Recipient")), help_text=" ", widget=forms.TextInput(attrs={'placeholder':'This author username '}))
    

    class Meta(BaseWriteForm.Meta):
        fields = ('recipients', 'subject', 'body')
        #recipients = forms.CharField(required=True, 
                              # widget=forms.TextInput(attrs={'class': 'bg-gray-50 border-gray-300 text-gray-900 sm:text-sm lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-grey-400 dark-white', 'placeholder':'Input this author username ',
                                                                # 'rows':2}))
        
        
 

class AnonymousWriteForm(BaseWriteForm):
    """The form for an anonymous user, to compose a message."""
    # The 'max' customization should not be permitted here.
    # The features available to anonymous users should be kept to the strict minimum.
    can_overwrite_limits = False

    email = forms.EmailField(label=_("Email"))
    recipients = CommaSeparatedUserField(label=(_("Recipients"), _("Recipient")), help_text='', max=1)  # one recipient is enough

    class Meta(BaseWriteForm.Meta):
        fields = ('email', 'recipients', 'subject', 'body')


class BaseReplyForm(BaseWriteForm):
    """The base class for a reply to a message."""
    def __init__(self, *args: Any, **kwargs: Any):
        recipient: 'AbstractBaseUser | None' = kwargs.pop('recipient', None)
        super().__init__(*args, **kwargs)
        self.recipient = recipient

    def clean(self):
        """Check that the recipient is correctly initialized and no filter prohibits the exchange."""
        if not self.recipient:
            raise forms.ValidationError(gettext("Undefined recipient."))

        exchange_filter = getattr(self, 'exchange_filter', None)
        if exchange_filter and isinstance(self.recipient, get_user_model()):
            try:
                reason = exchange_filter(self.instance.sender, self.recipient, None)
                if reason is not None:
                    raise forms.ValidationError(self.error_messages['filtered'].format(
                        users=self.error_messages[
                            'filtered_user_with_reason' if reason else 'filtered_user'
                        ].format(username=get_user_name(self.recipient), reason=reason)
                    ))
            except forms.ValidationError as e:
                raise forms.ValidationError(e.messages)
        return super().clean()

    def save(self, *args: Any, **kwargs: Any):
        return super()._save(self.recipient, *args, **kwargs)


class QuickReplyForm(BaseReplyForm):
    """
    The form to use in the view of a message or a conversation, for a quick reply.

    The recipient is imposed and a default value for the subject will be provided.

    """
    pass


allow_copies = not getattr(settings, 'POSTMAN_DISALLOW_COPIES_ON_REPLY', False)
class FullReplyForm(BaseReplyForm):
    """The complete reply form."""
    if allow_copies:
        recipients = CommaSeparatedUserField(
            label=(_("Additional recipients"), _("Additional recipient")), help_text='', required=False)

    class Meta(BaseReplyForm.Meta):
        fields = (['recipients'] if allow_copies else []) + ['subject', 'body']
