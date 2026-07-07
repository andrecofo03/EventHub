from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme

from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from services.forms import EventForm, EditEventForm
from services.models import Event, Registration
from services.permissions import AttendeeRequiredMixin, OrganizerRequiredMixin, AdminOnlyMixin, is_admin

class HomeView(TemplateView):
    template_name = 'services/landing_page.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return render(request, 'services/landing_page.html')
        if hasattr(user, 'user_type'):
            if user.user_type == 'admin':
                return render(request, 'services/landing_page_admin.html')
            elif user.user_type == 'attendee':
                return render(request, 'services/landing_page_attendee.html')
            elif user.user_type == 'organizer':
                return render(request, 'services/landing_page_organizer.html')
        return super().get(request, *args, **kwargs)

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'services/view_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        qs = Event.objects.annotate(num_registrations=Count('registrations'))
        order_by = self.request.GET.get('order_by')
        if order_by == 'date_desc':
            qs = qs.order_by('-date')
        elif order_by == 'date_asc':
            qs = qs.order_by('date')
        elif order_by == 'full_desc':
            qs = qs.order_by('-num_registrations')
        elif order_by == 'full_asc':
            qs = qs.order_by('num_registrations')
        else:
            qs = qs.order_by('date')
        if self.request.user.is_authenticated:
            qs = qs.exclude(registrations__user=self.request.user)
            user_type = getattr(self.request.user, 'user_type', None)
            if user_type == 'organizer':
                qs = qs.exclude(organizer=self.request.user)
        return qs

class EventDetailView(DetailView):
    model = Event
    template_name = 'services/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated and user.user_type in ['attendee', 'organizer']:
            context['is_registered'] = Registration.objects.filter(event=self.object, user=user).exists()
        else:
            context['is_registered'] = False
        return context

class EventRegistrationView(LoginRequiredMixin, AdminOnlyMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if Registration.objects.filter(event=event, user=request.user).exists():
            messages.warning(request, "Ti sei già iscritto a questo evento.")
        elif event.max_capacity is not None and event.registrations.count() >= event.max_capacity:
            messages.error(request, "L'evento ha raggiunto la capacità massima.")
        else:
            Registration.objects.create(event=event, user=request.user)
            messages.success(request, f"Registrazione effettuata all'evento")
        next_url = request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect('view_events')

class EventUnregistrationView(LoginRequiredMixin, AdminOnlyMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        reg = Registration.objects.filter(event=event, user=request.user).first()
        if reg:
            reg.delete()
            messages.success(request, f"Annullata l'iscrizione all'evento")
        next_url = request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)
        return redirect('view_events')

class UserRegistrationsView(LoginRequiredMixin, AdminOnlyMixin, ListView):
    model = Event
    template_name = 'services/my_registrations.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(registrations__user=self.request.user).order_by('date')

class OrganizerEventsView(LoginRequiredMixin, AdminOnlyMixin, OrganizerRequiredMixin, ListView):
    model = Event
    template_name = 'services/my_organized_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, AdminOnlyMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'services/create_event.html'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Evento creato con successo!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class EventUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Event
    form_class = EditEventForm
    template_name = 'services/edit_event.html'

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def get_success_url(self):
        return reverse_lazy('my_organized_events')

class EventDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if event.organizer != request.user and not is_admin(request.user):
            raise PermissionDenied("Non hai i permessi per eliminare questo evento.")
        event.delete()
        if is_admin(request.user):
            return redirect('view_events')
        return redirect('my_organized_events')

class EventAttendeeListView(LoginRequiredMixin, OrganizerRequiredMixin, DetailView):
    model = Event
    template_name = 'services/event_attendees.html'
    context_object_name = 'event'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.organizer != self.request.user and not is_admin(self.request.user):
            raise PermissionDenied("Non sei l'organizzatore di questo evento.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attendees'] = Registration.objects.filter(event=self.object).select_related('user')
        return context

def custom_permission_denied_view(request, exception=None):
    context = {
        'message': str(exception) if exception else "Non hai i permessi per accedere a questa risorsa."
    }
    return render(request, 'services/403.html', context, status=403)