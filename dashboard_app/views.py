from django.shortcuts import render,redirect
from main_app.models import Main_Category, Product, ProductImage, ProductVariant
from gauth_app.models import Customer
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache

     # ............. User Priventing Authentication...................
          
def admin_required(view_func):
    
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='dashboard_app:dashboard_login'
    )
    return actual_decorator(view_func)


#############################################################################################
                         # User management #
#############################################################################################


def users(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        user = Customer.objects.get(pk=user_id)
        if action == 'block':
            user.is_blocked = True
            messages.success(request, f"{user.email} is blocked.")
        elif action == 'unblock':
            user.is_blocked = False
            messages.success(request, f"{user.email} is unblocked.")

        user.save()

        return redirect('dashboard_app:users')

    # Order the records by email
    customers = Customer.objects.all().order_by('email')
    return render(request, 'dashboard/users.html', {'customers': customers})


#############################################################################################
                            # Login and home #
#############################################################################################

@never_cache
@admin_required
@login_required(login_url='dashboard_app:dashboard_login')
def dashboard_home(request):
    return render(request,'dashboard/home.html')


def dashboard_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            # Log in the superuser
            login(request, user)
            return redirect("dashboard_app:dashboard_home")  # Redirect to your dashboard
        else:
            # Handle incorrect credentials
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return render(request,'dashboard/login.html')



#############################################################################################
            # Main Category Section, All product, Add, update and delete #
#############################################################################################



@never_cache
@admin_required
@login_required(login_url='dashboard_app:dashboard_login')
def main_category(request):
    data = Main_Category.objects.all().order_by('id')
    return render(request,"dashboard/main_category.html",{"data": data})


@never_cache
@admin_required
@login_required(login_url='dashboard_app:dashboard_login')
def add_main_category(request):
    if request.method == 'POST':
        main_category_name = request.POST['main_category_name']
        description = request.POST['description']
        image = request.FILES.get('image')
        delete = request.POST.get('delete', False) == 'True'
        
        # Check the category name is already there
        if Main_Category.objects.filter(name = main_category_name).exists():
            messages.error(request, "Category is already exists.")
            return render(request, 'dashboard/add_main_category.html')

        # Savin Data to the database
        query = Main_Category.objects.create(
            name=main_category_name,
            descriptions=description,
            img=image,
            deleted = delete
        )
        query.save()
        return redirect('dashboard_app:main_category')
    return render(request, 'dashboard/add_main_category.html')


@never_cache
@admin_required
@login_required(login_url='dashboard_app:dashboard_login')
def update_main_category(request, id):
    data = Main_Category.objects.get(id=id)

    if request.method      == 'POST':
        main_category_name = request.POST['main_category_name']
        description        = request.POST['description']
        delete             = request.POST.get('delete', False)

        # Retrieve existing data
        edit = Main_Category.objects.get(id=id)

        # Update fields
        edit.name = main_category_name
        edit.descriptions = description 
        edit.deleted = delete

        if 'image' in request.FILES:
            image = request.FILES['image']
            edit.img = image
        
        # Save updated data
        edit.save()

        return redirect('dashboard_app:main_category')

    return render(request, "dashboard/update_main_category.html", {"data": data})



def soft_delete_category(request, id):
    data = Main_Category.objects.get(id=id)

    data.deleted = not data.deleted
    data.save()

    return redirect('dashboard_app:main_category')


@login_required(login_url='dashboard_app:dashboard_login')
def delete_main_category(request,id):
    data = Main_Category.objects.get(id=id) 
    data.delete()  
    return redirect('dashboard_app:main_category')
 

#############################################################################################
       # Product Section, contains "all_products, add, update and delete product" #
#############################################################################################


@login_required(login_url='dashboard_app:dashboard_login')
def products(request):
    data = Product.objects.all().order_by('id')
    return render(request, "dashboard/products.html", {"data": data})


@never_cache
@admin_required
@login_required(login_url='dashboard_app:dashboard_login')
def add_product(request):
    data = Main_Category.objects.all() 

    if request.method == 'POST':
        # Extracting data from the POST request
        brand = request.POST['brand']
        model = request.POST['model']
        description = request.POST['description']
        color = request.POST['color']
        display_size = request.POST['display_size']
        camera = request.POST['camera']
        network = request.POST.get('network', False) == 'true'
        smart = request.POST.get('smart', False) == 'true'
        battery = request.POST['battery']
        image = request.FILES.get('image')
        delete = request.POST.get('delete', False) == 'True'
        main_category_id = request.POST.get('main_category_id')  

        main_cat = Main_Category.objects.get(id=main_category_id)

        # Create the Product instance with the calculated offer price
        query = Product.objects.create(
            brand=brand,
            model=model,
            description=description,
            color=color,
            display_size=display_size,
            camera=camera,

            network=network,
            smart=smart,
            battery=battery,
            image=image,
            deleted=delete,
            main_category=main_cat,
        )

        # Save multiple images associated with the product
        images = request.FILES.getlist('images')
        for img in images:
            ProductImage.objects.create(product=query, image=img)
            
        return redirect('dashboard_app:products')

    # Render the form if it's not a POST request
    return render(request, 'dashboard/add_product.html', {"data": data})


@login_required(login_url='dashboard_app:dashboard_login')
def update_product(request, id):
    data = Main_Category.objects.all()
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        brand = request.POST['brand']
        model = request.POST['model']
        description = request.POST['description']
        color = request.POST['color']
        display_size = request.POST['display_size']
        camera = request.POST['camera']
        network = request.POST.get('network', False)
        smart = request.POST.get('smart', False)
        battery = request.POST['battery']
        delete = request.POST.get('delete', False)
        images = request.FILES.getlist('images')
        # Retrieve existing data
        edit = Product.objects.get(id=id)

        # Update data in the table
        edit.brand = brand
        edit.model = model
        edit.description = description
        edit.color = color
        edit.display_size = display_size
        edit.camera = camera
        edit.network = network
        edit.smart = smart
        edit.battery = battery
        edit.deleted = delete
        # Update main image only if the user provided
        if 'image' in request.FILES:
            image = request.FILES['image']
            edit.image = image

        edit.save()

        # Remove existing images associated with the product
        existing_images = ProductImage.objects.filter(product=edit)
        for existing_image in existing_images:
            existing_image.delete()

        # Save multiple new images associated with the product
        for img in images:
            ProductImage.objects.create(product=edit, image=img)

        return redirect('dashboard_app:products')

    return render(request, "dashboard/update_product.html", {"product": product, "data": data})



def soft_delete_product(request, id):
    product = Product.objects.get(id=id)

    product.deleted = not product.deleted
    product.save()

    return redirect('dashboard_app:products')



@login_required(login_url='dashboard_app:dashboard_login')
def delete_product(request,id):
    data = Product.objects.get(id=id) 
    data.delete()  
    return redirect('dashboard_app:all_products')



#############################################################################################
                        # Product Varinats management #
#############################################################################################


@login_required(login_url='dashboard_app:dashboard_login')
def all_products(request):
    products = Product.objects.prefetch_related('productvariant_set').all().order_by('id')
    context = {'products': products}
    return render(request, "dashboard/all_products.html", context)


@never_cache
@admin_required
@login_required(login_url='dashboard_app:dashboard_login')
def add_variant(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        # Extracting data from the POST request
        price = request.POST['price']
        ram = request.POST['ram']
        storage = request.POST['storage']
        stock = request.POST['stock']
        offer = request.POST['offer'] 
        product_id = request.POST.get('product_id')

        # Calculate offer price
        offer_price = int(price) - (int(price) * int(offer) / 100)

        # Create the Product instance with the calculated offer price
        query = ProductVariant.objects.create(
            price=price,
            ram=ram,
            storage=storage,
            stock=stock,
            offer=offer,
            offer_price=offer_price,
            product = product
        )
  
        return redirect('dashboard_app:products')

    # Render the form if it's not a POST request
    return render(request, 'dashboard/add_variant.html', {'product':product})


def update_variant(request, id):
    variant = ProductVariant.objects.get(id=id)

    if request.method == 'POST':
        price = request.POST['price']
        ram = request.POST['ram']
        storage = request.POST['storage']
        stock = request.POST['stock']
        offer = request.POST['offer']
        edit = ProductVariant.objects.get(id=id)


        # Udate data in the table
        edit.price = price
        edit.ram = ram
        edit.storage = storage
        edit.stock = stock
        edit.offer = offer
        edit.save()
        
        return redirect('dashboard_app:all_products')

    context = {'variant':variant}
    return render(request, "dashboard/update_variant.html", context)
