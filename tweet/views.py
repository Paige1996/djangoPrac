from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel
from .models import TweetComment
from django.contrib.auth.decorators import login_required

#트윗 모델을 들고온다
# login_required.: 로그인이 되어있어야만 어떤 함수를 실행할 수 있음

# Create your views here.

def home(request):
    user = request.user.is_authenticated
    #HOEM이라는 함수를 실행시키는 것 만으로도 사용자가 로그인 되어있는지 안되있는지 알 수있음
    if user: #이 사용자가 있으면
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request): #tweet안에 Home.html을 보여주는 함수
    if request.method == 'GET': #보여주니까 당연히 get
        user = request.user.is_authenticated #지금 유저가 로그인 되어있는 가.
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            #tweetModel.objects.all() 트윗 모델에 저장한 모든 데이터를 불러오겠다
            #order_by('-created_at') 생성된 것을 역순 (마이너스로 함) 으로 불러오고 이것을 all_tweet으로 묶음
            return render(request,'tweet/home.html', {'tweet' :all_tweet})
        #그렇게 묶은 all_tweet을 tweet/home안에 딕셔너리 형태로 넣어줌. 이 데이터의 키값은 tweet임
        else:
            return redirect('/sign-in')
    elif request.method =='POST':
        user = request.user #지금 로그인 되어있는 사용자 정보를 들고와서
        content = request.POST.get('my-content','')
        tags = request.POST.get('tag','').split(',')
        if content == '':
            #콘텐츠가 아무것도 없이 저장을 눌렀으면
            all_tweet = TweetModel.objects.all().order_by('-created_at') #현재 있는 모든 트윗을 보여주고
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다!', 'tweet': all_tweet})
                                #현재있는 모든 트윗을 보여줌과 똥시에 에러 메시지를 보여준다
        else: #공백이 아니라면
            my_tweet = TweetModel.objects.create(author=user, content=content)
            # user = request.user 유저와 콘텐츠를 만들어 my_tweet으로 묶고
            for tag in tags: #my_tweet은 TweetModel안에 tag를 가지고 있음.
                tag = tag.strip() #태그의 공백을 제거해줌
                if tag != '': #만약 태그가 없다면
                    my_tweet.tags.add(tag) #추가
                    # my_tweet은 TweetModel안에 tag를 가지고 있음. 그 값들을 넣어 추가함
            my_tweet.save() #my_tweet을 저장한다.
            return redirect('/tweet')

@login_required()#로그인 한 사람만 삭제할 수있다록
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id) #그 게시글을 들고와서
    my_tweet.delete() #장고가 제공하는 기능인 삭제를 넣고
    return redirect('/tweet') #다시 트윗으로 돌아가기

@login_required()
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id) #트윗 모델 id를 my_tweet으로 묶어서
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at') #그 트윗 아이디만 필터를 한뒤 그 트윗 아이디에대한 댓글을 내림차순으로 정렬하고 tweet_comment로 묶고
    return render(request, 'tweet/tweet_detail.html', {'tweet':my_tweet, 'comment': tweet_comment})
                        #딕셔너리 형태로 my_tweet과 tweet_comment로 tweet_detail.html에 쏴준다.

@login_required()
def write_comment(request, id):
    if request.method =='POST':
       comment = request.POST.get("comment","")
       current_tweet = TweetModel.objects.get(id=id)

       TC = TweetComment()
       TC.comment = comment
       TC.author = request.user
       TC.tweet = current_tweet
       TC.save()

       return redirect('/tweet/' + str(id))
       #그 트윗에 대한 id

@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/'+str(current_tweet))



#아래는 장고 taggit이라는 공식 웹사이트에서 제공하는 도큐먼트로써 이거 복붙 그냥 하면 됨
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context