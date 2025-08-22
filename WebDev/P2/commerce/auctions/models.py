from django.contrib.auth.models import AbstractUser
from django.db import models

# 6 models in total

class User(AbstractUser):
    def __str__(self):
        return f"{self.id} {self.username} {self.email}"
    
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} {self.name}"
    
class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_price = models.DecimalField(decimal_places=2, max_digits=16)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_listing")
    img_url = models.CharField(max_length=256, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name="auction_listing")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id} {self.title} {self.listed_by}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_item")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="wishlist_item")

    def __str__(self):
        return f"{self.id} {self.user} {self.item}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bidding")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bidding")
    amount = models.DecimalField(decimal_places=2, max_digits=16)

    def __str__(self):
        return f"{self.id} {self.bidder} {self.amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.id} {self.user} {self.item}"
