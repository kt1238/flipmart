from django.shortcuts import render, redirect, HttpResponse
from siteadmin.models import *
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def home(request):
    return render(request,'siteadmin/home.html')

def products(request):
    # Takes form input and creates new object
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        category = Category.objects.get(id = request.POST['category'])
        image = request.FILES['image']

        Product.objects.create(
            name = name,
            price = price,
            category = category,
            image = image
        )
        return redirect('products')

    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'siteadmin/products.html', context)


def product(request,id):
    # Displaying info about product
    product = Product.objects.get(id = id)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'product': product
    }

    # Updating info about product
    if request.method == 'POST':

        product = Product.objects.get(id = id)

        name =  request.POST['name']
        price = request.POST['price']
        category = Category.objects.get(id = request.POST['category'])
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            image = product.image

        
        product.name = name
        product.price = price
        product.category = category
        product.image = image
        product.save()
        return redirect('product',id)

    return render(request, 'siteadmin/product.html', context)


def delete_product(request, id):
    Product.objects.filter(id = id).delete()
    return redirect('products')

def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'siteadmin/users.html', context)


def delete_user(request, id):
    User.objects.filter(id = id).delete()
    return redirect('users')


def categories(request):

    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']
        Category.objects.create(
            name = name,
            image = image
        )
        return redirect('categories')
    
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'siteadmin/categories.html', context)

def edit_category(request, id):
    category = Category.objects.get(id = id)
    if request.method == 'POST':
        name = request.POST['name']
        try:
            image = request.FILES['image']
        except:
            image = category.image

        category.image = image
        category.name = name
        category.save()
        return redirect('categories')

    context = {
        'category': category
    }
    return render(request, 'siteadmin/edit_category.html', context)

def delete_category(request, id):
    Category.objects.filter(id = id).delete()
    return redirect('categories')


def reviews(request):
    reviews = Review.objects.all()
    context = {
        'reviews': reviews
    }
    return render(request, 'siteadmin/reviews.html', context)


def delete_review(request, id):
    Review.objects.filter(id=id).delete()
    return redirect('reviews')