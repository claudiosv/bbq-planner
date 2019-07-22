from django.views.generic.list import ListView
from bbqplanner.models import Event
from django.contrib.auth.mixins import LoginRequiredMixin


class EventsListView(LoginRequiredMixin, ListView):
    """List of all events organized by user"""

    model = Event
    template_name = "bbqplanner/events.html"
    context_object_name = "events"
    login_url = "/login/"

    def get_queryset(self):
        """Return the events organized by the current user."""
        return Event.objects.filter(organizer=self.request.user).order_by("-event_date")
