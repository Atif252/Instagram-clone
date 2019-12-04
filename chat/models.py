from django.db import models
from django.conf import settings



STATUS_CHOICES = (
    (1, "Sent"),
    (2, "Seen"),
)

DELETEFOR_CHOICES = (
    (1, "DELETED for user01"),
    (2, "DELETED for user02"),
)


class Chat(models.Model):
	started 			= models.DateTimeField(auto_now_add=True, editable=False)
	user01				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user01_chat', null=True)
	user02				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user02_chat', null=True)
	deletefor			= models.IntegerField(choices=DELETEFOR_CHOICES, null = True, blank=True, default=0)
	

	def get_last_message(self):
		message = Message.objects.filter(deletefor=0).filter(chat=self).last()
		return message if message else ""

	def get_last_message_timestamp(self):
		message = Message.objects.filter(chat=self).last()
		return message.timestamp if message else ""

	def get_chat_delete_details(self):
		return self.deletefor

class Message(models.Model):
	message_body		= models.CharField(max_length=2200, blank=False)
	image				= models.ImageField(null=True, blank=True)
	timestamp			= models.DateTimeField(auto_now=True, editable=False)
	chat 				= models.ForeignKey(Chat, on_delete=models.CASCADE)
	message_sender		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender', null=True)
	status				= models.IntegerField(choices=STATUS_CHOICES, default=1)
	delete_by_sender	= models.BooleanField(default=False)
	delete_by_receiver	= models.BooleanField(default=False)
	
	def __str__(self):
		return self.message_body

	def sender(self):
		return self.sender

	def message(self):
		return self.message