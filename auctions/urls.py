from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auctions/<int:auction_id>", views.auction, name="auction"),
    path("auctions/category/", views.category, kwargs={'category_id': None}, name="category_main"),
    path("auctions/category/<int:category_id>", views.category, name="category"),
    path("auctions/watchlist", views.watchlist, name="watchlist"),
    path("auctions/create", views.create, name="create")
]
