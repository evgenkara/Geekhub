from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.activate, name='activate'),
    path('login/', views.user_login, name='login'),
    path('password-change/', views.change_password, name='password_change'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('signup/', views.signup, name='signup'),
    path('ratings/', views.ratings, name='ratings'),
    path('watchlist/', views.watchlist, name='watchlist'),
]
