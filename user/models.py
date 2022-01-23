#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

#장고가 관리하는 setting에서 들고옴. spartDajngo 안에 setting


#AbstractUser는 장고가 제공하는 기본적인 auth유저 와 연동되는 클래스임.
# Create your models here.
class UserModel(AbstractUser): #abstractUSer모델 상속함.
    #이 유저모델에는 모든 정보가 들어가 있음. 아이디 비밀번호 등등등
    class Meta:
        db_table = "my_user"
        # Meta클래스는 데이터베이스에 이름을 지정해 주는 정보라고 할수있음.
    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    #setting안에있는 auth_user_model (우리모델을 many to many filed로 하겠다)
    # follow : 내가 팔로우할 사용자를 넣어놓음. followee는 유저모델을 팔로우 하는 사람들을 넣어줌