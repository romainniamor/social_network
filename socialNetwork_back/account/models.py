from typing import Any
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

class CustomUserManger(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('Invalid Email')
        email = self.normalize_email(email)
        user =self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    friends = models.ManyToManyField('self')
    friends_counter = models.IntegerField(default=0)

    posts_counter = models.IntegerField(default=0)

    people_you_may_know = models.ManyToManyField('self')


    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManger()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_avatar(self):
        if self.avatar:
            return 'http://127.0.0.1:8000' + self.avatar.url
        else:
            return 'http://127.0.0.1:8000/media/avatars/default_user.png'


class FriendRequest(models.Model):
        SENT = 'sent'
        ACCEPTED = 'accepted'
        DECLINED = 'declined'

        STATUS_CHOICES = (
             (SENT, 'Sent'),
             (ACCEPTED, ' Accepted'),
             (DECLINED, 'Declined')
        )
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        created_at = models.DateTimeField(auto_now_add=True)
        created_by = models.ForeignKey(User, related_name='created_relation', on_delete=models.CASCADE)
        created_for = models.ForeignKey(User, related_name='received_friend_request', on_delete=models.CASCADE)
        status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=SENT)
        
        





