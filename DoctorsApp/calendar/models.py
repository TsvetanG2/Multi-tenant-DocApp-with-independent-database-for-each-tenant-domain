from datetime import datetime

from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from DoctorsApp.tenants.models import Tenant


class Doctor(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='doctors')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name() if self.user.get_full_name() else self.user.username


class Member(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='members')
    MIN_MEMBERNAME_LENGTH = 5
    MAX_MEMBERNAME_LENGTH = 55
    name = models.CharField(
        max_length=MAX_MEMBERNAME_LENGTH,
        validators=[
            MinLengthValidator(MIN_MEMBERNAME_LENGTH),
        ]
    )
    email = models.EmailField(
        blank=False,
        null=False,
    )
    age = models.IntegerField(
        blank=False,
        null=False,
    )
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, doctor):
        return self.filter(doctor=doctor, is_active=True, is_deleted=False)

    def get_running_events(self, doctor):
        return self.filter(
            doctor=doctor,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")

class EventAbstract(models.Model):
    """ Event abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Event(EventAbstract):
    """ Event model """

    STATUS_CHOICES = (
        ('running', 'Running'),
        ('completed', 'Completed'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    original_event_id = models.IntegerField(null=True, blank=True)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event-detail", args=[self.id])

    @property
    def get_html_url(self):
        url = reverse("event-detail", args=[self.id])
        return f'<a href="{url}"> {self.title} </a>'

class EventMember(models.Model):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_members")
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="event_memberships"
    )

    class Meta:
        unique_together = ["event", "member"]

    def __str__(self):
        return str(self.member)

class ArchivedEvent(EventAbstract):
    """ Archived Event model """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="archived_events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    original_event_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class CompletedEvent(EventAbstract):
    """ Completed Event model """

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="completed_events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    original_event_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title
