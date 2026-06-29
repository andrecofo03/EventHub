from django.urls import path
from services.views import (
    HomeView, EventListView, EventRegistrationView,
    EventUnregistrationView, UserRegistrationsView,
    EventCreateView, OrganizerEventsView, EventDeleteView,
    EventAttendeeListView, EventUpdateView, EventDetailView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('events/', EventListView.as_view(), name='view_events'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/register/<int:event_id>/', EventRegistrationView.as_view(), name='register_event'),
    path('events/unregister/<int:event_id>/', EventUnregistrationView.as_view(), name='unregister_event'),
    path('my_registrations/', UserRegistrationsView.as_view(), name='my_registrations'),
    path('create_event/', EventCreateView.as_view(), name='create_event'),
    path('my-organized-events/', OrganizerEventsView.as_view(), name='my_organized_events'),
    path('delete-event/<int:event_id>/', EventDeleteView.as_view(), name='delete_event'),
    path('<int:pk>/attendees/', EventAttendeeListView.as_view(), name='event_attendees'),
    path('edit_event/<int:pk>/', EventUpdateView.as_view(), name='edit_event'),
]
