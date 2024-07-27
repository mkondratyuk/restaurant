from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout

def home(request):
    return render(request, 'restaurant/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Create a profile for the new user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('menu')
    else:
        form = UserRegisterForm()
    return render(request, 'restaurant/register.html', {'form': form})

@login_required 
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def menu(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    dishes = Dish.objects.all()

    if query:
        dishes = dishes.filter(name__icontains=query)
    if category_id:
        dishes = dishes.filter(category_id=category_id)
    if min_price:
        dishes = dishes.filter(price__gte=min_price)
    if max_price:
        dishes = dishes.filter(price__lte=max_price)

    popular_dishes = Dish.objects.annotate(order_count=models.Count('orderitem')).order_by('-order_count')[:5]
    categories = Category.objects.all()
    reviews = Review.objects.all()
    
    return render(request, 'restaurant/menu.html', {
        'dishes': dishes, 
        'categories': categories, 
        'popular_dishes': popular_dishes,
        'min_price': min_price,
        'max_price': max_price,
        'reviews': reviews,
    })

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, confirmed=False).first()
    if order:
        order_items = order.order_items.all()
        total_price = sum(item.dish.price * item.quantity for item in order_items)
    else:
        order_items = []
        total_price = 0

    return render(request, 'restaurant/cart.html', {'order_items': order_items, 'total_price': total_price})

@login_required
def add_to_cart(request, dish_id):
    user = request.user
    dish = get_object_or_404(Dish, id=dish_id)
    
    # Get or create an unconfirmed order for the user
    order = Order.objects.filter(user=user, confirmed=False).first()
    if not order:
        order = Order.objects.create(user=user)

    # Check if the dish is already in the order
    order_item, created = OrderItem.objects.get_or_create(order=order, dish=dish)
    if not created:
        order_item.quantity += 1
        order_item.save()

    messages.success(request, f'{dish.name} додано до замовлення.')
    return redirect('menu')


@login_required
def place_order(request):
    order = Order.objects.filter(user=request.user, confirmed=False).first()
    
    if not order:
        messages.error(request, "There is no active order to place.")
        return redirect('menu')
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            # Calculate total price
            total_price = sum(item.dish.price * item.quantity for item in order.order_items.all())
            order.total_price = total_price
            order.confirmed = True
            order.save()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderForm(instance=order)
    
    total_price = sum(item.dish.price * item.quantity for item in order.order_items.all())
    return render(request, 'restaurant/place_order.html', {'form': form, 'order': order, 'total_price': total_price})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = sum(item.dish.price * item.quantity for item in order.order_items.all())
    return render(request, 'restaurant/order_confirmation.html', {'order': order, 'total_price': total_price})

@login_required
def reviews(request):
    reviews = Review.objects.all().select_related('user')
    dishes = Dish.objects.all()
    return render(request, 'restaurant/reviews.html', {'reviews': reviews, 'dishes': dishes})

from django.db.models import Avg

def write_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.dish = dish
            review.save()
            
            # Calculate and update average rating for the dish
            average_rating = dish.reviews.aggregate(Avg('rating'))['rating__avg']
            if average_rating is not None:
                dish.rating = round(average_rating)
            else:
                dish.rating = 0  # or any default value you prefer
            dish.save()

            return redirect('menu')
    else:
        form = ReviewForm()
    
    return render(request, 'restaurant/write_review.html', {'form': form, 'dish': dish})

@login_required
@staff_member_required
def add_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name)
                dish.category = category
            else:
                dish.category = form.cleaned_data.get('category')
            dish.save()
            return redirect('menu')
    else:
        form = DishForm()
    return render(request, 'restaurant/add_dish.html', {'form': form})


@login_required
@staff_member_required
def edit_dish(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.category_id = form.cleaned_data['category'].id  # Призначення category_id перед збереженням
            dish.save()
            return redirect('menu')
    else:
        form = DishForm(instance=dish)
    return render(request, 'restaurant/edit_dish.html', {'form': form, 'dish': dish})

@login_required
@staff_member_required
def delete_dish(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        dish.delete()
        return redirect('menu')
    return render(request, 'restaurant/delete_dish.html', {'dish': dish})

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'restaurant/profile.html', {'form': form, 'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'restaurant/edit_profile.html', {'form': form})

@login_required
def add_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
            return redirect('reviews')  # Повертаємо користувача на сторінку з відгуками після додавання коментаря
    else:
        form = CommentForm()
    return render(request, 'restaurant/add_comment.html', {'form': form, 'review': review})

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, pk=dish_id)
    reviews = dish.reviews.filter(approved=True)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.dish = dish
            review.user = request.user
            review.save()
            return redirect('dish_detail', dish_id=dish.id)
    else:
        review_form = ReviewForm()

    return render(request, 'dish_detail.html', {'dish': dish, 'reviews': reviews, 'review_form': review_form})

@login_required
def repeat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    new_order = order.duplicate_order()
    return redirect('order_confirmation', order_id=new_order.id)

from django.db.models import Sum, Count

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, confirmed=True)
    
    most_ordered_dishes = OrderItem.objects.filter(order__user=request.user, order__confirmed=True)\
        .values('dish__name')\
        .annotate(count=Count('dish__name'))\
        .order_by('-count')[:5]

    total_spent = orders.aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'restaurant/order_history.html', {
        'orders': orders,
        'most_ordered_dishes': most_ordered_dishes,
        'total_spent': total_spent,
    })
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = sum(item.dish.price * item.quantity for item in order.order_items.all())
    return render(request, 'restaurant/order_detail.html', {'order': order, 'total_price': total_price})

from django.http import JsonResponse
from django.views import View
from .models import Dish

class DishesAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        dishes = Dish.objects.filter(name__icontains=query).values('id', 'name')
        results = list(dishes)
        return JsonResponse(results, safe=False)