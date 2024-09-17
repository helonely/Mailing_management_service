import secrets
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView

from users.forms import UserRegisterForm, PasswordResetForm, ProfileEditForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Подтвердите почту, для этого нужно перейти по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class PasswordResetView(FormView):
    form_class = PasswordResetForm
    template_name = "users/password_reset.html"
    success_url = reverse_lazy('users:login')  # Переход на страницу с сообщением об успешной смене пароля

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)  # Получаем пользователя по email
            except ObjectDoesNotExist:
                form.add_error('email', 'Пользователь с таким email не найден')  # Если пользователь не найден, добавляем ошибку
                return self.form_invalid(form)
            password = User.objects.make_random_password(length=12)
            user.set_password(password)
            user.save()
            send_mail(subject='Подтверждение пароля',
                      message=f'Пароль для вашего аккаунта: {password}',
                      from_email=EMAIL_HOST_USER, recipient_list=[user.email],)
            return super().form_valid(form)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users/profile_detail.html')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def profile_detail(request):
    user = request.user
    return render(request, 'users/profile_detail.html', {'user': user})
