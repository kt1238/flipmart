from django.urls import path
from . import views
app_name = 'user'

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("shop/", views.shop, name="shop"),
    path("shop/search/", views.search, name="search"),
    path("shop/category/<int:id>", views.category, name="category"),
    path("product/<int:id>", views.product, name="product"),
    path("product/<int:id>/delete_review", views.delete_review, name="delete_review"),
    path("checkout/", views.checkout, name="checkout"),
    path("contact/", views.contact, name="contact"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:id>", views.add_to_cart, name="add_to_cart"),
    path("cart/delete/<int:id>", views.delete_from_cart, name="delete_from_cart"),
    path("logout/", views.logout, name="logout"),
    path("account/", views.account, name="account"),
    path("account/delete/<int:id>", views.delete_account, name="delete_account"),
    path("checkout/complete/", views.checkout_complete, name="checkout_complete"),
    path("categories/", views.categories, name="categories"),
    path("buy_now/<int:id>", views.buy_now, name="buy_now"),
    
]