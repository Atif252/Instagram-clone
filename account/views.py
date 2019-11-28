from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.cache import cache_control
from account.forms import RegistrationForm,AccountAuthenticationForm,AccountUpdateForm
from post.models import Post
from account.models import Account, Connection, Request
from activity.models import Notification
from django.contrib import messages



def registration_view(request):
	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("home")
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			username = form.cleaned_data.get('username').lower()
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect("home")
	else:
		form = RegistrationForm()
	context['registration_form'] = form
	return render(request, 'account/register.html', context)



def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email'].lower()
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form

	return render(request, 'account/login.html', context)


def logout_view(request):
	logout(request)
	return redirect("home")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account_view(request, slug):

	if not request.user.is_authenticated:
		return redirect("login")

	context = {}
	user = request.user
	context['user'] = user

	try:
		user_profile = Account.objects.get(slug=slug)

		posts = Post.objects.filter(author=user_profile)
		context['posts'] = posts

		posts_count = Post.objects.filter(author=user_profile).count()
		context['posts_count'] = posts_count

	except Account.DoesNotExist:
		return redirect('home')

	context['followers'] = Connection.objects.filter(
			followers = user_profile
		).count()

	context['following'] = Connection.objects.filter(
			following = user_profile
		).count()

	if user.account_type == 'private':
		try:
			account_request = Request.objects.get(
			request_by=user_profile,
			target_user=user
			)
			context['user_profile_requested'] = True
		except Request.DoesNotExist:
			context['has_not_requested'] = True

	if user != user_profile:
		if Connection.objects.filter(following=user_profile).filter(followers=user) and not Connection.objects.filter(following=user,followers=user_profile):
					context['follow_back'] = True
		elif not Connection.objects.filter(
			followers=user_profile,
			following=user,
		):
			not_follows = True
			context['not_follows'] = not_follows

		if user_profile.account_type == 'private':
			try:
				request_ = Request.objects.get(
					request_by=user,
					target_user=user_profile
				)
				context['requested'] = True
			except Request.DoesNotExist:
				if not Connection.objects.filter(followers=user_profile,following=user):
					context['private'] = True
				

	context['user_profile'] = user_profile

	return render(request, 'account/account.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_account_view(request):
	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	user_account_type = request.user.account_type
	if user_account_type == 'private':
		response = True
	else:
		response = False

	if request.POST:
		form = AccountUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
		if form.is_valid():
			form.initial = {
				"name": request.POST['name'],
				"email" : request.POST['email'].lower(),
				"username" : request.POST['username'].lower(),
				"bio": request.POST['bio'], 
				"profile_picture": request.POST.get('profile_picture', False),
				'account_type': request.POST.get('account_type', 'public')
			}
			obj = form.save(commit=False)
			account_type = form.cleaned_data['account_type']
			print(account_type)
			obj.save()
			messages.success(request, "Profile Details Updated")
			context['success_message'] = "Updated"
			redirect('account_edit')
	else:
		form = AccountUpdateForm(
			initial={
				"name": request.user.name,
				"email": request.user.email,
				"username": request.user.username,
				"bio": request.user.bio, 
				"profile_picture": request.user.profile_picture,
				
			}
		)
	context['account_form'] = form
	context['response'] = response

	return render(request, 'account/edit_account.html', context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def follow_view(request,  slug):


	user_to_follow = get_object_or_404(Account, slug=slug)
	user = request.user

	if user_to_follow.account_type == 'public':
	
		create = Connection.objects.get_or_create(
			followers=user_to_follow,
			following=user,
			)
		generate_request_notification = Notification.objects.get_or_create(notification_type='following',user=user_to_follow, notification_by=user)
		messages.success(request, f'Followed {user_to_follow}.')

	elif user_to_follow.account_type == 'private':
		request = Request.objects.get_or_create(
			request_by=user,
			target_user=user_to_follow
		)
		generate_request_notification = Notification.objects.get_or_create(notification_type='request',user=user_to_follow, notification_by=user)

	return redirect('account_detail', slug=slug)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unfollow_view(request, slug):

	user_to_unfollow = get_object_or_404(Account, slug=slug)
	user = request.user

	try:
		request = Request.objects.get(
			request_by=user,
			target_user=user_to_unfollow
		)
		request.delete()
		get_request_notification = Notification.objects.get(notification_type='request',user=user_to_unfollow, notification_by=user)
		get_request_notification.delete()
	except Request.DoesNotExist:
		unfollow = Connection.objects.filter(
			followers=user_to_unfollow,
			following=user
		)
		get_follow_notification = Notification.objects.get(notification_type='following',user=user_to_unfollow, notification_by=user)
		get_follow_notification.delete()
		unfollow.delete()

	# if user_to_unfollow.account_type == 'public':
	# 	unfollow = Connection.objects.filter(
	# 		followers=user_to_unfollow,
	# 		following=user
	# 	)
	# 	get_follow_notification = Notification.objects.get(notification_type='following',user=user_to_unfollow, notification_by=user)
	# 	get_follow_notification.delete()
	# 	unfollow.delete()
	# 	messages.success(request, f'Unfollowed {user_to_unfollow}.')
	
	# elif user_to_unfollow.account_type == 'private':
	# 	request = Request.objects.get(
	# 		request_by=user,
	# 		target_user=user_to_unfollow
	# 	)
	# 	request.delete()
	# 	get_request_notification = Notification.objects.get(notification_type='request',user=user_to_unfollow, notification_by=user)
	# 	get_request_notification.delete()
	return redirect('account_detail', slug=slug)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def request_view(request, slug):
# 	user = request.user
# 	user_profile = get_object_or_404(Account, slug=slug)


# 	try:
# 		request = Request.objects.get(
# 			request_by=user,
# 			target_user=user_profile
# 		)
# 		request.delete()
# 		get_request_notification = Notification.objects.get(notification_type='request',user=user_profile, notification_by=user)
# 		get_request_notification.delete()
# 	except Request.DoesNotExist:
# 		request = Request.objects.get_or_create(
# 			request_by=user,
# 			target_user=user_profile
# 		)
# 		generate_request_notification = Notification.objects.create(notification_type='request',user=user_profile, notification_by=user)
# 	return redirect('account_detail', slug=slug)


def request_confirm_view(request, slug):
	user = request.user
	user_profile = get_object_or_404(Account, slug=slug)

	request = Request.objects.get(
			request_by=user_profile,
			target_user=user
		)
	request.delete()
	create = Connection.objects.get_or_create(
		followers=user,
		following=user_profile,
		)
	request_notification = Notification.objects.get(notification_type='request', user=user, notification_by=user_profile)
	request_notification.notification_type='following'
	request_notification.save()
	return redirect('account_detail', slug=slug)


def request_cancel_view(request, slug):
	user = request.user
	user_profile = get_object_or_404(Account, slug=slug)

	request = Request.objects.get(
			request_by=user_profile,
			target_user=user
		)
	request.delete()
	request_notification = Notification.objects.get(notification_type='request', user=user, notification_by=user_profile)
	request_notification.delete()
	return redirect('account_detail', slug=slug)


def followers_view(request, slug):
	context = {}

	user_profile = get_object_or_404(Account, slug=slug)
	followers = Connection.objects.filter(
		followers=user_profile
	)

	context['users'] = followers
	context['response'] = "Followers"

	return render(request, 'account/connection.html', context)

def following_view(request, slug):
	context = {}

	user_profile = get_object_or_404(Account, slug=slug)
	following = Connection.objects.filter(
		following=user_profile
	)

	context['users'] = following
	context['response'] = "Following"

	return render(request, 'account/connection.html', context)

def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		accounts = Account.objects.filter(
				Q(username__icontains=q) |
				Q(name__icontains=q)
			).distinct()

		for account in accounts:
			queryset.append(account)

	return list(set(queryset))