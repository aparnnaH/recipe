from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# from .models import User, Listing, Bid, Comment, Category, WatchList
from .models import User, Listing, Comment, Category, WatchList, Favourite
from .forms import CreateListingForm

#done
def index(request):
    return render(request, "recipes/index.html", {
        "listings": Listing.objects.all(),
        # "category": Category.objects.all()
    })

    # return render(request, "recipes/index.html", 
    # {"listings": Listing.objects.filter(sold=False)
    # })

def profile(request):
    return render(request, "recipes/profile.html", {
        "listings": Listing.objects.filter(user = request.user)
        # "category": Category.objects.all()
    })

#done
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
            return render(request, "recipes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "recipes/login.html")

#done
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#done
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "recipes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "recipes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "recipes/register.html")
#change
@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            prep_time = form.cleaned_data["prep_time"]
            cook_time = form.cleaned_data["cook_time"]
            ingredients = form.cleaned_data["ingredients"]
            steps = form.cleaned_data["steps"]
            # ingredients = request.POST['ingredients'].split(",")
            # steps = request.POST['steps'].split(".")
            image_url = form.cleaned_data["image_url"]
            user = request.user
            category_id = Category.objects.get(id=request.POST["categories"])
            Listing.objects.create(user = user, title = title, description = description, prep_time = prep_time, 
                cook_time = cook_time, ingredients = ingredients, steps = steps, image_url = image_url, category = category_id)
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "recipes/create_listing.html", {
            "listing_form": CreateListingForm(),
            "categories": Category.objects.all()
        })

#change
@login_required
def listing_info(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    # is_owner = True if listing.user == user else False
    category = Category.objects.get(category=listing.category)
    comments = Comment.objects.filter(listing=listing.id)
    watching = WatchList.objects.filter(user = user, listing = listing)
    if watching:
        watching = WatchList.objects.get(user = user, listing = listing)
    return listing, user, category, comments, watching
    # return listing, user, is_owner, category, comments, watching

#change
@login_required
def listing(request, listing_id):
    info = listing_info(request, listing_id)
    # listing, user, is_owner, category = info[0], info[1], info[2], info[3]
    listing, user, category = info[0], info[1], info[2]
    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            Comment.objects.create(user = user, listing = listing, comment = comment)

    return render(request, "recipes/listing.html", {
        "listing": listing,
        "category": category,
        "comments":Comment.objects.filter(listing=listing.id), 
        "watching": WatchList.objects.filter(user = user, listing = listing).values('watching'), 
        # "is_owner": is_owner
    })

#done
@login_required
def remove_watchlist(request, listing_id):
    info = listing_info(request, listing_id)
    # listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    listing, user, category, comments, watch = info[0], info[1], info[2], info[3], info[4]
    watch.watching = False
    watch.save()

    return render(request, "recipes/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "watching": WatchList.objects.get(user = user, listing = listing).watching, 
        # "is_owner": is_owner
    })

#done
@login_required
def add_watchlist(request, listing_id):
    info = listing_info(request, listing_id)
    # listing, user, is_owner, category, comments = info[0], info[1], info[2], info[3], info[4]
    listing, user, category, comments = info[0], info[1], info[2], info[3]
    watch = WatchList.objects.filter(user = user, listing = listing)
    if watch:
        watch = WatchList.objects.get(user = user, listing = listing)
        watch.watching = True
        watch.save()
    else:
        WatchList.objects.create(user = user, listing = listing, watching = True)

    return render(request, "recipes/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "watching": WatchList.objects.get(user = user, listing = listing).watching, 
        # "is_owner": is_owner
    })

#done
@login_required
def watchlist(request, user_id):
    listing_ids = WatchList.objects.filter(user = request.user, watching=True).values('listing')
    listing = Listing.objects.filter(id__in = listing_ids)
    return render(request, "recipes/watchlist.html", {
        "listings": listing
    })

#done
def category(request):
    listings = None
    category = None
    if request.method == "POST":
        category = request.POST["categories"]
        listings = Listing.objects.filter(category = category)
    return render(request, "recipes/categories.html", {
        "categories": Category.objects.all(),
        "category": Category.objects.get(id = category).category if category is not None else "",
        "listings": listings
    })


#### add ####
def categoryList(request, category):
    listings = None
    # category = None
    if request.method == "POST":
        category = request.POST["categories"]
        listings = Listing.objects.filter(category = category)
    return render(request, "recipes/category.html", {
        "categories": Category.objects.all(),
        "category": category,
        "listings": listings
    })

#### add ####
def favourite(request, user_id):
    listing_ids = WatchList.objects.filter(user = request.user, watching=True).values('listing')
    listing = Listing.objects.filter(id__in = listing_ids)
    return render(request, "recipes/favourite.html", {
        "listings": listing
    })


@login_required
def add_favourite(request, listing_id):
    info = listing_info(request, listing_id)
    # listing, user, is_owner, category, comments = info[0], info[1], info[2], info[3], info[4]
    listing, user, category, comments = info[0], info[1], info[2], info[3]

    watch = Favourite.objects.filter(user = user, listing = listing)
    if watch:
        watch = Favourite.objects.get(user = user, listing = listing)
        watch.watching = True
        watch.save()
    else:
        Favourite.objects.create(user = user, listing = listing, watching = True)

    return render(request, "recipes/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "watching": Favourite.objects.get(user = user, listing = listing).watching, 
        # "is_owner": is_owner
    })

@login_required
def remove_favourite(request, listing_id):
    info = listing_info(request, listing_id)
    # listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    listing, user, category, comments, watch = info[0], info[1], info[2], info[3], info[4]
    watch.watching = False
    watch.save()

    return render(request, "recipes/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "watching": Favourite.objects.get(user = user, listing = listing).watching, 
        # "is_owner": is_owner
    })

#change
@login_required
def listing_info(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    # is_owner = True if listing.user == user else False
    category = Category.objects.get(category=listing.category)
    comments = Comment.objects.filter(listing=listing.id)
    watching = WatchList.objects.filter(user = user, listing = listing)
    if watching:
        watching = WatchList.objects.get(user = user, listing = listing)
    return listing, user, category, comments, watching
    # return listing, user, is_owner, category, comments, watching

#change
@login_required
def listing(request, listing_id):
    info = listing_info(request, listing_id)
    # listing, user, is_owner, category = info[0], info[1], info[2], info[3]
    listing, user, category = info[0], info[1], info[2]

    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            Comment.objects.create(user = user, listing = listing, comment = comment)

    return render(request, "recipes/listing.html", {
        "listing": listing,
        "category": category,
        "comments":Comment.objects.filter(listing=listing.id), 
        "watching": WatchList.objects.filter(user = user, listing = listing).values('watching')
        # "is_owner": is_owner
    })