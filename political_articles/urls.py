from django.urls import path
from . import views
from .views import Like_comment

app_name = 'political_articles'
urlpatterns = [
       path('', views.post_list, name='political_post_list'),
       path('all_political_article_posts_view', views.list_load_Political_Article_posts_view, name='all_political_article_posts_view'),
      path('create_political_article/', views.Create_Post,name='create_post'),
       path('likes/<int:pk>/', views.like_post, name="post-like"),
        path('edit_post/<int:pk>', views.Update_Post, name='edit_post'),
     path('delete/<int:pk>', views.delete_post, name='post-delete'),
     path('<int:year>/<int:month>/<int:day>/<slug:post>/',         
          views.post_detail,         
          name='post_detail'),

    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    path('<int:post_id>/share/',         
          views.post_share, name='post_share'),

    path('<int:post_id>/comment/',         
           views.post_comment, name='post_comment'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('<int:pk>/edit-comment/', views.Update_Comment, name='edit-comment'),
    path('post/<int:post_pk>/comment/<int:pk>/like',  Like_comment.as_view(), name='comment-like'),
    path('delete/<int:pk>', views.delete_comment, name='comment-delete'),
   
]