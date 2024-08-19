from django.shortcuts import render,redirect
from django.http import HttpResponse
from siteadmin.models import User,Product,CartItem,Category,Purchase,Review
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

def get_user(request):
    try:
        user = User.objects.get(name = request.session.get('username'))
        return user
    except ObjectDoesNotExist:
        return None
    

def pass_user_details(request, context):
    """takes username from request.session and passes to context

    Args:
        request (HttpRequest): an incoming request from the user that contains session info
        context (dict): a dict that is passed to the webpage when rendering
    """
    username = request.session.get('username')
    context['username'] = username
    user = User.objects.filter(name = username).first()
    cart_items_count = CartItem.objects.filter(user = user).count()
    context['cart_items_count'] = cart_items_count


# Create your views here.
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    pass_user_details(request, context)
    return render(request,'user/home.html', context)

def register(request):
    # Initializing outside of form submission for first load
    register_success = False
    request_sent = False
    reasons = []
    context = {
        'register_success': register_success,
        'request_sent': request_sent,
    }
    if request.method == 'POST':
        request_sent = True
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.create(
                name = name,
                email = email,
                password = password
            )
            register_success = True
        except IntegrityError:
            reasons.append('Username already in use')
            register_success = False
    context['register_success'] = register_success
    context['request_sent'] = request_sent
    context['reasons'] = reasons
    pass_user_details(request, context)
    return render(request, 'user/register.html', context)

def login(request):
    # Initializing outside of form submission for first load
    login_success = False
    request_sent = False
    context = {
        'login_success': login_success,
        'request_sent': request_sent
    }
    if request.method == 'POST':
        request_sent = True
        name = request.POST['name']
        password = request.POST['password']

        user = User.objects.filter(name=name, password=password) # Returns an queryset object
        if user.exists():
            login_success = True
            request.session['username'] = user.first().name
            return redirect('user:home')
        else:
            login_success = False
        
    context['login_success'] = login_success
    context['request_sent'] = request_sent
    pass_user_details(request, context)
    return render(request, 'user/login.html', context)


def logout(request):
    if request.session.get('username') != None:
        del request.session['username']
    return redirect('user:home')


def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    pass_user_details(request, context)
    return render(request, 'user/shop.html', context)


def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
        products = Product.objects.filter(name__icontains = search_term)
    else:
        return redirect('user:shop')
    context = {
        'products': products,
        'search_term': search_term
    }
    pass_user_details(request, context)
    return render(request, 'user/shop.html', context)

def category(request, id):
    products = Product.objects.filter(category = id)
    category = Category.objects.get(id = id)
    context = {
        'products': products,
        'category': category.name
    }
    pass_user_details(request, context)
    return render(request, 'user/shop.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    pass_user_details(request, context)
    return render(request,'user/categories.html', context)


def product(request, id):
    product = Product.objects.get(id = id)
    reviews = Review.objects.filter(product = product)
    if reviews.exists():
        avg_rating = round(reviews.aggregate(Avg("rating"))['rating__avg'], ndigits=1)
    else:
        avg_rating = 'N/A'
    
    # Pass as iterable?
    rating_1 = reviews.filter(rating = 1).count()
    rating_2 = reviews.filter(rating = 2).count()
    rating_3 = reviews.filter(rating = 3).count()
    rating_4 = reviews.filter(rating = 4).count()
    rating_5 = reviews.filter(rating = 5).count()
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'rating_1': rating_1,
        'rating_2': rating_2,
        'rating_3': rating_3,
        'rating_4': rating_4,
        'rating_5': rating_5
    }
    # People should be able to view products without logging in!!!!
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    purchases = Purchase.objects.filter(user = user, product=product)
    userreview = Review.objects.filter(user=user, product=product)
    context.update({'userreview': userreview.first()})
    purchased_product = False
    reviewed = False
    if purchases.exists():
        purchased_product = True
    if userreview.exists():
        reviewed = True
    context.update({'purchased_product': purchased_product})
    context.update({'reviewed': reviewed})
    if request.method == 'POST' and request.POST['action'] == 'Add Review':
        details = request.POST['details']
        rating = request.POST['rating']
        
        Review.objects.create(
            user = user,
            rating = rating,
            details = details,
            product = product
        )
        return redirect('user:product', product.id)
    
    elif request.method == 'POST' and request.POST['action'] == 'Edit Review':
        details = request.POST['details']
        rating = request.POST['rating']
        userreview.update(
            details = details,
            rating = rating
        )
        return redirect('user:product', product.id)

    products = Product.objects.filter(category = product.category)
    context['products'] = products
    pass_user_details(request, context)
    return render(request, 'user/product.html', context)


def delete_review(request, id):
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    product = Product.objects.get(id = id)
    userreview = Review.objects.filter(user=user, product=product)
    userreview.delete()
    return redirect('user:product', product.id)

def checkout(request):
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    cart_items = CartItem.objects.filter(user = user)
    subtotal = 0
    for cart_item in cart_items:
        cart_item.total = cart_item.product.price * cart_item.quantity
        subtotal += cart_item.product.price * cart_item.quantity

    shipping = 50
    total = subtotal + shipping
    context = {
        'user': user,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    }
    # User completes payment
    if request.method == 'POST':
        for cart_item in cart_items:
            # Create purchase record
            Purchase.objects.create(
                product = cart_item.product,
                quantity = cart_item.quantity,
                user = cart_item.user
            )
            # Remove from cart
            cart_item.delete()
        return redirect('user:checkout_complete')
    
    pass_user_details(request, context)
    return render(request, 'user/checkout.html', context)

def checkout_complete(request):
    context = {}
    pass_user_details(request, context)
    return render(request, 'user/checkout_complete.html', context)

def contact(request):
    context = {}
    pass_user_details(request, context)
    return render(request, 'user/contact.html', context)


def buy_now(request, id):
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    product = Product.objects.get(id = id)
    # Clear user's cart
    CartItem.objects.filter(user = user).delete()
    # Form input from product page
    qty = 1
    if request.method == 'POST':
        qty = request.POST['qty']

    # Add product to it
    CartItem.objects.create(
        product = product,
        quantity = qty,
        user = user
    )
    return redirect('user:checkout')


def add_to_cart(request, id):
    product = Product.objects.get(id = id)
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    try:
        # This item already exists in user's cart
        cart_item = CartItem.objects.get(product = product, user = user)
        # Product page button selection managed here
        if request.method == 'POST':
            action = request.POST['action']
            if action == 'Buy Now':
                return buy_now(request, id)
            # Product page quantity input handled here
            cart_item.quantity = request.POST['qty']
        else:
            cart_item.quantity += 1
        cart_item.save()

    # This item is not in user's cart
    except ObjectDoesNotExist:
        # User input value from product page
        if request.method == 'POST':
            action = request.POST['action']
            if action == 'Buy Now':
                return buy_now(request, id)
            qty = request.POST['qty']
        else:
            qty = 1
        CartItem.objects.create(
            quantity = qty,
            product = product,
            user = user
        )
    context = {}
    pass_user_details(request, context)
    return redirect('user:cart')


def cart(request):
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    cart_items = CartItem.objects.filter(user = user)
    subtotal = 0
    for cart_item in cart_items:
        cart_item.total = cart_item.product.price * cart_item.quantity
        subtotal += cart_item.product.price * cart_item.quantity
        # Not saving because this is a temporary value

    if request.method == 'POST':
        for cart_item in cart_items:
            user_quantity = request.POST[str(cart_item.id) + '-qty']
            cart_item.quantity = user_quantity
            cart_item.save()
        return redirect('user:cart')

    context = {
        'cart_items':  cart_items,
        'subtotal': subtotal
    }
    pass_user_details(request, context)
    return render(request, 'user/cart.html', context)


def delete_from_cart(request, id):
    cart_item = CartItem.objects.get(id = id)
    cart_item.delete()
    return redirect('user:cart')


def account(request):
    user = get_user(request)
    if user == None:
        return redirect('user:login')
    context = {}
    context['user'] = user

    # Show purchase history
    purchases = Purchase.objects.filter(user = user).order_by('-date')
    context['purchases'] = purchases

    # Updating user details
    if request.method == 'POST':
        # Get values from form
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Update user details
        user.name = name
        user.email = email
        user.password = password
        user.save()

        # Update sessions
        request.session['username'] = name

        return redirect('user:account')

    pass_user_details(request, context)
    return render(request, 'user/account.html', context)


def delete_account(request, id):
    User.objects.filter(id = id).delete()
    return logout(request)
    