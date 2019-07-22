from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum


class Event(models.Model):
    """
    Event model represents a single BBQ event
    which has an organizer (a registered user), a name,
    an event date & time, and date that the event was created.
    """

    organizer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    date_posted = models.DateField(auto_now=True)
    event_date = models.DateTimeField(auto_now=False)

    def __str__(self):
        return self.name

    def meats(self):
        """Return the available meats of the event."""

        return MeatType.objects.filter(event_id=self.id)

    def visitors(self):
        """Return the registered visitors of the event."""

        return Visitor.objects.filter(event_id=self.id)

    def visitor_total_count(self):
        """Return the total number of visitors including guests of the event."""

        visitors = Visitor.objects.filter(event_id=self.id)
        visitor_count = visitors.count()
        guests_count = visitors.values("guest_count").aggregate(
            Sum("guest_count"))["guest_count__sum"]
        if not guests_count:
            guests_count = 0
        total_count = guests_count + visitor_count
        return total_count

    def meat_choices(self):
        """
        Return a map of all meat choices with the
        number of times the piece is wanted
        """

        meat_counts = {}
        meat_options = MeatType.objects.filter(event__id__exact=self.id)
        for option in meat_options:
            meat_counts[option.name] = 0

        meat_choice_queryset = (VisitorMeatChoice.objects
                                .filter(meat__event__id__exact=self.id)
                                .values("meat__name")
                                .annotate(meat_sum=Sum("count")))

        for meat_choice in meat_choice_queryset:
            meat_counts[meat_choice["meat__name"]] = meat_choice["meat_sum"]
        return meat_counts


class MeatType(models.Model):
    """
    Represents a type of meat, with a name such as "Steak",
    specific to one event.
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


class Visitor(models.Model):
    """
    Represents a person signed up to attend a specific event.
    Has a name and number of guests
    """

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    guest_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class VisitorMeatChoice(models.Model):
    """
    Represents the number of pieces of a specific meat
    a specific visitor wants
    """

    visitor = models.ForeignKey(
        Visitor,
        on_delete=models.CASCADE
    )
    meat = models.ForeignKey(
        MeatType,
        on_delete=models.CASCADE
    )
    count = models.IntegerField()

    def __str__(self):
        return self.visitor.name + " " + self.meat.name
