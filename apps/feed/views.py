from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Tweet

@login_required
def feed(request):
    userids = [request.user.id]

    for tweeter in request.user.tweeterprofile.follows.all():
        userids.append(tweeter.user.id)

    tweets = Tweet.objects.filter(created_by_id__in=userids)

    for tweet in tweets:
        likes = tweet.likes.filter(created_by_id=request.user.id)
        if likes.count() > 0:
            tweet.liked = True
        else:
            tweet.liked = False

    return render(request, 'feed/feed.html', {'tweets': tweets})

@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        tweeters = User.objects.filter(username__icontains=query)
        tweets = Tweet.objects.filter(body__icontains=query)
    else:
        tweeters = []
        tweets = []

    context = {
        'query': query,
        'tweeters': tweeters,
        'tweets': tweets,
    }

    return render(request, 'feed/search.html', context)