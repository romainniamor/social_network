from .models import Notification
from post.models import Post
from account.models import FriendRequest


def create_notification(request, type_of_notification, post_id=None, friendrequest_id=None):
    created_for = None
    
    if type_of_notification == 'post_like':
            body = f'Like from {request.user.name}'
            post = Post.objects.get(pk=post_id)
            created_for = post.created_by
    elif type_of_notification == 'post_comment':
            body = f'Comment from {request.user.name}'
            post = Post.objects.get(pk=post_id)
            created_for = post.created_by
    elif type_of_notification == 'friendrequest':
            body = f'New invitation from {request.user.name}'
            friendrequest = FriendRequest.objects.get(pk=friendrequest_id)
            created_for = friendrequest.created_for

    notification = Notification.objects.create(
           body=body,
           type_of_notification=type_of_notification,
           created_by = request.user,
           post_id=post_id,
           created_for=created_for
    )

    return notification


    

      
  

    # class Notification(models.Model):
    #  FRIENDREQUEST = 'newfriendrequest'
    #  POST_LIKE = 'newlike'
    #  POST_COMMENT = 'newcomment'

    #  CHOICES_TYPE_NOTIFICATION = (
    #       (FRIENDREQUEST, 'New friend request'),
    #        (POST_LIKE, 'New like' ),
    #        (POST_COMMENT, 'Post comment')
    #        )       
     


    #  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #  created_by = models.ForeignKey(User, related_name='created_notification', on_delete=models.CASCADE)
    #  created_for = models.ForeignKey(User, related_name='received', on_delete=models.CASCADE)
    #  body = models.TextField()
    #  post_id = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)
    #  created_at = models.DateTimeField(auto_now_add=True)
    #  is_read = models.BooleanField(default=False)
    #  type_of_notification = models.CharField(max_length = 100, choices=CHOICES_TYPE_NOTIFICATION)
