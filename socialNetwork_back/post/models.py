from django.db import models
import uuid 
from account.models import User
from django.utils.timesince import timesince

#def des elements de post et pj (rajouter un counter de like)

class Like(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    #modif de l affichage du time avec timesince, recuperation du premier element seulement en splitant la chaine de caractere(Day, Hour, Min) 
    def created_at_formated(self):
        time_since = timesince(self.created_at)
        parts = time_since.split(", ") 
        if len(parts) > 0:
            return parts[0]
        return time_since

class PostAttachments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='attachments_posts') #file d envoi des pieces jointes
    created_by = models.ForeignKey(User, related_name='posts_attachments', on_delete=models.CASCADE) 

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        
        else:
            return ''

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    attachments = models.ManyToManyField(PostAttachments, blank=True)
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)
    

    class Meta:
        ordering = ('-created_at',)

    #modif de l affichage du time avec timesince, recuperation du premier element seulement en splitant la chaine de caractere(Day, Hour, Min) 
    def created_at_formated(self):
        time_since = timesince(self.created_at)
        parts = time_since.split(", ") 
        if len(parts) > 0:
            return parts[0]
        return time_since
    
class Trend(models.Model):
    hashtag = models.CharField(max_length=100)
    occurence = models.IntegerField()





  