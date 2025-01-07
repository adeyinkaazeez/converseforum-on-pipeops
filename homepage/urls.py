from django.urls import path
from . import views
from .feeds import LatestPostsFeed

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('business_home/', views.list_load_business_posts_view, name='business_home'),
    path('politics_home/', views.list_load_politics_posts_view, name='politics_home'),
    path('search/', views.search_view, name='search_view'),
    path('search/results/', views.search_results_view, name='search_results_view'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('subscribe/', views.newsLetter, name="newsletter" ),
]