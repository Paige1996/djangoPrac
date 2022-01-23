from django.shortcuts import render, redirect
from .models import UserModel
from django.http import HttpResponse
from django.contrib.auth import get_user_model #사용자가 데이터베이스 안에 있는지 검사하는 함수
from django.contrib import auth
from django.contrib.auth.decorators import login_required

#httpResponse. 화면 상단에 글자를 띄울때 추가한다. 로그인이 성공한다면 로그인 성공이라는 메시지를 띄움
#login_requeired 는 로그아웃했을때


#render를  통해 html 파일을 화면에 보여주게 한다.라는 뜻

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':  # 화면에서 장고 서버로 요청이 가는데, 장고가 확인을 하게 되는데
        # 요청하는 방식이 get이면
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    # user/signup.html이라는 파일을 render즉 보여준다ㅏ. 여기서 회원이 회원가입 하는 것임.

    elif request.method == 'POST':  # 사용자가 수정 삭제 등을 했을경우 포스트로 받아와야하니까... 그리고 이건 html의 method에도 추가돼잉ㅆ음음
        username = request.POST.get('username', '') #none이 아니라 ''으로 표시하게됨
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

    if password != password2  :
        return render(request, 'user/signup.html', {'error': '패스워드를 확인해 주세요!'})
        # 두개가 다르면 다시 signup화면으로 보여달라는 듯. 그리고 에러 모습도 보여주기. 이 error 딕셔너리 형태는 html도 적어얗함
    else:
        if username == '' or password == '': #유저가 유저네임이나 비번을 아무것도 안적었다면
            return render(request, 'user/signup.html', {'error': '사용자 이름과 비번은 필수다!'})
        exist_user = get_user_model().objects.filter(username=username) #만약에 저장된 유저이름이 같은 이름이 있다면.
        if exist_user:
            return render(request, 'user/signup.html', {'error':'사용자가 존재합니다!'}) #다시 돌아오고, 사용자가 존재한다는 에러 메시지를 보냄

        else:  # 패스워드가 다 같고 유저이름이 다르다면
            UserModel.objects.create_user(username=username, password=password, bio=bio)
            return redirect('/sign-in')
            # 이렇게 저장되면 바로 /sign-in 페이지로 간다


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '') #유저네임,페스워드를 받아와서

        me = auth.authenticate(request, username=username, password=password)
        #암호화된 비밀번호와 현재 비밀번호가 일치 하는지, 사용자와 맞는지 확인 일치하는것에 me라는 변수에 넣어줌
        if me is not None: #사용자가 비어있는지 없는지만 구분해줌
            auth.login(request, me)
            return redirect('/') #/라는 기본 url로 넘어가게 됨. tweet클래스안에 urls에 있는 ''로 넘어
        else:
            return render(request, 'user/signin.html', {'error': '유저 이름 패스워드 확인해주세요!'})
    elif request.method == 'GET': #요청이 겟이라면
        user = request.user.is_authenticated #유저가 로그인 했는데도불구하고 sign-in을 누르면 sign-i페이지가 나옴. 그러면
        #안되므로..
        if user: #만약 유저가 있다면
            return redirect('/')
        else: #아니라면
            return render(request, 'user/signin.html') #화면을 보여줌감

@login_required #사용자가 꼭 로그인이 되어있어야만 적용되는 함수
def logout(request):

    auth.logout(request) #장고의 로그아웃 기능
    return redirect('/')


# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        # 내 username 만 빼고 usermodel 모두를 user_list로 묶겠다
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user #로그인한 유저. 나를 me로 묶고
    click_user = UserModel.objects.get(id=id) #내가 방금 누른 사람
    if me in click_user.followee.all():
        #내가 방금 누른 사람. 그사람을 팔로우하는 모든 사람들 데려 와서, 그 중에 내가 있다면
        click_user.followee.remove(request.user) #나를 빼주고 (팔로우 취소가 됨)
    else:
        click_user.followee.add(request.user) # 내가 없다면 팔로우 하게됨.
    return redirect('/user')