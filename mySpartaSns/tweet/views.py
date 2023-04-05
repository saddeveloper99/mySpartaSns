from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from .models import TweetModel, TweetComment
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')
        
    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')

        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '글은 공백일 수 없습니다', 'tweet': all_tweet})
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '': 
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')

            # my_tweet = TweetModel()
            # my_tweet.author = user
            # my_tweet.content = request.POST.get('my-content', '')
            # my_tweet.save()
            # return redirect('/tweet')

@login_required
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')

# my_tweet = TweetModel.objects.get(id=id)
# tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)

def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    all_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet':my_tweet, 'comment': all_comment})

def write_comment(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    my_comment = TweetComment()
    user = request.user
    my_comment.author = user
    my_comment.tweet = my_tweet
    my_comment.comment = request.POST.get('comment', '')
    my_comment.save()
    return redirect('/tweet/' + str(id))

def delete_comment(request, id):
    my_comment = TweetComment.objects.get(id=id)
    my_comment.delete()
    return redirect('/tweet/' + str(my_comment.tweet_id))

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