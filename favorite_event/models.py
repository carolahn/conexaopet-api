from django.db import models
from django.conf import settings
from event.models import Event

class FavoriteEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favorite_event'
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user.username} - {self.event.name}' 