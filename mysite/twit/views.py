from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet, Like, Comment, Share
from .forms import TweetForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse

# Homepage view
def index(request):
    if request.user.is_authenticated:
        return redirect('tweet_list')
    else:
        return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    return render(request, 'tweet_list.html', {'tweets': tweets, 'comment_form': comment_form})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)  # handle file upload
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'tweet_edit.html', {'form': form, 'tweet': tweet})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_delete_confirm.html', {'tweet': tweet})

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': tweet.likes.count()})

@login_required
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            return redirect('tweet_list')
    return redirect('tweet_list')

@login_required
def share_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    Share.objects.create(user=request.user, tweet=tweet)
    return redirect('tweet_list')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    
    return render(request,
                  'registration/register.html',
                  {'form': form})
