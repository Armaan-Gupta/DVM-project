from django.urls import path
from .views import ProductDeleteView
from . import views

urlpatterns = [
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-store/', views.my_store, name='my_store'),
    path('my-store/order-detail/<int:pk>/', views.my_store_order_detail, name='my_store_order_detail'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-store/delete-product/<int:pk>/', ProductDeleteView.as_view(template_name='userprofile/product_confirm_delete.html'), name='delete_product'),
]