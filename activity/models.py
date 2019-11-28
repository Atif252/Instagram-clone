from django.db import models
from account.models import Account
from post.models import Post

NOTIFICATION_MESSAGE=(
	('following', 'started following you'),
	('like', 'liked your photo')
)

NOTIFICATION_TYPE=(
	('request', 'REQUEST_NOTIFICATION'),
	('following', 'FOLLOWING_NOTIFICATION'),
	('like', 'LIKE_NOTIFICATION'),

)
class Notification(models.Model):
	message 					= models.CharField(choices=NOTIFICATION_MESSAGE, null=True, max_length=100)
	notification_type			= models.CharField(choices=NOTIFICATION_TYPE, max_length=100)
	timestamp 					= models.DateTimeField(auto_now=True, editable=False)
	user						= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifcation_for_user')
	notification_by				= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifcation_by_user')
	post 						= models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		ordering  = ('-timestamp',)
