from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from .forms import PetForm , ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.cache import never_cache,cache_control
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from .forms import UpdateUserForm
from django.db.models import Q 
# Create your views here.

@never_cache
def index(request):
    category=Category.objects.all()
    if category:
       return render(request,'index.html',{'category':category})
    else:
       return render(request,'index.html')

############admin panel ##############
#####################################

##############Admin register ##################

def admin_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("password")
        passw2= request.POST.get("password1")
        
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'administrator/register.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    password=passw1,
                  
                    is_admin=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful.')
                return redirect('admin_login')
        else:
            messages.error(request, 'password not matching.')
            return redirect('admin_register')
        
    else:
        return render(request, "administrator/register.html")
    

#############login #########################
def admin_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_admin:
            login(request, user)
            return redirect('adm_home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'administrator/login.html', {'username': uname})
    return render(request, "administrator/login.html")

########admin home #######
@login_required
@never_cache
def adm_home(request):
    return render(request,'administrator/base.html')

##############staff register ##################

def staff_register(request):
    staff=User.objects.filter(is_staff=True)
    
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("Password")
        passw2= request.POST.get("Password1")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        Role = request.POST.get("Role")
        
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'administrator/add_staff.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    password=passw1,
                    name=name,
                    mobile=phone,
                    email=email,
                    role=Role,
                    is_staff=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful.')
                return redirect('staff_register')
        else:
            messages.error(request, 'password not matching.')
            return redirect('staff_register')
    
    else:
        context={
        'staff':staff
    }
        return render(request, "administrator/add_staff.html",context)

##### delete shop
def delete_staff(request,pk):
    staff=User.objects.get(pk=pk)
    staff.delete()
    messages.error(request, 'Delete Successfully Completed.')
    return redirect('staff_register')  

##############staff register ##################

def boy_register(request):
    boy=User.objects.filter(is_boy=True)
    
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("Password")
        passw2= request.POST.get("Password1")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        Role = request.POST.get("Role")
        
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'administrator/add_boy.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    password=passw1,
                    name=name,
                    mobile=phone,
                    email=email,
                    role=Role,
                    is_boy=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful.')
                return redirect('boy_register')
        else:
            messages.error(request, 'password not matching.')
            return render(request,"administrator/add_boy.html", {
                'username': uname,
                'name':name,
                'email': email,
                'phone':phone,
                'role':Role,
                
                
            })
    
    else:
        context={
        'boy':boy
    }
        return render(request, "administrator/add_boy.html",context)
    

##### delete shop
def delete_boy(request,pk):
    boys=User.objects.get(pk=pk)
    boys.delete()
    messages.error(request, 'Delete Successfully Completed.')
    return redirect('boy_register')
  
def add_category(request): 
    cate=Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            messages.error(request, f"The category '{name}' already exists.")
        else:
          category=Category.objects.create(
          
            name=name,
        
          )
          category.save()
          messages.success(request,'Successfully added')
          return redirect('add_category')
    context={
        'cate':cate
    }
  

    return render(request, "administrator/add_category.html",context)


##### delete shop
def delete_category(request,pk):
    boys=Category.objects.get(pk=pk)
    boys.delete()
    messages.error(request, 'Delete Successfully Completed.')
    return redirect('add_category')

def Logout(request):  
    logout(request)
    request.session.flush()
    return redirect('index')
##############Customer  register ##################
###################################################
def cus_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        name = request.POST.get("name")
        passw1 = request.POST.get("password")
        passw2= request.POST.get("confirm_password")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        Role = request.POST.get("Role")
        address = request.POST.get("address")
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'user/register.html')
            else:
                user = User.objects.create_user(
                    username=uname,
                    name=name,
                    password=passw1,
                    mobile=phone,
                    email=email,
                    Address=address,
                    role=Role,
                    is_customer=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful.')
                return redirect('cus_login')
        else:
            messages.error(request, 'password not matching.')
            return render(request, 'user/register.html', {
                'username': uname,
                'email': email,
                'phone':phone,
                'address':address,
                'password':passw1,
                'confirmPassword':passw2,
            })
            # return redirect('cus_register')
    
    else:
        return render(request, "user/register.html")
    
def cus_login(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user.is_customer:
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('cus_home')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'user/login.html', {'username': uname})
    return render(request, "user/login.html")

def cus_home(request):
    view_pets=Pet.objects.all()
    view_products=Products.objects.all()
    category =Category.objects.all()
    context={
        'view_pets':view_pets,
        'view_products':view_products,
        'category':category,
    }

    return render(request,'user/index.html',context)


@never_cache
def r_login(request): #login for all users
    print(request.path)
    roles = User.objects.exclude(role__isnull=True).values('role')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_authenticated:
            # Check role
            if user.is_admin:
                login(request, user)
                return redirect('adm_home')
            elif user.is_staff and role == user.role:
                print(user.role)
                login(request, user)
                return redirect('staff_home')
            elif user.is_boy and role == user.role:
                login(request, user)
                return redirect('delivery_boy_home')
            elif user.is_customer:
                login(request, user)
                return redirect('cus_home')
            else:
                messages.error(request, 'Invalid role for this user.')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'username': username})

    return render(request,'login.html',{'roles': roles})

@login_required
@never_cache
def staff_home(request): #staff here adds pets stocks and details
    print(request.path)
    categories = list(Category.objects.all().values_list('name', flat=True) ) # Fetch all categories
    pets = Pet.objects.all()  # Fetch all pets from the database
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)  # Form for adding a new pet
        if form.is_valid():
            form.save()  # Save the pet to the database
            return redirect('staff_home')  # Redirect to the same page after saving
    else:
        form = PetForm()

    context = {
        'form': form,
        'pets': pets,
        'categories': categories
    }
    

    return render(request,'staff/home.html',context)



class PetUpdateView(UpdateView):
    model = Pet
    fields = ['name','age', 'category', 'pic', 'price', 'description', 'breed', 'color', 'stock_level','vaccination']
    template_name = 'staff/pet_form.html'
    success_url = reverse_lazy('staff_home')

class PetDeleteView(DeleteView):
    model = Pet
    template_name = 'staff/pet_confirm_delete.html'
    success_url = reverse_lazy('staff_home')     

def add_product(request):
    products= Products.objects.all()

    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES) 
       if form.is_valid():
            form.save()  
            return redirect('add_product')
    else:
        form = PetForm()

    context = {
        'form': form,
        'products': products,
        
    }

    return render(request,'staff/add_product.html',context)


class ProductUpdateView(UpdateView):
    model = Products
    fields = ['name', 'category', 'pic', 'price', 'description', 'stock_level']
    template_name = 'staff/product_update.html'
    success_url = reverse_lazy('add_product')

class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'staff/product_confirm_delete.html'
    success_url = reverse_lazy('add_product')

def view_pets(request):
    view_pets=Pet.objects.all()

    return render(request,'user/view_pets.html',{'view_pets': view_pets}) 

def view_products(request):
    view_products=Products.objects.all()

    return render(request,'user/view_products.html',{'view_products':view_products})   





def update_staff_or_boy(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # Redirect or return a success message
            if user.is_staff:
                return redirect('staff_register')  
            else:
                return redirect('boy_register')
    else:
        form = UpdateUserForm(instance=user)
    
    return render(request, 'administrator/update.html', {'form': form})


def edit_staff(request):
    boy = User.objects.filter(is_boy=True)
    stock_manager = User.objects.filter(is_staff=True)

    context = {
        "boy": boy,
        "staff": stock_manager
    }
    return render(request, "administrator/edit.html", context)


def view_pets_category(request):
    category=Category.objects.all()

    return render(request,"user/view_pets_category.html",{"category":category})



def view_pets_products(request,category_id):
    category = Category.objects.get(id=category_id)
    pets = Pet.objects.filter(category=category)
    products = Products.objects.filter(category=category)
    
    context = {
        'category': category,
        'pets': pets,
        'products': products
    }
    
    return render(request, 'user/view_pets_products.html', context)

def search(request):
    query = request.GET.get('query', '')  # Get the search term from the request
    print(query)
    categorys =Category.objects.all()
    c_query=query
    for i in categorys:
        # print(i)
        i=i.name
        no_spaces = ''.join(i.split())
        if no_spaces.lower() == ''.join(query.split()).lower():
           c_query=i
        # print("hello",c_query)
        # print(no_spaces.lower())
    category=Category.objects.filter(name__iexact=c_query).first()
    print(category)
    product_results = []
    pet_results = []
    error_message = "" 
    if query:
        # Search in the Product model (e.g., name or description)
        pet_results = Pet.objects.filter(
            Q(name__iexact=query) | Q(category=category.id if category else None)
        )
        
        if not pet_results.exists():  # Search in the Category model (e.g., title)
            product_results = Products.objects.filter(
                              Q(name__iexact=query) | Q(category=category.id if category else None)
                            )
        if not product_results and not pet_results:
               error_message = "No pets or products found for your search."

    context = {
        'product_results': product_results,
        'pet_results': pet_results,
        'query': query,
        'error_message': error_message,
    }
    print(pet_results)
    return render(request, 'user/search.html', context)



def search1(request):
    query = request.GET.get('query', '')  # Get the search term from the request
    print(query)
    categorys =Category.objects.all()
    c_query=query
    for i in categorys:
        # print(i)
        i=i.name
        no_spaces = ''.join(i.split())
        if no_spaces.lower() == ''.join(query.split()).lower():
           c_query=i
        # print("hello",c_query)
        # print(no_spaces.lower())
    category=Category.objects.filter(name__iexact=c_query).first()
    print(category)
    product_results = []
    pet_results = []
    error_message = "" 
    if query:
        # Search in the Product model (e.g., name or description)
        pet_results = Pet.objects.filter(
            Q(name__iexact=query) | Q(category=category.id if category else None)
        )
        
        if not pet_results.exists():  # Search in the Category model (e.g., title)
            product_results = Products.objects.filter(
                              Q(name__iexact=query) | Q(category=category.id if category else None)
                            )
        if not product_results and not pet_results:
               error_message = "No pets or products found for your search."

    context = {
        'product_results': product_results,
        'pet_results': pet_results,
        'query': query,
        'error_message': error_message,
    }
    print(pet_results)
    return render(request, 'staff/search1.html', context)

# def search(request):
#     query_string = request.GET.get('query', '').strip()  # Get the search term from the request
#     if not query_string:
#         return render(request, 'user/search.html', {'error_message': "Please enter a search term."})

#     # Normalize the search term
#     normalized_search_term = ''.join(query_string.split())  # Remove all spaces
#     print(normalized_search_term)
#     # Prepare the search query using Q objects
#     search_query = Q()

#     # Split the normalized search term into individual characters or keywords
#     search_chars = list(normalized_search_term)

#     # Build the search query to match any of the characters
#     for char in search_chars:
#         search_query |= Q(name__icontains=char)

#     # Initialize results
#     product_results = []
#     pet_results = []
#     category_results = []
#     error_message = ""

#     # Search in the Pet model
#     pet_results = Pet.objects.filter(Q(name__icontains=query_string) | Q(description__icontains=query_string))

#     # Search in the Product model
#     product_results = Products.objects.filter(Q(name__icontains=query_string) | Q(description__icontains=query_string))

#     # Search in the Category model
#     category_results = Category.objects.filter(name__icontains=query_string)

#     # Check if there are results
#     if not product_results and not pet_results and not category_results:
#         error_message = "No results found for your search."

#     context = {
#         'product_results': product_results,
#         'pet_results': pet_results,
#         'category_results': category_results,
#         'query': query_string,
#         'error_message': error_message,
#     }

#     return render(request, 'user/search.html', context)
    

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType


@login_required
def add_to_cart(request, item_type, item_id):
    # Determine whether the item is a Product or a Pet
    if item_type == 'product':
        content_type = ContentType.objects.get_for_model(Products)
        item = get_object_or_404(Products, id=item_id)
    elif item_type == 'pet':
        content_type = ContentType.objects.get_for_model(Pet)
        item = get_object_or_404(Pet, id=item_id)
    else:
        return redirect('view_cart')  # Invalid type

    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=item.id
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
        'total_price': cart.total_price(),
    }
    return render(request, 'user/cart.html', context)
   

def increment_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def decrement_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')   

def checkout_view(request):
    if request.method == "POST":
        # Handle your payment processing logic here
        cart = Cart.objects.get(user=request.user)  # Assuming each user has one cart
        print(cart)
        # Clear all cart items for the user's cart
        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, "Checkout successful! Your cart has been cleared.")
        return redirect('view_cart')  # Redirect to cart or a success page

    return render(request, 'user/checkout.html')


def pet_booking(request, pet_id):
    pet_obj = Pet.objects.get(id=pet_id)
    print("&&&&&&&&&&&&&&&&&&&&", pet_obj)
    return render(request, "user/pet_booking.html", {'pet': pet_obj})

def booking(request):
    print("%%%%%%%%%%",request.POST)
    user_lid = request.session['user_id']
    product_id = request.POST['product_id']
    quantity = request.POST['quantity']
    print(request.POST, "=================================")
    print(product_id, "PPPPPPPPPPPPPPPPPPPPPPP")
    print(quantity, "qqqqqqqqqqqqqqqqqqqqqqq")
    print(user_lid, "lllllllllllllllllllllllll")
    p_ob = Pet.objects.get(id=product_id)
    quant = 0
    if quantity.strip():  # Check if the string is not empty after stripping whitespace
        quant = int(quantity)
    else:
        # Handle the case where quantity is empty, e.g., set a default value or show an error message
        print("Error: Quantity is empty.")
        # You may also want to return or raise an exception depending on your application's logic.
    tt = int(p_ob.price) * quant
    print(tt, "price=====================tt========")
    stock = p_ob.stock_level
    print(stock, "SSSSSSSSSSSSSSSSSSSSSSSSS")
    quant = 0
    if quantity.strip():  # Check if the string is not empty after stripping whitespace
        quant = int(quantity)
    else:
        # Handle the case where quantity is empty, e.g., set a default value or show an error message
        print("Error: Quantity is empty.")
        # You may also want to return or raise an exception depending on your application's logic.

    no_stock = int(stock) - int(quant)
    print(no_stock, "OOOOOOOOOOOOOOOOOOOO")
    if stock >= quant:
        up = Pet.objects.get(id=product_id)
        up.stock_level = no_stock
        up.save()
        q = BookingTable.objects.filter(USER_id=user_lid, Status='booked')

        if len(q) == 0:
            print("%%%%%%%%%%%%%%%%%%%%%$444444444444444")
            obe = BookingTable()
            obe.Total = tt
            obe.Status = 'booked'
            obe.Date = datetime.now().strftime("%Y-%m-%d")
            obe.USER = User.objects.get(id=user_lid)
            obe.save()
            obe1 = BookingDetails()
            obe1.Quantity = quantity
            obe1.BOOK = obe
            obe1.Status = 'booked'
            obe1.PET = up
            obe1.save()
            return HttpResponse('''<script>alert("Booked"); window.location="/cus_home"</script>''')
        else:
            total = int(p_ob.price) + int(tt)
            print(total, "KKKKKKKKKKKKKKKK")

            obr = BookingTable.objects.get(id=q[0].id)
            obr1 = BookingDetails()
            obr1.Quantity = quantity
            obr1.BOOK = obr
            obr1.PET = up
            obr1.Status = "booked"
            obr1.save()
            return HttpResponse('''<script>alert("Booked"); window.location="/cus_home"</script>''')
    else:
        return HttpResponse('''<script>alert("out of stock"); window.location="/cus_home"</script>''')


def manage_booking(request):
    booking_details = BookingDetails.objects.all()
    return render(request, "administrator/manage_booking.html", {'bookings': booking_details})

def cancel_booking(request, booking_id):
    booking_obj = BookingDetails.objects.get(id=booking_id)
    booking_obj.Status = "cancelled"
    booking_obj.save()
    return HttpResponse('''<script>alert("Cancelled"); window.location="/manage_booking"</script>''')


# ////////////////////////////////////// delivery boy ///////////////////////////////////////


def deliveryboy_home(request):
    return render(request, "deliveryboy/home.html")

def view_order(request):
    obj = AssignTable.objects.all()
    return render(request, "deliveryboy/view_order.html",{'orders': obj})

def update_delivery(request):
    return render(request, "deliveryboy/update_delivery.html")
