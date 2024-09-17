from django import forms
from django.forms import BooleanField

from mailing.models import Client, MailingSettings, MailingMessage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'  # По умолчанию поле будет в виде чекбокса.
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForms(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment',)


class MailingSettingsForms(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = ('periodicity_mailing', 'message', 'clients',)
        exclude = ('date_start_mailing', 'date_end_mailing',)


class MailingMessageForms(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ('subject', 'body',)

