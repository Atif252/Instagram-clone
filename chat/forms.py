from django import forms
from chat.models import Chat, Message
from django.db.models import Q
from django.http import request



class CreateChatMessage(forms.ModelForm):
	

	class Meta:
		model = Message
		fields = ['message_body', 'message_sender', 'chat']
