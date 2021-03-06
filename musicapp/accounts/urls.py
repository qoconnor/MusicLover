from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView

app_name="users"

urlpatterns = [
    url(r'^$', views.home),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name="logout"),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile_pic/', views.upload_pic, name='upload_pic'),
    path('create_post/', views.create_post, name='create_post'),
    url(r'^view_post/(?P<pk>\d+)/$', views.view_post, name='view_post'),
    url(r'^remove_post/(?P<pk>\d+)/$', views.remove_post, name='remove_post'),
    url(r'^create_comment/(?P<pk>\d+)/$', views.create_comment, name='create_comment'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('popular/', views.popular, name='popular'),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
