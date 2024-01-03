from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignupForm,ProfileForm
from .models import FriendRequest, User
from .serializers import UserSerializer, FriendRequestSerializer


@api_view(['GET'])
def me(request):
    return JsonResponse(
        {
            'id': request.user.id,
            'name': request.user.name,
            'email': request.user.email,
            'avatar': request.user.get_avatar(),
        }
        )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'name': data.get('name'),
        'email': data.get('email'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),    
    })
    
    if form.is_valid():
       form.save()
    else:
        message = 'error post data sign up'

    return JsonResponse({'message': message})

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        print(request.FILES)
        print(request.POST)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        
        serializer = UserSerializer(user)

        return JsonResponse({'message': 'profile updated', 'user': serializer.data})

    





@api_view(['POST'])
def sendFriendRequest(request, pk):
    user = User.objects.get(pk=pk)

    check_request_1 = FriendRequest.objects.filter(created_for = request.user).filter(created_by = user) 
    check_request_2 = FriendRequest.objects.filter(created_for = user).filter(created_by = request.user) 
    
    if not check_request_1 or not check_request_2:
        friend_request = FriendRequest.objects.create(created_for=user, created_by=request.user)

        return JsonResponse({'message': 'friend relation created'})
    else:
        return JsonResponse({'message':'already requested'})

@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)

    requests = []

    # u = request.user
    # u.friends_counter = 1
    # u.save()

    # user.friends_counter = 1
    # user.save()
    if user == request.user:
        requests = FriendRequest.objects.filter(created_for = request.user, status=FriendRequest.SENT) 
        requestSerializer = FriendRequestSerializer(requests, many=True).data
       
    
         

    friends = user.friends.all()

    userSerializer = UserSerializer(user).data
    friendsSerializer = UserSerializer(friends, many=True).data

    return JsonResponse(
        {
            'user': userSerializer, 
            'friends': friendsSerializer, 
            'requests': requestSerializer,
            }
            , safe=False)

@api_view(['POST'])
def handle_request(request, pk, status):
    
    user = User.objects.get(pk=pk)
    
    friend_request = FriendRequest.objects.filter(created_for=request.user).get(created_by=user)
    friend_request.status = status
    friend_request.save()
    #ajout de l'ami
    user.friends.add(request.user)
     #maj friends_counter
    user.friends_counter = user.friends_counter + 1
    user.save()

    request_user = request.user
    request_user.friends_counter = request_user.friends_counter + 1

    request_user.save()

    return JsonResponse({'message': 'friends updated'})

@api_view(['GET'])
def friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)
    print("serializer.data", serializer.data)

    return JsonResponse(serializer.data, safe=False)



 