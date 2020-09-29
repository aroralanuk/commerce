from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Catergory, WatchList, Bid


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
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

def displayListing(request, item_id):
    user = request.user.id
    item = Listing.objects.get(id=item_id)
    try:
        highestBid = Bid.objects.filter(listing_id=item_id).order_by('-amt').first()
    except:
        highBid = item.minPrice
    comments = Comment.objects.filter(listing_id=item_id)
    watchlisted = WatchList.objects.filter(user_id=user,listing_id = item).exists()
    return render(request,"auctions/entry.html",{
        "item": item,
        "bid": highestBid,
        "comments": comments,
        "watchlisted": watchlisted
    })

def toggleWL(request):
    if request.method == 'POST':
        try:
            item = Listing.objects.get(id=request.POST['watchlist'])
            watchlisted = WatchList.objects.filter(user=request.user).get(listing_id=item)
            watchlisted.delete()
        except:
            newEntry = WatchList(listing_id=request.POST['watchlist'],user=request.user)
            newEntry.save()
        return HttpResponseRedirect(reverse("listing",
        args=[request.POST["watchlist"]]))

def place_bid(request, item_id):
    if request.method == 'POST':
        try:
            curr_highest_bid = Bid.objects.filter(listing_id=item_id).order_by('-amt').first().amt
        except:
            curr_highest_bid = Listing.objects.filter(id=item_id).first().minPrice
        offered = int(request.POST['bid'])
        print(f"amt: {curr_highest_bid}, offer: {offered}")
        if offered > curr_highest_bid:
            new_bid = Bid(bidder=request.user,amt=offered, listing_id_id=item_id)
            new_bid.save()
            added = 1
        else:
            added = 2
             
        response = HttpResponseRedirect(reverse("listing", args=[item_id]))
        response.set_cookie(key='bid_added',value='added')
        return response
        
