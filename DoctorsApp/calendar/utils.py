from calendar import HTMLCalendar
from .models import Event, Doctor
from django_tenants.utils import schema_context
from django.contrib import messages


def get_doctor_or_redirect(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    if not doctor:
        messages.error(request, "You do not have an associated doctor profile. Please contact the administrator.")
        return None
    return doctor

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, doctor=None):
        self.year = year
        self.month = month
        self.doctor = doctor
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    def formatmonth(self, withyear=True):
        with schema_context(self.doctor.tenant.schema_name):
            events = Event.objects.filter(
                start_time__year=self.year, start_time__month=self.month, doctor=self.doctor
            )
            cal = (
                '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
            )  # noqa
            cal += (
                f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
            )  # noqa
            cal += f"{self.formatweekheader()}\n"
            for week in self.monthdays2calendar(self.year, self.month):
                cal += f"{self.formatweek(week, events)}\n"
            return cal
