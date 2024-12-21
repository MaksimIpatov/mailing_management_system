from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authorizations.forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            "Вы успешно зарегистрированы!",
        )
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Ошибка при регистрации. Пожалуйста, исправьте ошибки",
        )
        return super().form_invalid(form)
