import logging
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic, View
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import  reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_tenants.utils import schema_context

from .models import EventMember, Event, ArchivedEvent, CompletedEvent, Member, Doctor
from .utils import Calendar
from .forms import EventForm, AddMemberForm


@login_required
def dashboard_view(request):
    if request.user.is_authenticated:
        doctor = Doctor.objects.filter(user=request.user).first()
        if not doctor:
            messages.error(request, "You do not have an associated doctor profile. Please contact the administrator.")

        now = datetime.now()

        with schema_context(doctor.tenant.schema_name):
            total_completed_events = CompletedEvent.objects.filter(doctor=doctor, is_completed=True)
            total_archived_events = ArchivedEvent.objects.filter(doctor=doctor).count()
            running_events = Event.objects.filter(doctor=doctor, end_time__gte=now, is_active=True)
            latest_events = Event.objects.filter(doctor=doctor).order_by('-start_time')[:10]

        context = {
            'total_completed_events': total_completed_events,
            'total_archived_events': total_archived_events,
            'running_events': running_events,
            'latest_events': latest_events,
        }

        return render(request, 'calendar2/dashboard.html', context)
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')

class ArchivedEventsListView(LoginRequiredMixin, ListView):
    template_name = "event-list.html"
    model = ArchivedEvent
    context_object_name = "archived_events"

    def get_queryset(self):
        doctor = Doctor.objects.filter(user=self.request.user).first()

        with schema_context(doctor.tenant.schema_name):
            return ArchivedEvent.objects.filter(doctor=doctor)


class CompletedEventsListView(LoginRequiredMixin, ListView):
    template_name = "completed_event_list.html"
    model = CompletedEvent
    context_object_name = "completed_events"

    def get_queryset(self):
        doctor = Doctor.objects.filter(user=self.request.user).first()

        with schema_context(doctor.tenant.schema_name):
            return CompletedEvent.objects.filter(doctor=doctor)

class RunningEventsListView(LoginRequiredMixin, ListView):
    template_name = "event-list-active.html"
    model = Event
    context_object_name = "running_events"

    def get_queryset(self):
        now = datetime.now()
        doctor = Doctor.objects.filter(user=self.request.user).first()

        with schema_context(doctor.tenant.schema_name):
            return Event.objects.filter(doctor=doctor, end_time__gte=now)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)

    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)

    return month


class CalendarView(LoginRequiredMixin, View):
    login_url = "login"
    template_name = "calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        doctor = Doctor.objects.filter(user=request.user).first()

        if not doctor:
            return redirect('home')  # Or any appropriate handling for no doctor found

        with schema_context(doctor.tenant.schema_name):
            events = Event.objects.filter(doctor=doctor)
            events_month = Event.objects.filter(doctor=doctor, end_time__gte=datetime.now())  # Fixed filtering

            event_list = [
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "description": event.description,
                }
                for event in events
            ]

            d = get_date(self.request.GET.get("month", None))
            cal = Calendar(d.year, d.month, doctor=doctor)
            html_cal = cal.formatmonth(withyear=True)

        context = {
            "form": form,
            "events": event_list,
            "events_month": events_month,
            "calendar": mark_safe(html_cal),
            "prev_month": prev_month(d),
            "next_month": next_month(d),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        doctor = Doctor.objects.filter(user=request.user).first()

        if not doctor:
            return redirect('home')  # Or any appropriate handling for no doctor found

        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.doctor = doctor

            with schema_context(doctor.tenant.schema_name):
                new_event.save()

            return redirect("calendar")

        context = {"form": form}
        return render(request, self.template_name, context)

@login_required(login_url="login")
def create_event(request):
    form = EventForm(request.POST or None)

    if request.POST and form.is_valid():
        doctor = Doctor.objects.filter(user=request.user).first()
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]

        with schema_context(doctor.tenant.schema_name):
            Event.objects.get_or_create(
                doctor=doctor,
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )
        return HttpResponseRedirect(reverse("calendar"))
    return render(request, "event.html", {"form": form})


def EventEdit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event-detail', event_id=event.id)
    else:
        form = EventForm(instance=event)

    return render(request, 'event-edit.html', {'form': form, 'event': event})



@login_required
def event_details(request, event_id):
    doctor = Doctor.objects.filter(user=request.user).first()

    with schema_context(doctor.tenant.schema_name):
        event = get_object_or_404(Event, id=event_id)
        eventmember = EventMember.objects.filter(event=event).select_related('member')
    context = {"event": event, "eventmember": eventmember}

    return render(request, "event-details.html", context)


@login_required
def add_eventmember(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    doctor = Doctor.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = AddMemberForm(request.POST, doctor=doctor)
        if form.is_valid():
            member_id = form.cleaned_data['member'].id
            member = get_object_or_404(Member, id=member_id)

            with schema_context(doctor.tenant.schema_name):
                existing_event_member = EventMember.objects.filter(event=event, member=member).exists()
                if not existing_event_member:
                    EventMember.objects.create(event=event, member=member)
                    messages.success(request, "Member added successfully.")
                else:
                    messages.warning(request, "Member is already part of this event.")
            return redirect('event-detail', event_id=event.id)
    else:
        form = AddMemberForm(doctor=doctor)

    return render(request, 'add_member.html', {'form': form})


@login_required
def delete_event_member(request, event_id, member_id):
    doctor = Doctor.objects.filter(user=request.user).first()

    with schema_context(doctor.tenant.schema_name):
        event = get_object_or_404(Event, id=event_id)
        event_member = get_object_or_404(EventMember, event=event, id=member_id)

    if request.method == 'POST':
        with schema_context(doctor.tenant.schema_name):
            event_member.delete()
        return redirect('event-detail', event_id=event.id)

    return render(request, 'remove_member.html', {'event': event, 'member': event_member.member})


logger = logging.getLogger(__name__)


@login_required
def delete_event(request, event_id):
    doctor = Doctor.objects.filter(user=request.user).first()
    event = get_object_or_404(Event, id=event_id, doctor=doctor)
    event.is_deleted = True
    event.is_active = False
    with schema_context(doctor.tenant.schema_name):
        event.save()

    if request.method == 'POST':
        # Create an ArchivedEvent before deleting
        with schema_context(doctor.tenant.schema_name):
            ArchivedEvent.objects.create(
                doctor=doctor,
                title=event.title,
                description=event.description,
                start_time=event.start_time,
                end_time=event.end_time,
                original_event_id=event_id
            )

            event.delete()
        return redirect('dashboard')

    return render(request, 'event_delete.html', {'event': event})


@login_required
def complete_event(request, event_id):
    doctor = Doctor.objects.filter(user=request.user).first()
    event = get_object_or_404(Event, id=event_id, doctor=doctor)
    event.is_completed = True
    event.is_active = False
    with schema_context(doctor.tenant.schema_name):
        event.save()

    if request.method == 'POST':
        # Create an ArchivedEvent before deleting
        with schema_context(doctor.tenant.schema_name):
            ArchivedEvent.objects.create(
                doctor=doctor,
                title=event.title,
                description=event.description,
                start_time=event.start_time,
                end_time=event.end_time,
            )

            CompletedEvent.objects.create(
                doctor=doctor,
                title=event.title,
                description=event.description,
                start_time=event.start_time,
                end_time=event.end_time,
            )

            event.delete()
        return redirect('dashboard')

    return render(request, 'complete_event.html', {'event': event})



@login_required
def next_week(request, event_id):
    doctor = Doctor.objects.filter(user=request.user).first()
    with schema_context(doctor.tenant.schema_name):
        event = get_object_or_404(Event, id=event_id)

        if request.method == "POST":
            # Create a duplicate event for the next week
            Event.objects.create(
                doctor=event.doctor,
                title=event.title,
                description=event.description,
                start_time=event.start_time + timedelta(days=7),
                end_time=event.end_time + timedelta(days=7)
            )
            return JsonResponse({"message": "Success!"})
        else:
            return JsonResponse({"message": "Error!"}, status=400)


@login_required
def next_day(request, event_id):
    doctor = Doctor.objects.filter(user=request.user).first()
    with schema_context(doctor.tenant.schema_name):
        event = get_object_or_404(Event, id=event_id)

        if request.method == "POST":
            # Create a duplicate event for the next day
            Event.objects.create(
                doctor=event.doctor,
                title=event.title,
                description=event.description,
                start_time=event.start_time + timedelta(days=1),
                end_time=event.end_time + timedelta(days=1)
            )
            return JsonResponse({"message": "Success!"})
        else:
            return JsonResponse({"message": "Error!"}, status=400)
