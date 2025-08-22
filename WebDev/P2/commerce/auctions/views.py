from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Max
from .models import User, Category, Watchlist, Bid, Auction, Comment


### helper functions ###
def get_listing(listing_id):
    return Auction.objects.get(pk=listing_id)


def check_bid(bid, starting_price, highest_bid):
    if bid < starting_price:
        return False
    elif highest_bid:
        if bid < float(highest_bid): 
            return False
        else:
            return True
    else:
        return True


### view functions ###
def index(request):
    title="Active Listings"
    listings = Auction.objects.filter(active=True).annotate(
        highest_bid = Max('bidding__amount')
    )

    return render(request, "auctions/index.html", {
        "title": title, 
        "listings": listings
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


@login_required
def add_listing(request):
    if request.method == "POST":
        new_listing = Auction(
            title = request.POST.get("title"), 
            description = request.POST.get("description"), 
            starting_price = request.POST.get("starting_bid"),
            listed_by = request.user
        )

        if request.POST.get("img_url") != "":
            new_listing.img_url = request.POST.get("img_url")
        if request.POST.get("category"):
            new_listing.category = Category.objects.get(name=request.POST.get("category"))

        new_listing.save()
        return HttpResponseRedirect(reverse('index'))
    
    else:
        return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


def auction_listing(request, listing_id, error=False, bid_amt = 0):
    listing = get_listing(listing_id)
    highest_bid = Bid.objects.filter(item=listing).order_by('-amount').first()
    bid_count = Bid.objects.filter(item=listing).count()

    comments = Comment.objects.filter(item=listing)
    comment_count = comments.count()
    if request.user.id:
        watchlist = Watchlist.objects.filter(user=request.user, item=listing).exists()
    else:
        watchlist = None


    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "highest_bid": highest_bid, 
        "bid_count": bid_count,
        "watchlist": watchlist, 
        "comments": comments,
        "comment_count": comment_count, 
        "error": error, 
        "bid_amt": bid_amt
    })


@login_required
def add_watchlist(request, listing_id):
    watchlist = Watchlist(
        user = request.user, 
        item = get_listing(listing_id)
    )
    watchlist.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        wl_user = request.user
        wl_item = get_listing(listing_id)

        watchlist_lst = Watchlist.objects.filter(user=wl_user, item=wl_item)
        for watchlist in watchlist_lst:
            watchlist.delete()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        bid = float(request.POST.get("bid"))
        listing = get_listing(listing_id)
        highest_bid_amt = Bid.objects.filter(item=listing).aggregate(Max('amount'))['amount__max']
        user = request.user
        print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        print(f"Bid amount: {bid}, Highest bid: {highest_bid_amt}")

        if check_bid(bid, listing.starting_price, highest_bid_amt):
            new_bid = Bid(
                bidder = user, 
                item = listing, 
                amount = bid
            )
            new_bid.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        else:
            return auction_listing(request, listing_id, error=True, bid_amt = bid)
    else:
        return auction_listing(request, listing_id, error=False)


@login_required
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = get_listing(listing_id)
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse('listing', args=[listing_id]))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def category_listings(request, cat_id):
    title = "Category: " + Category.objects.get(pk=cat_id).name
    listings = Auction.objects.annotate(
        highest_bid = Max("bidding__amount")
    ).filter(category=cat_id)

    return render(request, "auctions/index.html", {
        "title": title, 
        "listings": listings
    })

@login_required
def watchlist(request):
    title = "Watchlist"
    watchlist_lst = Watchlist.objects.filter(user=request.user)
    listings = Auction.objects.annotate(
        highest_bid = Max("bidding__amount")
    ).filter(wishlist_item__in=watchlist_lst)

    return render(request, "auctions/index.html", {
        "title":title, 
        "listings": listings
    })

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        new_comment = request.POST.get("comment")

        new_comment_object = Comment(
            user = request.user, 
            item = get_listing(listing_id),
            comment = new_comment
        )
        new_comment_object.save()

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))