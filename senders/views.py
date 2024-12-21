from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from senders.forms import MailingForm, MessageForm, RecipientForm
from senders.models import MailAttemptToSend, Mailing, Message, Recipient
from senders.tasks import send_mailing


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    context_object_name = "recipients"

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("senders:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("senders:recipient_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("У Вас недостаточно прав для этой операции")
        return obj


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("senders:recipient_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("У Вас недостаточно прав для этой операции")
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "messages"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("senders:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("senders:message_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("У Вас недостаточно прав для этой операции")
        return obj


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("senders:message_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404("У Вас недостаточно прав для этой операции")
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = "mailings"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.has_perm(
            "senders.can_manage_all_mailings"
        ):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("senders:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("senders:mailing_list")

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        if mailing.owner != self.request.user:
            raise Http404(
                "Вы не можете редактировать чужую рассылку",
            )
        return mailing

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Произошла ошибка при сохранении рассылки",
        )
        return super().form_invalid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy("senders:mailing_list")

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        if mailing.owner != self.request.user:
            raise Http404("Вы не можете удалить чужую рассылку")
        return mailing

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Рассылка успешно удалена")
        return super().delete(request, *args, **kwargs)


class MailAttemptListView(LoginRequiredMixin, ListView):
    model = MailAttemptToSend
    context_object_name = "attempts"


class ManagerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MailingStatisticView(ManagerOnlyMixin, ListView):
    model = Mailing
    template_name = "senders/statistics.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return (
            Mailing.objects.values("status")
            .annotate(
                total_success_count=Count(
                    "attempts",
                    filter=Q(attempts__status="success"),
                ),
                total_failure_count=Count(
                    "attempts",
                    filter=Q(attempts__status="failure"),
                ),
            )
            .order_by("status")
        )


class MailingSendView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            mailing = Mailing.objects.get(pk=pk, owner=request.user)
            send_mailing(mailing)
            messages.success(request, "Рассылка отправлена!")
        except Mailing.DoesNotExist:
            messages.error(request, "Вы не можете отправить эту рассылку")
        return HttpResponseRedirect(reverse("senders:mailing_list"))
