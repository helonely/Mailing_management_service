from django.contrib import admin

from mailing.models import Client, MailingSettings, MailingMessage, MailingTry


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment', 'owner')
    search_fields = ('email', 'full_name')


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_start_mailing', 'date_end_mailing', 'periodicity_mailing', 'mailing_status', 'owner', 'is_active')
    search_fields = ('date_start_mailing', 'mailing_status')
    list_filter = ('periodicity_mailing', 'mailing_status')


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body', 'owner')
    search_fields = ('subject', 'body')


@admin.register(MailingTry)
class MailingTryAdmin(admin.ModelAdmin):
    list_display = ('id', 'datetime_try_last', 'try_status', 'server_response')
    search_fields = ('datetime_try_last', 'try_status')
    list_filter = ('try_status',)
