from datetime import timezone
import json;
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Subquery
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.management.base import CommandError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Follower
import datetime

def index(request):
    return render(request, "network/index.html")


#Save post
@csrf_exempt
@login_required
def createPost(request):
    if (request.method != 'POST'):
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # get content post
    data = json.loads(request.body)
    content = data["content"]
    date = datetime.datetime.now(tz=timezone.utc)

    # Save post data
    try: 
        post = Post(
            content = content,
            created_by = request.user,
            created_date = date
        )

        post.save()
    except IntegrityError:
            # already been created because we got IntegrityError
            raise CommandError("Post not saved")

    return JsonResponse({"message": "Post created successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required(login_url='/login')
def getProfile(request, profile_id):
    try:
        profile = User.objects.get(pk=profile_id)
        following = profile.following.count()
        followersCount = profile.followers.count()
        posts = Post.objects.filter(created_by=profile.id).all().order_by('-created_date')
        is_followed = profile.followers.filter(following_id = profile_id).exists()
        # Add pagination for page profile
        paginator= Paginator(posts, 10);
        page_number = request.GET.get('page')
        post_page = paginator.get_page(page_number)

    except User.DoesNotExist:
        raise CommandError("Post not saved")
    
    return render(request, "network/profile.html", {
        "profile": profile, 
        "following": following,
        "followers" : followersCount,
        "is_followed": is_followed,
        "posts": post_page
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def getPostList(request):
    posts = Post.objects.all().order_by('-created_date')
    paginator= Paginator(posts, 10);

    page_number = request.GET.get('page')
    post_page = paginator.get_page(page_number)

    return render(request, "network/post.html", {
        "posts": post_page
    })

def following(request):
    following  = Follower.objects.filter(follower_id = request.user.id).values('following')
    posts = Post.objects.filter(created_by__in=Subquery(following))

    paginator= Paginator(posts, 10);

    page_number = request.GET.get('page')
    post_page = paginator.get_page(page_number)

    return render(request, "network/post.html", {
        "posts": post_page
    })

@csrf_exempt
@login_required
def updatePost(request):
    if (request.method != 'POST'):
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content = data["content"]

    try:
        post = Post.objects.get(pk=content['id'])
        if (post is not None):
            post.content = content['post']
            post.save()

    except Post.DoesNotExist:
        raise CommandError("Post not existed")

    return JsonResponse({"message": "Post updated successfully."}, status=201)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
