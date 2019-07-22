from django.test import TestCase
from django.contrib.auth.models import User
from bbqplanner.models import Event, MeatType, Visitor, VisitorMeatChoice
from django.utils.dateparse import parse_datetime


class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cspiess",
            first_name="Claudio",
            last_name="Spiess",
            password="claudio",
        )
        event_datetime = parse_datetime("2019-01-01T20:30+01:00")
        self.event = Event.objects.create(
            organizer=self.user, name="Test event", event_date=event_datetime
        )

        meat_options = ["Pork", "Steak", "Lamb", "Sausage"]
        self.meat_types = []
        for meat_option in meat_options:
            meat_type = MeatType.objects.create(event=self.event, name=meat_option)
            self.meat_types.append(meat_type)

        visitor_1 = "Test Visitor #1"
        visitor_1_guest_count = 3
        self.visitor_1_obj = Visitor.objects.create(
            event=self.event, name=visitor_1, guest_count=visitor_1_guest_count
        )

        visitor_2 = "Test Visitor #2"
        visitor_2_guest_count = 2
        self.visitor_2_obj = Visitor.objects.create(
            event=self.event, name=visitor_2, guest_count=visitor_2_guest_count
        )

        visitor_3 = "Test Visitor #3"
        visitor_3_guest_count = 0
        self.visitor_3_obj = Visitor.objects.create(
            event=self.event, name=visitor_3, guest_count=visitor_3_guest_count
        )

        self.visitor_meat_choice_1 = VisitorMeatChoice.objects.create(
            visitor=self.visitor_1_obj, meat=self.meat_types[0], count=2
        )
        VisitorMeatChoice.objects.create(
            visitor=self.visitor_1_obj, meat=self.meat_types[1], count=2
        )
        VisitorMeatChoice.objects.create(
            visitor=self.visitor_2_obj, meat=self.meat_types[2], count=2
        )
        VisitorMeatChoice.objects.create(
            visitor=self.visitor_3_obj, meat=self.meat_types[3], count=1
        )

    def test_get_meats_count(self):
        # 4 meat choices
        self.assertEqual(len(self.event.meats()), 4)

    def test_get_visitors_count(self):
        # 3 named visitor objects because guest count shouldn't be included
        self.assertEqual(len(self.event.visitors()), 3)

    def test_get_visitors_total_count(self):
        # 8 because 3 visitors, one with 3 guests, one with 2, and one with none
        self.assertEqual(self.event.visitor_total_count(), 8)

    def test_get_meat_choices(self):
        meat_choice_map = {"Pork": 2, "Steak": 2, "Lamb": 2, "Sausage": 1}
        self.assertEqual(self.event.meat_choices(), meat_choice_map)

    def test_get_event_name(self):
        self.assertEqual(str(self.event), "Test event")

    def test_get_meat_name(self):
        self.assertEqual(str(self.meat_types[0]), "Pork")

    def test_get_visitor_name(self):
        self.assertEqual(str(self.visitor_2_obj), "Test Visitor #2")

    def test_get_meat_choice_name(self):
        self.assertEqual(str(self.visitor_meat_choice_1), "Test Visitor #1 Pork")
