from django.urls import path
from activity.views import (
	all_notification_view,
	request_notification_view,
)



app_name = 'activity'


urlpatterns = [
	path('all/', all_notification_view, name='notifications'),
	path('requests/', request_notification_view, name='request_notifications')
]