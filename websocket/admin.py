from django.contrib import admin
from .models import ChatMessage, Connection

# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(Connection)

