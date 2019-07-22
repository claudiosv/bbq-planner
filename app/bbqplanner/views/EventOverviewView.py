from django.views.generic.detail import DetailView
from bbqplanner.models import Event


class EventOverviewView(DetailView):
    """View basic information about an event before registering for it"""

    model = Event
    template_name = "bbqplanner/overview.html"
