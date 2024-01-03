from django.urls import path

from . import api

urlpatterns = [
    path('', api.conversations_list, name='conversations_list'),
    path('<uuid:pk>/', api.conversation_details, name='conversation_details'),    
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'), 
    path('<uuid:pk>/get-or-create/', api.conversation_get_or_create, name='conversation_get_or_create'), 
      
]