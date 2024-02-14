from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.product_detail, name='product_detail'),
    path('carts', views.carts, name='carts'),
    path('cart/<int:id>/', views.cart_detail, name='cart_detail'),
    path('cart/detail/delete/', views.cart_detail_delete, name='cart_detail_delete'),
    path('wish-list/create', views.create_wish_list, name='create_wish_list'),
    path('wish-list/list', views.list_wish_list, name='list_wish_list'),
    path('wish-list/delete', views.delete_wish_list, name='delete_wish_list'),
    path('profile-edit', views.edit_profile, name='edit_profile'),
    path('set-password', views.set_password, name='set_password'),

]