from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from bbqplanner.models import Event


class TestCreateEventView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<IRoAmUkw+tuK"
        )

    def test_redirect_event_creation(self):
        url = reverse("bbqplanner:create-event")

        # test req method GET
        response = self.client.get(url)
        self.assertRedirects(response, "/login/?next=/event/create")

        response = self.client.post(url, {})
        self.assertRedirects(response, "/login/?next=/event/create")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser1", password="1X<IRoAmUkw+tuK")
        response = self.client.get(reverse("bbqplanner:create-event"))
        self.assertTemplateUsed(response, "bbqplanner/create_event.html")


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        url = reverse("bbqplanner:login")

        # test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)


class TestRegisterEventView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<IRoAmUkw+tuK"
        )
        event_datetime = parse_datetime("2019-01-01T20:30+01:00")
        self.event = Event.objects.create(
            organizer=test_user1, name="Test event", event_date=event_datetime
        )

    def test_event_registration(self):
        url = reverse("bbqplanner:register-event", args=[self.event.pk])

        # test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)


class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<IRoAmUkw+tuK"
        )

    def test_registration(self):
        url = reverse("bbqplanner:register")

        # test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)


class TestEventsListView(TestCase):
    def setUp(self):
        self.client = Client()
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<IRoAmUkw+tuK"
        )

    def test_redirect_events_list(self):
        url = reverse("bbqplanner:events")

        # test req method GET
        response = self.client.get(url)
        self.assertRedirects(response, "/login/?next=/events/")

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser1", password="1X<IRoAmUkw+tuK")
        response = self.client.get(reverse("bbqplanner:events"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bbqplanner/events.html")
