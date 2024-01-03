
from django.urls import path

from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('profile/<uuid:id>/', api.profile_list_posts, name='profile_list_posts'),
    path('<uuid:pk>/like/', api.post_like, name="post_like"),
    path('<uuid:pk>/', api.post_details, name="post_details"),
    path('<uuid:pk>/comment/', api.post_comment, name="post_comment"),
    path('trends/', api.get_trends, name="get_trends"),
    
     
]