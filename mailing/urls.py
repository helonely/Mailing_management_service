from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MailingSettingsListView, MailingSettingsCreateView, MailingSettingsUpdateView, MailingSettingsDeleteView, \
    MailingMessageListView, MailingMessageCreateView, MailingMessageUpdateView, MailingMessageDeleteView, \
    MailingTryListView, HomeView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients/', ClientListView.as_view(template_name='mailing/client_list.html'), name='client_list'),
    path('clients/<int:pk>', cache_page(300)(ClientDetailView.as_view()), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('mailing_settings/', MailingSettingsListView.as_view(), name='settings_list'),
    path('mailing_settings/create/', MailingSettingsCreateView.as_view(), name='settings_create'),
    path('mailing_settings/<int:pk>/update/', MailingSettingsUpdateView.as_view(), name='settings_update'),
    path('mailing_settings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='settings_delete'),

    path('mailing_message/', MailingMessageListView.as_view(), name='message_list'),
    path('mailing_message/create/', MailingMessageCreateView.as_view(), name='message_create'),
    path('mailing_message/<int:pk>/update/', MailingMessageUpdateView.as_view(), name='message_update'),
    path('mailing_message/<int:pk>/delete/', MailingMessageDeleteView.as_view(), name='message_delete'),

    path('logs/', MailingTryListView.as_view(), name='logs_list'),
]