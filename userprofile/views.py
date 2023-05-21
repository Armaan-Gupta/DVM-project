from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from store.forms import ProductForm
from django.utils.text import slugify
from store.models import Product, Order, OrderItem
from .models import Userprofile

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    return render(request, 'userprofile/vendor_detail.html', {
        'user':user
    })


@login_required
def my_store(request):
    order_items = OrderItem.objects.filter(product__user=request.user)
    return render(request, 'userprofile/my_store.html', {
        'order_items':order_items,
    })

@login_required
def my_store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'userprofile/my_store_order_detail.html', {
        'order':order
    })


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():            # since the user field is not a part of the form, the validation will be OK, but we need to have the user field as well
            title = request.POST.get('title')
            product = form.save(commit=False)                 # form.save() will give an error because of the above reason, hence we forst create an instance and then add the user field to it. commit=FALSE does not send it to th database
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            messages.success(request, "The product was added!")

            return redirect('my_store')
        
    else:
        form = ProductForm()
        return render(request, 'userprofile/add_product.html', {'form':form,
                                                                'title':'Add Product'})
    
@login_required
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "The product was updated!")
            return redirect('my_store')
    else:
        form = ProductForm(instance=product)
        return render(request, 'userprofile/add_product.html', {'form':form, 
                                                                'title':'Edit Product',
                                                                'product':product})
    
class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/my-store/'

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            is_vendor = form.cleaned_data['is_vendor']
            userprofile = Userprofile.objects.create(user=user,
                                                     is_vendor = is_vendor)
            userprofile.save()

            messages.success(request, f'Your account has been created, You can now login!')
            return redirect('login')
        else:
            return render(request, 'userprofile/register.html', {'form': form})
        
    else:
        form = UserRegisterForm()
        return render(request, 'userprofile/register.html', {'form':form})

# def register_customer(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         print(form)
#         if form.is_valid():
#             form.save()
#             # profile = Userprofile(
#             #     user = User.objects.get(),
#             #     is
#             # )
#             profile.save()
#             messages.success(request, f'Your account has been created, You can now login!')
#             return redirect('login')
        
#     else:
#         form = UserRegisterForm()
#         return render(request, 'userprofile/register_customer.html', {'form':form})
    
# def register_vendor(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been created, You can now login!')
#             return redirect('login')
        
#     else:
#         form = UserRegisterForm()
#         return render(request, 'userprofile/register_vendor.html', {'form':form})
    
@login_required
def profile(request):
    return render(request, 'userprofile/profile.html')

@login_required
def my_orders(request):
    order_items = OrderItem.objects.filter(order__created_by=request.user)
    return render(request, 'userprofile/my_orders.html', {
        'order_items':order_items,
    })
