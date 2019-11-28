from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Connection, Request

class AccountAdmin(UserAdmin):
	list_display = ('email', 'username', 'date_joined', 'is_admin','is_staff')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(Connection)
admin.site.register(Request)