from django.urls import path
from . import views
from .views import PetUpdateView,ProductUpdateView
from .views import PetDeleteView,ProductDeleteView
urlpatterns = [
    path('', views.index, name='index'),
############admin#######
    path('adm_home', views.adm_home, name='adm_home'),
    path('admin_register', views.admin_register, name='admin_register'),
    
    path('admin_login', views.admin_login, name='admin_login'),
    path('staff_register', views.staff_register, name='staff_register'),
    path('delete_staff/<int:pk>/', views.delete_staff, name='delete_staff'),
    path('boy_register', views.boy_register, name='boy_register'),
    path('delete_boy/<int:pk>/', views.delete_boy, name='delete_boy'),
    path('add_category', views.add_category, name='add_category'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('Logout', views.Logout, name='Logout'),

    path('cus_home', views.cus_home, name='cus_home'),
    path('cus_login', views.cus_login, name='cus_login'),
    path('cus_register', views.cus_register, name='cus_register'),
    path('view_pets',views.view_pets,name='view_pets'),
    path('view_products',views.view_products,name='view_products'),
    path('r_login',views.r_login,name='r_login'),
    path('staff_home',views.staff_home,name='staff_home'),
    path('pet/update/<int:pk>/', PetUpdateView.as_view(), name='pet_update'),
    path('pet/delete/<int:pk>/', PetDeleteView.as_view(), name='pet_delete'),
    path('add_product',views.add_product,name='add_product'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('update-user/<int:user_id>/', views.update_staff_or_boy, name='update_user'),
    path('edit_staff',views.edit_staff,name="edit_staff"),
    path('view_pets_category',views.view_pets_category,name='view_pets_category'),
    path('view_pets_products/<int:category_id>/',views.view_pets_products,name="view_pets_products"),
    path('search',views.search,name="search"),
    path('search1',views.search1,name="search1"),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/increment/<int:item_id>/', views.increment_cart_item, name='increment_cart_item'),
    path('cart/decrement/<int:item_id>/', views.decrement_cart_item, name='decrement_cart_item'),
    path('cart/checkout/', views.checkout_view, name='checkout_view'),   
    path('pet_booking/<int:pet_id>', views.pet_booking, name='pet_booking'),
    path('booking/', views.booking, name='booking'),
    path('manage_booking', views.manage_booking, name="manage_booking"),
    path('cancel_booking/<int:booking_id>', views.cancel_booking, name="cancel_booking"),
    path('deliveryboy_home/', views.deliveryboy_home, name="deliveryboy_home"),
    path('view_order/', views.view_order, name="view_order"),
    path('update_delivery/<int:assign_id>', views.update_delivery, name="update_delivery"),




    

]

