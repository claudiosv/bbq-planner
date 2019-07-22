from django.views import View
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from bbqplanner.models import Event, MeatType, Visitor, VisitorMeatChoice
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as log_in, get_user


class RegisterEventView(View):
    """
    View allowing a visitor to register for an
    event and specify guest and meat choices
    """

    def post(self, request, pk):
        """Handle POST request that specifices guest and meat counts"""

        if not("name" in request.POST) or not("number" in request.POST):
            return self.get(request, pk)
        visitor = request.POST["name"]
        num_guests = request.POST["number"]

        visitor_obj = Visitor.objects.create(
            event=Event(pk), name=visitor, guest_count=num_guests)

        meat_choices = [(x[5:], request.POST[x]) for x in request.POST if x.startswith(
            "meat-") and int(request.POST[x]) > 0]
        for meat_choice in meat_choices:
            VisitorMeatChoice.objects.create(
                visitor=visitor_obj, meat=MeatType(meat_choice[0]), count=meat_choice[1])

        return render(request, "bbqplanner/registered.html")

    def get(self, request, pk):
        """Handle GET request to view event details for registration"""

        visitors = MeatType.objects.filter(event_id=pk)
        event = Event.objects.get(pk=pk)
        context = {"event": event, "visitors": visitors}
        return render(request, "bbqplanner/register_event.html", context=context)
