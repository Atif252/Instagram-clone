from django.contrib import admin
from activity.models import Notification


class NotificationAdmin(admin.ModelAdmin):
	list_display = ('notification_type', 'timestamp')

admin.site.register(Notification, NotificationAdmin)

