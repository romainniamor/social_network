from django.db import models
from account.models import User
from django.utils.timesince import timesince
import uuid

# Create your models here.

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def modified_at_formated(self):
        time_since = timesince(self.created_at)
        parts = time_since.split(", ") 
        if len(parts) > 0:
            return parts[0]
        return time_since
    

class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField(max_length=250 )
    sent_to = models.ForeignKey(User, related_name='received_message', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='sent_message', on_delete=models.CASCADE)

    def created_at_formated(self):
        time_since = timesince(self.created_at)
        parts = time_since.split(", ") 
        if len(parts) > 0:
            return parts[0]
        return time_since



