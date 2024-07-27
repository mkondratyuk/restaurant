from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dish_images/', null=True, blank=True)
    rating = models.FloatField(default=0.0)  # New field for average rating

    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contact_info = models.TextField()
    delivery_address = models.TextField()
    payment_method = models.CharField(max_length=100, choices=[('online', 'Online'), ('cash', 'Cash on Delivery')])
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)

    def duplicate_order(self):
        new_order = Order.objects.create(
            user=self.user,
            confirmed=False,  # New order is not confirmed
            total_price=self.total_price,  # Keep the same total price
            created_at=timezone.now()  # Set current creation time
        )

        # Copy order items
        for item in self.order_items.all():
            OrderItem.objects.create(
                order=new_order,
                dish=item.dish,
                quantity=item.quantity
            )

        return new_order

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.pk} - Order: {self.order.pk}, Dish: {self.dish.name}, Quantity: {self.quantity}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.user.username

