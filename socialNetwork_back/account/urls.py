from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api.signup, name='signup'),
    path('editprofile/', api.edit_profile, name='edit_profile'),
    path('friends/<uuid:pk>/', api.friends, name='friends'),
    path('friends/<uuid:pk>/request/', api.sendFriendRequest, name='send_friend_request'),
    path('friends/<uuid:pk>/<str:status>/', api.handle_request, name="handle_request"),
    path('friends/suggested/', api.friendship_suggestions, name="friendship_suggestions")
    
    
]