from django.urls import path
from explore.views import(
	suggest_accounts_view,
)


app_name = 'explore'

urlpatterns = [
	path('explore/', suggest_accounts_view, name="account_suggestion"),
]