from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from userprofile.models import Userprofile
from .models import Product, Order, OrderItem
from .forms import OrderForm
from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)

    if product.no_of_items >= 1:
        cart.add(product_id)
        product.no_of_items = product.no_of_items - 1
        product.save()
    else:
        messages.info(request, "The item is no more in stock.")
        return redirect('cart_view')

    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'cart':cart
    })

@login_required
def checkout(request):
    cart = Cart(request)
    user = Userprofile.objects.get(user=request.user)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item['product']
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            

            if order.paid_amount > user.wallet:
                messages.info(request, "Your cart does not contain enough money")
                return redirect('cart_view')
            else:
                user.wallet = user.wallet - order.paid_amount
                user.save()
                order.save()

                for item in cart:
                    product = item['product']
                    quantity = int(item['quantity'])
                    price = product.price * quantity

                    item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

            cart.clear()

            return redirect('frontpage')
    else:
        form = OrderForm

    return render(request, 'store/checkout.html', {
        'cart':cart,
        'form':form
    })

def change_quantity(request, product_id):
    action = request.GET.get('action', '')
    product = Product.objects.get(pk=product_id)

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        if product.no_of_items >= quantity:
            cart.add(product_id, quantity, True)
            product.no_of_items = product.no_of_items - quantity
            product.save()
        else:
            messages.info(request, "The item is no more in stock.")
            return redirect('cart_view')
            

    return redirect('cart_view')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'store/product_detail.html', {
        'product':product
    })


