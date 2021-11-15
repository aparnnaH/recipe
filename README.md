# Recipe Website

## Home
The receipes are displayed in an image card view with description on the side that mentions the title, description, category. 

## Categories
The recipe are sorted by the following categories (Breakfast, Lunch, Dinner, Dessert). Using the dropdown menu the user is able to sort based on the desired category. The recipe is shown in by card view with the image, name, description, posted by whom. If the title of the recipe is clicked it will direct the user to the recipe page.   

## Submit recipe
Using Django, the form allows the user to submit a recipe, which will include the following information ...
 - Tittle 
 - Description
 - Preparation time (format: 00:00:00)
 - Cook time (format: 00:00:00)
 - Ingredients (separated by new line for a new ingredient) 
 - Steps (separated by new line for a new step) 
 - Image URL
 - Category (drop down menu)

## Favourite
User is able to favourite any recipe for later use. The page shows the recipes in card view with the image and title. The title is a hyperlink that directs the user to the recipe page. 

## Profile
The profile page shows what recipes the currently logged in user had poster. The card view is shown as 3 in each row. Each card has the image and title that hyperlinks to the recipe page. 

## Account 
The Django 
## What’s contained in each file you created
**cookbook/recipes/templates/recipes/** 
 - categories.html
 - category.html
 - create_listing.html
 - favourite.html
 - index.html
 - layout.html
 - listing.html
 - login.html
 - profile.html
 - register.html
 
**cookbook/recipes/static/recipes/** 
 - category.css
 - header.css
 - styles.css

**cookbook/recipes/**
 - forms.py
 - models.py
 - urls.py
 - views.py


## How to run your application 

## Additional information

## Distinctiveness and Complexity


**Export to disk** 

> **Note:** The **Publish now** button is disabled if your file has not been published yet.


