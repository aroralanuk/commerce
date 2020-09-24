from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Catergory(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    minPrice = models.IntegerField()
    image = models.ImageField(upload_to="images/",blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myItems")
    category = models.ForeignKey(Catergory, on_delete=models.CASCADE, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()

    def __str__(self):
        return f"{self.title}"

class   Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myBid")
    amt = models.IntegerField()
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="itemBids", default=0)
    
    def __str__(self):
        return f"{self.listing_id} at {self.amt} by {self.bidder}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myWatchList")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="inPeoplesWatchList")
    
    def __str__(self):
        return f"{self.user}'s watchList'"

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myComments")
    created_at = models.DateTimeField(auto_now_add=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="ListingComments")
    
    def __str__(self):
        return f"{self.user}'s comment: \"{self.comment}\""
    
