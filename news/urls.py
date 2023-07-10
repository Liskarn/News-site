from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.post_list, name='post_list'),  # List of posts
    path('post/new/', views.post_new, name='post_new'),  # Create a new post
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='post_list.html'), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('post/<int:pk>/upvote/', views.upvote, name='upvote'),
    # path('post/<int:pk>/comment/', views.add_comment, name='add_comment'), # remove this line
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]