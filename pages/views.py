from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from .models import Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm, EditUserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
# from .models import userCreation
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from .models import  Cart , Address ,OrderPlaced
from django.http import JsonResponse
import razorpay
from django.conf import settings
import json


# Create your views here.
# @login_required(login_url='login')
def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def service(request):
    return render(request, 'pages/service.html')

def contact(request):
    return render(request, 'pages/contact.html')



class categoryView(View):
    def get(self, request, val):
        gadget = Product.objects.filter(category=val)
        categoryName = val
        title = Product.objects.filter(category=val).values('gadgetName')
        return render(request, 'pages/category.html', {'gadgets': gadget, 'categoryName': categoryName, 'title': title})
    
class gadgetDetail(LoginRequiredMixin, View):
    login_url = 'login'  # Redirect to login page if not authenticated
    redirect_field_name = 'redirect_to'

    def get(self, request, id):
        gadget = Product.objects.get(id=id)
        related_products = Product.objects.filter(category=gadget.category).exclude(id=id)
        return render(request, 'pages/gadgetDetail.html', {
            'gadget': gadget,
            'related_products': related_products,
        })

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('signup')  # Redirect to the signup page in case of error
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')  # Redirect to the login page after successful signup

    return render(request, 'pages/signup.html')
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Username or password is incorrect!")
            return redirect('login')  # Redirect back to login on failure

    return render(request, 'pages/login.html')

def LogoutPage(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')  # Redirect to the login page after logging outdef LogoutPage(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')  # Redirect to the home page after logging out


@login_required
def profile(request):
    # The 'request.user' object contains the information of the currently logged-in user.
    user = request.user

    # You can pass this user object to the template.
    context = {
        'user': user
    }
    return render(request, 'pages/profile.html', context)


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile  # Raise error if profile doesn't exist
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)  # Create a profile if it doesn't exist

    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = EditUserProfileForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        # Check if the profile forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')

            # If password form is valid, save password
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Keep the user logged in

            return redirect('profile')
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
            print("Password form errors:", password_form.errors)

    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = EditUserProfileForm(instance=profile)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'pages/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })


@login_required
def add_to_cart(request, product_id):  # Accept product_id from the URL
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:  # If the item was already in the cart, increment the quantity
        cart_item.quantity += 1
    cart_item.save()
    
    return redirect('view_cart')  # Ensure this matches your URL pattern name


@login_required
def show_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)  
    amount = 0
    for item in cart_items:
        value = item.product.price * item.quantity
        amount += value
    total_amount = amount + 40  # Assuming 40 is the shipping cost

    return render(request, 'pages/addtocart.html', {
        'cart_items': cart_items,
        'amount': amount,
        'total_amount': total_amount,
    })


def increase_quantity(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        
        # Fetch the cart item for this user and increase quantity
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
            cart_item.quantity += 1
            cart_item.save()

            # Calculate updated amounts
            amount = cart_item.quantity * cart_item.product.price
            total_amount = sum(item.quantity * item.product.price for item in Cart.objects.filter(user=request.user))
            
            return JsonResponse({
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': total_amount
            })
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def decrease_quantity(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        
        # Fetch the cart item and decrease the quantity if it's greater than 1
        try:
            cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                # Optionally, you could remove the item from the cart if quantity reaches 0
                cart_item.delete()

            # Calculate updated amounts
            amount = cart_item.quantity * cart_item.product.price if cart_item.quantity > 0 else 0
            total_amount = sum(item.quantity * item.product.price for item in Cart.objects.filter(user=request.user))
            
            return JsonResponse({
                'quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                'amount': amount,
                'totalamount': total_amount
            })
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Product not found in cart'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
def remove_cart_item(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.get(product_id=prod_id, user=request.user)
        cart_item.delete()
        
        # Calculate new total amounts
        cart_items = Cart.objects.filter(user=request.user)
        amount = sum(item.product.price * item.quantity for item in cart_items)
        total_amount = amount + 40  # Example shipping cost
        
        return JsonResponse({'totalamount': total_amount, 'amount': amount})

@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = 40 + sum(item.total_cost for item in cart_items)  # Total in INR paise

    # Fetch user's saved addresses
    addresses = Address.objects.filter(user=request.user)

    # Razorpay API client setup
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    # Create an order when the checkout page is loaded (or after an address is selected)
    if request.method == 'POST':
        # Check if adding a new address
        if 'locality' in request.POST:
            locality = request.POST.get('locality')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            
            # Save address to the database
            Address.objects.create(
                user=request.user,
                locality=locality,
                city=city,
                state=state,
                zipcode=zipcode
            )
            messages.success(request, "New address added successfully!")
            return redirect('checkout')  # Redirect to checkout to see the updated address list

        # Handle address selection
        address_id = request.POST.get('custid')
        if not address_id:
            messages.error(request, "Please select or add an address.")
            return redirect('checkout')

        selected_address = Address.objects.get(id=address_id)

        # Razorpay order creation
        razorpay_order_data = {
            'amount': total_amount * 100,  # Amount in paise (Razorpay expects the amount in paise)
            'currency': 'INR',
            'payment_capture': '1',
        }
        razorpay_order = client.order.create(data=razorpay_order_data)
        razorpay_order_id = razorpay_order['id']

        # Save each cart item as an order
        for item in cart_items:
            OrderPlaced.objects.create(
                user=request.user,
                address=selected_address,
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_cost 
            )

        # Clear cart after order is placed
        cart_items.delete()

        # Redirect to the payment page with Razorpay order ID and amount
        return redirect('payment_page', razorpay_order_id=razorpay_order_id, total_amount=total_amount)

         # Convert total amount to paise (multiply by 100)
    total_amount_in_paise = int(total_amount * 100)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,  # In INR
        'total_amount_in_paise': total_amount_in_paise,  # In paise
        'addresses': addresses,
        'razorpay_api_key': settings.RAZORPAY_API_KEY,
        # 'razorpay_order_id': razorpay_order_id,
    }

    return render(request, 'pages/checkout.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        
        # Save address to database (assuming Address model exists)
        Address.objects.create(
            user=request.user,
            locality=locality,
            city=city,
            state=state,
            zipcode=zipcode
        )
        messages.success(request, "New address added successfully!")
        return redirect('checkout')  # Redirect back to the checkout page
    else:
        return redirect('checkout')



# payment gateway
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@login_required
def create_payment(request):
    amount = 50000  # Amount in paisa (e.g., 50000 paisa = 500 INR)

    # Create a Razorpay order
    razorpay_order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1",
    })

    # Save the order details in the Payment model
    payment = Payment.objects.create(
        user=request.user,
        amount=amount / 100,  # Store as INR
        razorpay_order_id=razorpay_order["id"],
        razorpay_payment_status="created",
    )

    context = {
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_merchant_key": settings.RAZORPAY_API_KEY,
        "amount": amount,
        "currency": "INR",
    }
    return render(request, "checkout.html", context)   

def payment_success(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Initialize Razorpay client
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # Verify the payment signature
        try:
            payment = razorpay_client.payment.fetch(data['razorpay_payment_id'])
            # order = razorpay_client.order.fetch(data['razorpay_order_id'])

            # Validate the payment signature
            generated_signature = razorpay_client.utility.verify_payment_signature(data)

            if generated_signature:
                # Update payment record as successful
                payment_instance = Payment.objects.create(
                    user=request.user,
                    amount=order['amount'] / 100,  # Convert back to INR
                    razorpay_order_id=data['razorpay_order_id'],
                    razorpay_payment_id=data['razorpay_payment_id'],
                    razorpay_payment_status='success',
                    paid=True
                )

                # Optionally create order record for each cart item
                cart_items = Cart.objects.filter(user=request.user)
                for item in cart_items:
                    OrderPlaced.objects.create(
                        user=request.user,
                        product=item.product,
                        quantity=item.quantity,
                        total_price=item.total_cost
                    )

                # Clear cart after successful payment
                cart_items.delete()

                return JsonResponse({'status': 'success'}, status=200)

            else:
                return JsonResponse({'status': 'failure'}, status=400)

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'status': 'failure', 'message': 'Signature verification failed'}, status=400)
    return JsonResponse({'status': 'failure'}, status=400)

def payment_failure(request):
    # You can render a failure page or just send a failure message
    return render(request, 'payment_failure.html', {
        'message': 'Payment failed. Please try again.'
    })
