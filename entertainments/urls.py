from django.urls import path
from . import views
from .views import Like_comment

app_name = 'entertainments'
urlpatterns = [
    
     path('', views.Enter_post_list, name='entertainment_post_list'),
     path('all_entertainment_posts_view', views.list_load_Entertainment_posts_view, name='all_entertainment_posts_view'),
     path('likes/<int:pk>/', views.like_post, name="post-like"),
     path('create_entertainment_post/', views.Create_Post,name='create_post'),
     path('<int:year>/<int:month>/<int:day>/<slug:post>/',         
          views.post_detail,         
          name='post_detail'),

    path('tag/<slug:tag_slug>/', views.Enter_post_list, name='post_list_by_tag'),

    path('<int:post_id>/share/',         
          views.post_share, name='post_share'),

    path('<int:post_id>/comment/',         
           views.post_comment, name='post_comment'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('<int:pk>/edit-comment/', views.Update_Comment, name='edit-comment'),
    path('edit_post/<int:pk>', views.Update_Post, name='edit_post'),
    path('delete/<int:pk>', views.delete_post, name='post-delete'),
    path('delete/<int:pk>', views.delete_comment, name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like',  Like_comment.as_view(), name='comment-like'),

   
]