from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_home/', views.user_home, name='user_home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile_completion/', views.profile_completion, name='profile_completion'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]