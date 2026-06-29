from django.core.exceptions import PermissionDenied

def is_organizer(user):
    return user.user_type == 'organizer'  

def is_attendee(user):
    return user.user_type == 'attendee'  

def is_admin(user):
    return getattr(user, "user_type", None) == "admin"

class OrganizerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not (is_organizer(request.user) or is_admin(request.user)):
            raise PermissionDenied("Solo gli organizzatori o amministratori possono accedere a questa pagina")
        return super().dispatch(request, *args, **kwargs)

class AttendeeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_attendee(request.user):
            raise PermissionDenied("I partecipanti hanno il permesso di accedere a questa pagina")
        return super().dispatch(request, *args, **kwargs)

class AdminOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if is_admin(request.user):
            raise PermissionDenied("Non puoi eseguire questa azione")
        return super().dispatch(request, *args, **kwargs)