from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.post_list, name='post_list'),  # List of posts
    path('post/new/', views.post_new, name='post_new'),  # Create a new post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Detail view for a post
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  # User registration
    path('post/<int:pk>/upvote/', views.upvote, name='upvote'),
    path('post/<int:pk>/downvote/', views.downvote, name='downvote'),
    
]