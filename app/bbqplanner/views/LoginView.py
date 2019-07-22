from django.http import HttpResponse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as log_in, get_user
from django.contrib import messages


class LoginView(View):
    """Form that allows organizer to log in and create/view their events"""

    def post(self, request):
        """Handle POST request for user login"""

        if not("username" in request.POST) or not("password" in request.POST):
            # Return an 'invalid login' error message.
            messages.error(
                request, "No username or password specified. Please try again.", extra_tags="is-danger")
            return render(request, "bbqplanner/login.html")

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            log_in(request, user)

            # Redirect to a success page.
            return HttpResponseRedirect(reverse("bbqplanner:events"))
        else:
            # Return an 'invalid login' error message.
            messages.error(
                request, "Wrong username or password. Please try again.", extra_tags="is-danger")
            return render(request, "bbqplanner/login.html")

    def get(self, request):
        """Direct user to events page if authenticated"""

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("bbqplanner:events"))
        else:
            return render(request, "bbqplanner/login.html")
