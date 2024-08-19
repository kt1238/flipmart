from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.products, name="products"),
    path("products/<int:id>", views.product, name="product"),
    path("products/delete/<int:id>", views.delete_product, name="delete_product"),
    path("users/", views.users, name="users"),
    path("users/delete/<int:id>", views.delete_user, name="delete_user"),
    path("categories/", views.categories, name="categories"),
    path("categories/edit/<int:id>", views.edit_category, name="edit_category"),
    path("categories/delete/<int:id>", views.delete_category, name="delete_category"),
    path("reviews/", views.reviews, name="reviews"),
    path("reviews/delete/<int:id>", views.delete_review, name="delete_review"),
]