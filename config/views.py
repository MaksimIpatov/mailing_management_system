from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from senders.models import Mailing, Recipient


class HomeView(TemplateView):
    template_name = "index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["total_mailings"] = Mailing.objects.count()
        data["active_mailings"] = Mailing.objects.filter(
            status="started",
        ).count()
        data["unique_recipients"] = Recipient.objects.distinct().count()

        return data
