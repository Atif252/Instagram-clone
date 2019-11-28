from django.shortcuts import render, redirect,  get_object_or_404
from django.views.decorators.cache import cache_control
from chat.forms import CreateChatMessage
from chat.models import Chat, Message
from account.models import Account
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def message_view(request, slug):
	user = request.user

	context = {}

	if not user.is_authenticated:
		return redirect('login')

	user_profile = Account.objects.get(slug=slug)
	context['user_profile'] = user_profile
	try:
		chat = Chat.objects.get(
			Q(user01=user, user02=user_profile) | Q(user01=user_profile, user02=user)
		)
		context['chat'] = chat
	except Chat.DoesNotExist:
		return redirect("add_chat", user_profile.slug)

	try:
		# Querying All Messages
		messages = Message.objects.filter(chat=chat)
		context['messages'] = messages
		# Querying Non-Deleted Messages

		update_message_status = Message.objects.filter(chat=chat).filter(message_sender=user_profile).update(status=2)
	except Message.DoesNotExist:
		return None
	form = CreateChatMessage(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		message_body = form.cleaned_data.get('message_body')
		obj.message_body = message_body
		obj.save()
		form = CreateChatMessage()
		return redirect('chat:message', user_profile.slug)

	return render(request, 'chat/messages.html', context)

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inbox_view(request):
	user = request.user

	context = {}

	if not user.is_authenticated:
		return redirect('login')

	try:
		chats = Chat.objects.filter(
			Q(user01=user) | Q(user02=user)
		)
	except Chat.DoesNotExist:
		return redirect("home")

	messages = Message.objects.filter(chat__in=chats).last()

	context['messages'] = messages

	context['chats'] = chats

	return render(request, 'chat/inbox.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def new_chat_list(request):
	user = request.user

	context = {}

	accounts = Account.objects.all().exclude(username=user.username)

	context['accounts'] = accounts

	return render(request, 'chat/new_chat_list.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def new_chat(request, slug):
	user = request.user

	context = {}

	user_profile = Account.objects.get(slug=slug)

	try:
		chat = Chat.objects.get(
			Q(user01=user, user02=user_profile) | Q(user01=user_profile, user02=user)
		)
	except Chat.DoesNotExist:
		chat = Chat.objects.get_or_create(
			user01 = user,
			user02 = user_profile
		)

	context['response'] = "Chat Created Successfully"

	return redirect('chat:message', slug=user_profile.slug)


def delete_chat(request, id):
	user = request.user

	if not user.is_authenticated:
		return redirect('home')

	try:
		chat = Chat.objects.get(id=id)
	except Chat.DoesNotExist:
		return redirect('chat:inbox')

	
	if chat.deletefor is None:
		if chat.user01 == user:
			Chat.objects.filter(id=id).update(deletefor=1)
		else:
			Chat.objects.filter(id=id).update(deletefor=2)
	else:
		chat.delete()

	return redirect('chat:inbox')


def delete_message(request, id, slug):
	user = request.user

	if not user.is_authenticated:
		return redirect('home')

	user_profile = Account.objects.get(slug=slug)

	message = Message.objects.get(id=id)

	message_sender = message.message_sender

	if message_sender == user:
		message.delete_by_sender = True
		message.save()
	else:
		message.delete_by_receiver = True
		message.save()

	if message.delete_by_receiver == True and message.delete_by_sender == True:
		message.delete()

	return redirect('chat:message', user_profile.slug)