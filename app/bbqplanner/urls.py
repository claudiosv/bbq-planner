from django.urls import path
from bbqplanner.views.HomePageView import HomePageView
from bbqplanner.views.EventDetailView import EventDetailView
from bbqplanner.views.EventOverviewView import EventOverviewView
from bbqplanner.views.EventsListView import EventsListView
from bbqplanner.views.CreateEventView import CreateEventView
from bbqplanner.views.LoginView import LoginView
from bbqplanner.views.RegisterEventView import RegisterEventView
from bbqplanner.views.RegisterView import RegisterView

app_name = "bbqplanner"
urlpatterns = [
    # Home page of site
    path("", HomePageView.as_view(), name="index"),
    # Login form
    path("login/", LoginView.as_view(), name="login"),
    # Registration form
    path("register/", RegisterView.as_view(), name="register"),
    # Create event form
    path("event/create", CreateEventView.as_view(), name="create-event"),
    # View event overview, link to be shared and direct people to register
    path("event/<int:pk>/", EventOverviewView.as_view(), name="event-overview"),
    # Register for event form
    path("event/<int:pk>/register", RegisterEventView.as_view(), name="register-event"),
    # View event details from, including shopping list
    path("event/<int:pk>/details", EventDetailView.as_view(), name="event-details"),
    # View overview of all events
    path("events/", EventsListView.as_view(), name="events"),
]
