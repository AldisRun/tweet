from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.notification.utilities import create_notification

from.forms import TweeterProfileForm

def tweeterprofile(request, username):
    user = get_object_or_404(User, username=username)
    tweets = user.tweets.all()

    for tweet in tweets:
        likes = tweet.likes.filter(created_by_id=request.user.id)
        if likes.count() > 0:
            tweet.liked = True
        else:
            tweet.liked = False

    context = {
        'user': user,
        'tweets': tweets,
    }

    return render(request, 'tweeterprofile/tweeterprofile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = TweeterProfileForm(request.POST, request.FILES, instance=request.user.tweeterprofile)
        if form.is_valid():
            form.save()
            return redirect('tweeterprofile', username=request.user.username)
    else:
        form = TweeterProfileForm(instance=request.user.tweeterprofile)

    context = {
        'user': request.user,
        'form': form,
    }

    return render(request, 'tweeterprofile/edit_profile.html', context)

@login_required
def follow_tweeter(request, username):
    user = get_object_or_404(User, username=username)

    request.user.tweeterprofile.follows.add(user.tweeterprofile)

    create_notification(request, user, 'follower')

    return redirect('tweeterprofile', username=username)

@login_required
def unfollow_tweeter(request, username):
    user = get_object_or_404(User, username=username)

    request.user.tweeterprofile.follows.remove(user.tweeterprofile)

    return redirect('tweeterprofile', username=username)

def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'tweeterprofile/followers.html', {'user': user})

def follows(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'tweeterprofile/follows.html', {'user': user})