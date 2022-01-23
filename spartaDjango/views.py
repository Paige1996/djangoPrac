from django.http import HttpResponse
from django.shortcuts import render



#""안에 있는 친구를 전달하는 거임


def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")

def first_view(request):
    return render(request, 'my_test.html')