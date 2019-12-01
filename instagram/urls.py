"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from home.views import home_screen_view

from account.views import (
    registration_view,
    login_view,
    logout_view,
    must_authenticate_view,
    account_view,
    edit_account_view,
    follow_view,
    unfollow_view,
    followers_view,
    following_view,
    request_confirm_view,
    request_cancel_view,
)

urlpatterns = [
    path('', home_screen_view, name="home"),
    path('admin/', admin.site.urls),
    path('register/', registration_view , name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('<slug>/', account_view, name="account_detail"),
    path('account/edit/', edit_account_view, name="account_edit"),
    path('<slug>/request/confirm', request_confirm_view, name="confirm_request"),
    path('<slug>/request/cancel', request_cancel_view, name="cancel_request"),
    path('<slug>/follow', follow_view, name="follow"),
    path('<slug>/unfollow', unfollow_view, name="unfollow"),
    path('<slug>/followers', followers_view, name="followers"),
    path('<slug>/following', following_view, name="following"),
    path('p/', include('post.urls', 'post')),
    path('c/', include('chat.urls', 'chat')),
    
    path('explore/', include('explore.urls', 'explore')),
    path('activity/', include('activity.urls', 'activity')),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
    # path(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    # path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

]
urlpatterns += re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
    # path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),


    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),