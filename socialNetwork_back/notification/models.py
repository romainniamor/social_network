from django.db import models
import uuid 
from account.models import User
from post.models import Post
from django.utils.timesince import timesince



class Notification(models.Model):
     FRIENDREQUEST = 'new friend request'
     POST_LIKE = 'new like'
     POST_COMMENT = 'new comment'

     CHOICES_TYPE_NOTIFICATION = (
          (FRIENDREQUEST, 'New friend request'),
           (POST_LIKE, 'New like' ),
           (POST_COMMENT, 'New comment')
           )       
     


     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     body = models.TextField()
     is_read = models.BooleanField(default=False)
     type_of_notification = models.CharField(max_length = 100, choices=CHOICES_TYPE_NOTIFICATION)
     post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
     created_by = models.ForeignKey(User, related_name='created_notification', on_delete=models.CASCADE)
     created_for = models.ForeignKey(User, related_name='received', on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     

