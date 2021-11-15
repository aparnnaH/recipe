from django.contrib.auth.models import AbstractUser
from django.db import models
from django_mysql.models import ListTextField
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta

class User(AbstractUser):
    pass

class Category(models.Model): # represent category of listings
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

# class Listing(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) # user who posted the listing
#     title = models.CharField(max_length=64)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=6, decimal_places=2) # not required
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category")
#     categories = models.ManyToManyField(Category, blank=True, related_name="select_category") # all categories to select from
#     image_url = models.URLField(default='google.com')
#     sold = models.BooleanField(default=False) # not required

#     def __str__(self):
#         return f"{self.title} posted by {self.user}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user who posted the listing
    title = models.CharField(max_length=64)
    description = models.TextField()
    # duration time 
    prep_time = models.DurationField(default=timedelta(minutes=0))
    cook_time = models.DurationField(default=timedelta(minutes=0))
    # Steps list 
    steps = models.TextField(null = False, blank = False)
    # Ingredients list 
    ingredients = models.TextField(default="Ingredients not entered")

    # steps = ArrayField(
    #     ArrayField(
    #         models.CharField(max_length=100, blank=True),
    #         size=30,
    #     ),
    #     size=30,
    # )
    # Ingredients list 
    # ingredients = ArrayField(
    #     ArrayField(
    #         models.CharField(max_length=100, blank=True),
    #         size=30,
    #     ),
    #     size=30,
    # )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category")
    categories = models.ManyToManyField(Category, blank=True, related_name="select_category") # all categories to select from
    image_url = models.URLField(default='google.com')

    def __str__(self):
        return f"{self.title} posted by {self.user}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment} - {self.user}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watching = models.BooleanField(default=False)

#### add ####
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    watching = models.BooleanField(default=False)

