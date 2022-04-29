from ntpath import realpath
from tkinter import CASCADE
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.urls import reverse

CATEGORIES = [
        (1, "Misc"),
        (2, "Art"),
        (3, "Electronics"),
        (4, "Auto"),
        (5, "Toys"),
        (6, "Books"),
        (7, "Clothing")
    ]

class User(AbstractUser):
    watchlist = models.CharField(validators=[validate_comma_separated_integer_list], max_length=100, blank=True, null=True, default='')

class Bid(models.Model):
    #Add reference_name to item, to filter all bids for a particular auction to find the highest bid, later
    amount = models.IntegerField(default=0)
    item = models.ForeignKey("Auction", on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Bid for {self.item} for {self.amount}"

class Category(models.Model):
    #category = models.CharField(max_length=11, blank=False, choices=CATEGORIES, null=True)
    class Categories(models.IntegerChoices):
        Misc = 1,
        Art = 2,
        Electronics = 3,
        Auto = 4,
        Toys = 5,
        Books = 6,
        Clothing = 7

    category = models.IntegerField(choices=Categories.choices, null=True)

    def __str__(self):
        return "%s" % (self.get_category_display())


class Auction(models.Model):
    starting_bid = models.IntegerField()

    #Delete current_bid. Current bids are stored in Bid table
    #current_bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, related_name="bid", null=True, blank=True)
    image = models.CharField(max_length=150, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64, blank=True, default="")
    is_open = models.BooleanField(default=True)
    description = models.CharField(max_length=1000, default="")
    #category = models.CharField(max_length=11, choices=CATEGORIES, null=True, default='misc')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False)


    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('auction', args=[str(self.id)])

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True, related_name="auction")
    comment = models.CharField(max_length=800, null=True)

    def __str__(self):
        return f"{self.comment}"