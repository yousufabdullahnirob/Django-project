from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('tweets/', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('<int:tweet_id>/comment/', views.add_comment, name='add_comment'),
    path('<int:tweet_id>/share/', views.share_tweet, name='share_tweet'),
]


