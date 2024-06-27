from django.contrib import admin
from .models import Event, EventMember, ArchivedEvent, CompletedEvent, Doctor, Member


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant', 'specialty']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'doctor', 'email', 'age', 'phone', 'address', 'city', 'state', 'zipcode']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['doctor', 'city', 'state']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'title', 'description', 'start_time', 'end_time', 'original_event_id')


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ('event', 'member')

@admin.register(ArchivedEvent)
class ArchivedAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'title', 'description', 'start_time', 'end_time', 'original_event_id')

@admin.register(CompletedEvent)
class CompletedAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'title', 'description', 'start_time', 'end_time', 'original_event_id')
