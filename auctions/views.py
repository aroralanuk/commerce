from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Comment, Catergory, WatchList, Bid, WinningBid



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

def displayListing(request, item_id, bid_message=0):
    user = request.user.id
    try:
        item = Listing.objects.get(id=item_id)
    except:
        return HttpResponseRedirect(reverse("index"))
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
        "watchlisted": watchlisted,
        "bid_message": bid_message
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
            bid_added = 1
        else:
            bid_added = 2
             
        return displayListing(request, item_id, bid_added)

def close_bid(request, item_id):
    user = request.user
    
    closing_now = Listing.objects.get(id=item_id)
    closing_now.active = False
    closed = WinningBid()
    closed.sold = closing_now
    closed.seller = user
    try:
        closed.buyer = Bid.objects.filter(listing_id=item_id).order_by('-amt').first().bidder
        closed.amt = Bid.objects.filter(listing_id=item_id).order_by('-amt').first().amt
    except:
        closed.buyer = user
        closed.amt = Listing.objects.filter(owner=user).first().minPrice
    closed.save()
    closing_now.save()
    return HttpResponseRedirect(reverse("listing",args=[item_id]))  

def add_comment(request, item_id):
    if request.method == 'POST':
        new_c = Comment()
        new_c.comment = request.POST['comment']
        new_c.user = request.user
        try:
            new_c.listing_id = Listing.objects.get(id=item_id)
        except:
            return HttpResponseRedirect(reverse("index"))
        new_c.save()
        return HttpResponseRedirect(reverse("listing",args=[item_id])) 

def categories(request):
    cats = set(Listing.objects.only('category'))
    return render(request,"auctions/categories.html",{
        "categories": cats
    })

def filterByCat(request, cat):
    category = Catergory.objects.get(title=cat)
    return render(request, "auctions/category.html",{
        "category": cat,
        "listings": Listing.objects.filter(category = category)
    })

def createListing(request):
    categories = Catergory.objects.all()

    return render(request,"auctions/createListing.html",{
        "categories": set(Catergory.objects.only('title'))
    })

def submitListing(request):
    user = request.user
    if user.is_authenticated and request.method == 'POST':
        newListing = Listing()
        newListing.owner = user
        newListing.title = request.POST['title']
        newListing.category_id = request.POST['category']
        newListing.description = request.POST['description']
        newListing.minPrice = request.POST['minPrice']
        if request.POST.get('image'):
            newListing.image = request.POST.get('image')
        newListing.active = True
        newListing.save()
        return HttpResponseRedirect(reverse("listing",args=[newListing.id]))
    else:
        return HttpResponseRedirect(reverse('index'))
