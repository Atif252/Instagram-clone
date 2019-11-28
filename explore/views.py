from django.shortcuts import render, redirect
from account.models import Account, Connection, Request
from django.db.models import Q



def suggest_accounts_view(request):	
	user = request.user
	context = {}
	if user.is_authenticated:
		accounts = Account.objects.all()
	else:
		return redirect('login')
	
	context['user'] = user

	connection_followers = Connection.objects.filter(
		followers=user, request=False
	)

	followers_list = []
	following_list = []
	request_list = []
	for account in accounts:
		if Connection.objects.filter(following=user, followers=account).exists():
			followers_list.append(account)
		elif Request.objects.filter(request_by=user, target_user=account).exists():
			request_list.append(account)
		if Connection.objects.filter(followers=user, following=account).exists():
			following_list.append(account)
		
	context['followers_list'] = followers_list
	context['following_list'] = following_list
	context['request_list'] = request_list

	# for account in accounts:
	# 	if account != user:
	# 		if Connection.objects.filter(following=user, followers=account).exists():
	# 			context['following'] = account
	# 		elif Request.objects.filter(request_by=user, target_user=account).exists():
	# 			context['request'] = account

	context['connections'] = connection_followers
	context['accounts'] = accounts
	return render(request, 'explore/account_suggestion.html', context)