from django.urls import path
from . import views


urlpatterns = [

    path('', views.post_list, name='post_list'),    
    path('api', views.PostList.as_view()),
    path('api/<int:pk>/', views.PostDetail.as_view()),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/mypost/',views.get_user_Posts,name='get_my_posts'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/Liked/', views.add_Likes, name='add_Likes'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    
]