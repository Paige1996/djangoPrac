from django.contrib import admin
from .models import UserModel

#setting에서 admin을 생성했다
#.models는 우리와 동일하게 있는 위치의 파일인 models 파일중에 class의 UserModel을 불러오겠다는 뜻임


# Register your models here.
admin.site.register(UserModel)
#우리가 들고온 UserModel을 관리자 계정에 넣어주겠다 라는 얘기.

# 이 코드가 나의 UserModel을 Admin에 추가 해 줍니다