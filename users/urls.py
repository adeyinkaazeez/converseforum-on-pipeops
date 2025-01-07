from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import login, logout, authenticate
from .views import ResetPasswordView, Subscribe


urlpatterns = [
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('my_dashboard/', views.dashboard, name='dashboard'),
path('logout/', views.logout_view, name='logout'),
path('password-change/', views.password_change_view, name='change_password'),
path('password-change/done/',
                             views.PasswordChangeDoneView,
                             name='password_change_done'),
path('activate/<uidb64>/<token>', views.activate, name='activate'),
path('edit/', views.edit, name='edit'),
path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

path('my_activities/', views.my_activities, name='my_activities'),
path('post_author/<int:pk>', views.Author_Profile_View, name='post_author' ),
path('subscribe', views.Subscribe, name='subscribe'),
path('users/follow/<int:id>', views.user_to_follow, name='user_follow'),
path('author/<username>/', views.search_for_author, name='search_author'),
path('all_my_comment/', views.load_all_my_commenting_activites, name="load_all_my_comments"),
path('all_my_posting/', views.load_all_my_posting_activities, name="load_all_my_posting"),



]