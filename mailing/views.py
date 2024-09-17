from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blog.models import Blog
from mailing.forms import ClientForms
from mailing.models import Client, MailingSettings, MailingMessage, MailingTry
from mailing.services import get_all_mailings_count_from_cache, get_active_mailings_count_from_cache, \
    get_clients_count_from_cache


class HomeView(TemplateView):
    template_name = 'mailing/home.html'
    extra_context = {
            'title': 'Mail - Сервис Ваших рассылок'
        }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data()
        blog_list = Blog.objects.order_by('?')[:3]

        context_data['all_mailings_count'] = get_all_mailings_count_from_cache()
        context_data['active_mailings_count'] = get_active_mailings_count_from_cache()
        context_data['unique_clients_count'] = get_clients_count_from_cache()
        context_data['blog_list'] = blog_list

        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    extra_context = {
        'title': 'Список клиентов'
    }


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    extra_context = {
        'title': 'Клиент'
    }


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')
    form_class = ClientForms
    extra_context = {
        'title': 'Добавить клиента'
    }

    def form_valid(self, form):
        """Автоматически назначает текущего пользователя в качестве владельца статьи"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'mailing/client_form.html'
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Изменить данные клиента'
    }


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')
    extra_context = {
        'title': 'Удалить клиента'
    }


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings_form.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')
    extra_context = {
        'title': 'Добавить настройки рассылки'
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.date_next = form.instance.date_start
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings_form.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')
    extra_context = {
        'title': 'Изменить настройки рассылки'
    }


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_settings_list')
    extra_context = {
        'title': 'Удалить настройки рассылки'
    }


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings_list.html'
    extra_context = {
        'title': 'Список рассылок'
    }


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings
    template_name = 'mailing/mailing_settings_detail.html'
    extra_context = {
        'title': 'Рассылка'
    }


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage
    template_name = 'mailing/mailing_message_list.html'
    extra_context = {
        'title': 'Список сообщений'
    }


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    template_name = 'mailing/mailing_message_form.html'
    success_url = reverse_lazy('mailing:mailing_message_list')
    extra_context = {
        'title': 'Добавить сообщение',
    }

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    template_name = 'mailing/mailing_message_form.html'
    success_url = reverse_lazy('mailing:mailing_message_list')
    extra_context = {
        'title': 'Изменить сообщение',
    }


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    template_name = 'mailing/mailing_message_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_message_list')
    extra_context = {
        'title': 'Удалить сообщение',
    }


class MailingTryListView(LoginRequiredMixin, ListView):
    model = MailingTry
    template_name = 'mailing/mailing_try_list.html'
    extra_context = {
        'title': 'Отчет проведенных рассылок'
    }
