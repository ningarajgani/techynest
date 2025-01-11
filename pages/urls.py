from django.urls import path
from pages import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('login/', views.LoginPage, name='login'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>/', views.categoryView.as_view(), name='category'),
    path('gadgetDetail/<int:id>/', views.gadgetDetail.as_view(), name='gadgetDetail'),
    path('logout/', views.LogoutPage, name='logout'),
    path('signup/', views.SignupPage, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    


    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # URL to add to cart
    path('view-cart/', views.show_cart, name='view_cart'),  # URL to view the cart
    path('checkout/', views.checkout_view, name='checkout'),  # URL for the checkout page
    path('pluscart/', views.increase_quantity, name='pluscart'),
    path('minuscart/', views.decrease_quantity, name='minuscart'),
    path('removecart/', views.remove_cart_item, name='remove_cart_item'),
    path('add_address/', views.add_address, name='add_address'),  # URL for adding new address
    path('payment/', views.create_payment, name="create_payment"),
    path('payment/success/', views.payment_success, name='payment_success'),  # This is the payment_success route
    path('payment/failure/', views.payment_failure, name='payment_failure'),  # Optional for failure handling
   

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
