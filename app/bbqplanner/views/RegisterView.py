from django.http import HttpResponse
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as log_in, get_user
from django.contrib import messages
from django.contrib.auth.models import User


class RegisterView(View):
    """View that allows organizer to register an account"""

    def post(self, request):
        """Handle POST request to make a new user in the system"""

        if "password" in request.POST and "passwordConfirmation" in request.POST:
            if request.POST["password"] != request.POST["passwordConfirmation"]:
                messages.error(
                    request,
                    "Passwords did not match. Please try again.",
                    extra_tags="is-danger",
                )
                return HttpResponseRedirect(reverse("bbqplanner:register"))
        else:
            messages.error(
                request,
                "Password was not entered. Please try again.",
                extra_tags="is-danger",
            )
            return HttpResponseRedirect(reverse("bbqplanner:register"))
        user = User.objects.create_user(
            username=request.POST["username"],
            first_name=request.POST["firstName"],
            last_name=request.POST["lastName"],
            password=request.POST["password"],
        )
        messages.success(
            request,
            "Account successfully created. Please login.",
            extra_tags="is-success",
        )
        return HttpResponseRedirect(reverse("bbqplanner:login"))

    def get(self, request, *args, **kwargs):
        """Handle GET request for registration page"""

        return render(request, "bbqplanner/register.html")
