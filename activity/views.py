from django.shortcuts import render, redirect,  get_object_or_404
from activity.models import Notification
from account.models import Connection, Request


def all_notification_view(request):
	context = {}
	user = request.user
	
	notifications = Notification.objects.filter(user=user)
	context['authenticated'] = True
	status_list = []
	request_list = []
	for notification in notifications:
		if Connection.objects.filter(following=user, followers=notification.notification_by).exists():
			status_list.append(notification.notification_by)
		elif Request.objects.filter(request_by=user, target_user=notification.notification_by).exists():
			request_list.append(notification.notification_by)
	context['status_list'] = status_list
	context['request_list'] = request_list
	context['notifications'] = notifications
	context['response'] = 'all'

	return render(request, 'activity/notifications.html', context)


def request_notification_view(request):
	context = {}
	user = request.user
	notifications = Notification.objects.get(user=user, notification_type='request')
	context['notification'] = notification
	
	context['response'] = 'request'


	return render(request, 'activity/notifications.html', context)
