from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    USER_TYPES = [
        ("attendee", "Partecipante"),
        ("organizer", "Organizzatore"),
        ("admin", "Amministratore"),
    ]

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        default="attendee",
        verbose_name="Tipo utente",
        help_text="Seleziona il tipo di utente: Partecipante o organizzatore.",
    )
    email = models.EmailField(unique=True)

