from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from bbqplanner.models import Event, MeatType
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as log_in, get_user


class CreateEventView(LoginRequiredMixin, View):
    """Event creation view, allows an organizer to create a new event"""

    login_url = "/login/"

    def post(self, request):
        """Handle POST request and create necessary objects"""

        event_date = parse_datetime(
            request.POST["date"] + " " + request.POST["time"])
        event = Event.objects.create(organizer=get_user(
            request), name=request.POST["name"], event_date=event_date)
        meats = request.POST["meats"].split(",")
        meat_options = [meat.strip() for meat in meats]
        for meat_option in meat_options:
            meat_type = MeatType.objects.create(event=event, name=meat_option)
        return HttpResponseRedirect(reverse("bbqplanner:events"))

    def get(self, request):
        """Render event creation form"""

        return render(request, "bbqplanner/create_event.html")
