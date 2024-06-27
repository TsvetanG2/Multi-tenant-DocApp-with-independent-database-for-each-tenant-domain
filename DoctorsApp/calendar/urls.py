from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('events/archived/', views.ArchivedEventsListView.as_view(), name='archived-events'),
    path('events/completed/', views.CompletedEventsListView.as_view(), name='completed-events'),
    path('events/running/', views.RunningEventsListView.as_view(), name='running-events'),
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/create/', views.create_event, name='event-create'),
    path('event/<int:event_id>/', views.event_details, name='event-detail'),
    path('event/<int:event_id>/edit/', views.EventEdit, name='event-edit'),
    path('event/<int:event_id>/delete/', views.delete_event, name='event-delete'),
    path('event/<int:event_id>/complete/', views.complete_event, name='complete-event'),
    path('event/<int:event_id>/add-member/', views.add_eventmember, name='add-event-member'),
    path('event/<int:event_id>/remove-member/<int:member_id>/', views.delete_event_member, name='delete-event-member'),
    path('event/next-week/<int:event_id>/', views.next_week, name='next-week'),
    path('event/next-day/<int:event_id>/', views.next_day, name='next-day'),
]
