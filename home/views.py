from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from post.models import Post
from account.models import Account
from post.views import get_post_queryset
from operator import attrgetter
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


BLOG_POST_PER_PAGE = 10

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_screen_view(request):
	context = {}

	query = ""

	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("home_screen_view: " + str(query))

	posts = sorted(get_post_queryset(query), key=attrgetter('date_updated'), reverse=True)
	

	#Pagination
	page = request.GET.get('page', 1)
	posts_paginator = Paginator(posts, BLOG_POST_PER_PAGE)

	try:
		posts = posts_paginator.page(page)
	except PageNotAnInteger:
		posts = posts_paginator.page(BLOG_POST_PER_PAGE)
	except EmptyPage:
		posts = posts_paginator.page(blog_posts_paginator.num_pages)

	user = request.user
	
	context['user'] = user

	context['authenticated'] = True
	context['posts'] = posts
	context['accounts'] = Account.objects.all()
	return render(request, 'home/home.html' , context)
