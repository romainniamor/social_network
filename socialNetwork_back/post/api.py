from .serializers import PostSerializer, UserSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from .models import Post, User, Like, Comment, Trend
from account.models import FriendRequest
from notification.utils import create_notification



from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm, AttachmentForm




# Create your views here.

# get tous mes posts et ceux de mes amis
@api_view(['GET'])
def post_list(request):
    #tableau dans lequel il y a lid de l user
    user_ids = [request.user.id]


    #pour chaque ami de l'user on rajoute au tableau son id
    for user in request.user.friends.all():
        user_ids.append(user.id)
    #recup les posts selon correspondance entre created_by_id dans le tableau cree preceddemnrt
    posts = Post.objects.filter(created_by_id__in=list(user_ids))


    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains='#'+trend)

    #les données du model dans le serialize 
    serializer = PostSerializer(posts, many=True)
    #envoi en json
    return JsonResponse(serializer.data, safe=False)



# recuperation de ses posts
@api_view(['GET'])
def profile_list_posts(request, id):
    user = User.objects.get(pk=id)
    profile_posts = Post.objects.filter(created_by_id = id)
    #recup post count
    count_post = profile_posts.count()


    posts_serializer = PostSerializer(profile_posts, many=True) 
    user_serializer = UserSerializer(user)
    posts_counter_serializer = count_post

    can_send_friend_request = True

    if request.user in user.friends.all():
        can_send_friend_request = False
    
    check_request_1 = FriendRequest.objects.filter(created_for = request.user).filter(created_by = user) 
    check_request_2 = FriendRequest.objects.filter(created_for = user).filter(created_by = request.user) 

    if check_request_1 or check_request_2:
        can_send_friend_request = False



    
    return JsonResponse(
        {
        'posts': posts_serializer.data,
         'user': user_serializer.data,
         'posts_counter': posts_counter_serializer,
         'can_send_friend_request': can_send_friend_request,
         }, 
         safe=False)



@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)


    if attachment_form.is_valid():
   
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid:
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            print(attachment)
            post.attachments.add(attachment)
        
     

     

        user = request.user
        user.posts_counter = user.posts_counter + 1
        user.save()
        

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'problem occur during post'})
    

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(created_by = request.user):
        like = Like.objects.create(created_by = request.user)
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()
  
        return JsonResponse({'message': 'like added'})
    else:
         return JsonResponse({'message': 'like alreday added'})
    

@api_view(['GET'])
def post_details(request, pk):
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })

@api_view(['POST'])
def post_comment(request, pk):
        comment = Comment.objects.create(body = request.data.get('body'), created_by = request.user)
        post = Post.objects.get(pk=pk)
        post.comments.add(comment)
        post.comments_count = post.comments_count + 1
        post.save()
        serializer = CommentSerializer(comment)

        return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)

    return JsonResponse(serializer.data, safe=False)






