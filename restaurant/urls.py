from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from .views import  DishesAutocompleteView




urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='restaurant/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('menu/', views.menu, name='menu'),
    path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
    path('write_review/<int:dish_id>/', views.write_review, name='write_review'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('edit_dish/<int:dish_id>/', views.edit_dish, name='edit_dish'),
    path('delete_dish/<int:dish_id>/', views.delete_dish, name='delete_dish'),
    path('reviews/', views.reviews, name='reviews'),
    path('write_review/<int:dish_id>/', views.write_review, name='write_review'),
    path('add_comment/<int:review_id>/', views.add_comment, name='add_comment'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('dishes/autocomplete/', DishesAutocompleteView.as_view(), name='dishes_autocomplete'),

]
