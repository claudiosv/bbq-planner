from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from bbqplanner.models import Event


class EventDetailView(LoginRequiredMixin, DetailView):
    """View for details of an event, allowing organier to see how much of what to buy"""

    model = Event
    template_name = "bbqplanner/detail.html"
    login_url = "/login/"
