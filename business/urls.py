from django.urls import path
from . import views
from .views import Like_comment, Dislike_comment


app_name = 'business'
urlpatterns = [
      path('', views.post_list, name='business_post_list'),
     path('create_business_post/', views.Create_Post,name='create_post'),
     path('all_business_posts_view', views.list_load_business_posts_view, name='all_business_posts_view'),
     path('like/<int:id>', views.like_post, name='like_post'),

     path('<int:year>/<int:month>/<int:day>/<slug:post>/',         
          views.post_detail,         
          name='post_detail'),

    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    path('<int:post_id>/share/',         
          views.post_share, name='post_share'),

    path('htmx/post_comment/<int:post_id>',    views.post_comment, name='post_comment'),
    #path('comment/<int:id>/like', views.like_comment, name='like_comment'),
    path('post/<int:post_pk>/comment/<int:pk>/like',  Like_comment.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike',  Dislike_comment.as_view(), name='comment-dislike'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('<int:pk>/edit-comment/', views.Update_Comment, name='edit-comment'),
    path('edit_post/<int:pk>', views.Update_Post, name='edit_post'),
    path('edit_comment/<int:pk>', views.Update_Comment, name='edit_comment'),
    path('delete/<int:pk>', views.delete_post, name='post-delete'),
    path('delete/<int:pk>', views.delete_comment, name='comment-delete'),
   
    
]