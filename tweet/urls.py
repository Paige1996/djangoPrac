# tweet/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path가 아무것도 없을때 (즉 그냥 127.0.0.1:8000일때 view.py폴더 안의 home을 보여주고
    # ( 127.0.0.1:8000 과 views.py 폴더의 home 함수 연결)
    path('tweet/', views.tweet, name='tweet'),
    # path가 아무것도 없을때 (즉 그냥 127.0.0.1:8000/tweet 일때 view.py폴더 안의 twet를 연결
    # 127.0.0.1:8000/tweet 과 views.py 폴더의 tweet 함수 연결
    path('tweet/delete/<int:id>', views.delete_tweet, name='delete-tweet'),
    # 127.0.0.1:8000/tweet/delete/그 글의 특정 id 일때 view.py폴더 안의 delete_tweet함수로 연결해줌
    path('tweet/<int:id>', views.detail_tweet, name='detail-tweet'),
    path('tweet/comment/<int:id>', views.write_comment, name='write-comment'),
    path('tweet/comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
]
