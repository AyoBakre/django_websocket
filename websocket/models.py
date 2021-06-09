from django.db import models


class Connection(models.Model):
    connection_id = models.CharField(max_length=255, default=1)

    def __str__(self):
        return self.connection_id


class ChatMessage(models.Model):
    username = models.CharField(max_length=50)
    messages = models.CharField(max_length=400)
    timestamp = models.CharField(max_length=100)