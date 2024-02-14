from . import views
from django.urls import path

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard),
    path('product-list', views.products),
    path('product-create', views.product_create),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),
    # enters
    path('enter-list', views.list_enter, name='list_enter'),
    path('enter-create', views.create_enter, name='create_enter'),
    path('enter-update/<int:id>/', views.update_enter, name='update_enter'),
    path('enter-delete/<int:id>/', views.delete_enter, name='delete_enter'),
]