from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("lisitng/create", views.create_listing, name="create_listing"),
    path("listing/add", views.add_listing, name="add_listing"),
    path("listing/<int:listing_id>", views.auction_listing, name="listing"), 
    path("listing/close/<int:listing_id>", views.close_listing, name="close_listing"), 
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.add_watchlist, name="add_watchlist"), 
    path("watchlist/remove/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"), 
    path("bid/place/<int:listing_id>", views.place_bid, name="place_bid"), 
    path("categories", views.categories, name="categories"), 
    path("category/<int:cat_id>", views.category_listings, name="category_listings"), 
    path("comment/add/<int:listing_id>", views.add_comment, name="add_comment")
]
