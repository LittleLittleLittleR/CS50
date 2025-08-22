import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Following, Comment

### Helper functions

def get_followers_count(user_id):
    # Get the number of followers for the user
    return Following.objects.filter(following__id=user_id).count()

def get_following_count(user_id):
    # Get the number of users that the given user is following
    return Following.objects.filter(user__id=user_id).count()

def get_likes_count(post_id):
    # Get the number of likes for the given post
    return Like.objects.filter(post__id=post_id).count()

def check_following(login_user, profile_user):
    # Check if the login user is following the profile user
    if Following.objects.filter(user__id=login_user, following__id=profile_user):
        return True
    else:
        return False

def get_post_page(user_id=None, page_no=1):
    posts_data = []
    if user_id:
        posts = Post.objects.filter(user__id__in=user_id).order_by("-datetime") # Fetch posts in descending order of creation
    else:
        posts = Post.objects.all().order_by("-datetime")  

    for post in posts:
        likes_count = get_likes_count(post.id)  # Using the helper function

        posts_data.append({
            "id": post.id, 
            "user": {
                "id": post.user.id,  # Include user.id
                "username": post.user.username  # Include user.username
            },
            "content": post.content,
            "datetime": post.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "likes_count": likes_count,
        })

    post_pages = Paginator(posts_data, 10)
    post_page = post_pages.page(page_no).object_list
    
    return post_page, post_pages.num_pages, list(post_pages.page_range)
### Views functions

def index(request):
    post_page, page_count, page_list = get_post_page()

    return render(request, "network/index.html", {
        "post_page": post_page,
        "page_no": 1, 
        "page_count": page_count,
        "page_list": page_list,
        "filter": "index"
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
    
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    followers_count = get_followers_count(user_id)
    following_count = get_following_count(user_id)
    post_page, page_count, page_list = get_post_page(user_id=[user_id])

    if request.user.id != user_id:
        is_following = check_following(request.user.id, user_id)
    else:
        is_following = None

    return render(request, "network/profile.html", {
        "profile_user": user,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "post_page": post_page,
        "page_no": 1, 
        "page_count": page_count, 
        "page_list": page_list
        })  
    
@login_required
def new_post(request):
    return render(request, "network/new_post.html") 

@login_required
def create_post(request):
    new_post = Post(
        user = request.user,
        content = request.POST.get("content")
    )
    new_post.save()

    return HttpResponseRedirect(reverse('index'))

@login_required
def following(request):
    user_id = request.user.id
    following_ids = list(Following.objects.filter(user_id=user_id).values_list("following_id", flat=True))
    
    post_page, page_count, page_list = get_post_page(user_id=following_ids)

    return render(request, "network/index.html", {
        "post_page": post_page,
        "page_no": 1, 
        "page_count": page_count, 
        "page_list": page_list,
        "filter": "following"
        })

@csrf_exempt
def follow_user(request, user_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        try:
            target_user = User.objects.get(id=user_id)

            # Check if following relationship already exists
            existing_follow = Following.objects.filter(user=request.user, following=target_user)

            if existing_follow.exists():
                existing_follow.delete()  # Unfollow
                isFollowing = False
            else:
                Following.objects.create(user=request.user, following=target_user)  # Follow
                isFollowing = True

            return JsonResponse({"success": True, "isFollowing": isFollowing})

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)

def fetch_page(request, filter, page_no):
    user_id = request.user.id

    if filter == "index":
        post_page, page_count, page_list = get_post_page(page_no=page_no)
    elif filter == "following":
        following_ids = list(Following.objects.filter(user_id=user_id).values_list("following_id", flat=True))
        post_page, page_count, page_list = get_post_page(page_no=page_no, user_id=following_ids)

    return JsonResponse({
        "user_id": user_id,
        "post_page": post_page,
        "page_no": page_no, 
        "page_count": page_count,
        "page_list": page_list,
    })

def fetch_profile_page(request, profile_id, page_no):
    post_page, page_count, page_list = get_post_page(page_no=page_no, user_id=[profile_id])
    user_id = request.user.id
    

    return JsonResponse({
        "user_id": user_id,
        "post_page": post_page,
        "page_no": page_no, 
        "page_count": page_count,
        "page_list": page_list,
    })

def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post = Post.objects.get(id=post_id)

        post.content = data["content"]
        post.save()
        
        return JsonResponse({"success": True})
        
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def like_post(request, post_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=401)

        try:
            post = Post.objects.get(id=post_id)
            # Check if like relationship already exists
            existing_like = Like.objects.filter(user=request.user, post=post)

            if existing_like.exists():
                existing_like.delete()  # Unlike
                isLiked = False
            else:
                Like.objects.create(user=request.user, post=post)  # Like
                isLiked = True

            return JsonResponse({"success": True, "isLiked": isLiked})

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)