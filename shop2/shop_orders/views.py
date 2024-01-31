from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem
from accounts.models import Customer
from django.conf import settings
import requests
import json
from django.contrib import messages
from home.models import Category


# Create your views here.


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        info = False
        if request.user.is_authenticated:
            logged_in = True
            customer = Customer.objects.get(user=request.user)
            if customer.full_address and customer.city and customer.postal_code is not None:
                info = True
        else:
            logged_in = False
            
        context = {
            'logged_in':logged_in,
            'cart':cart,
            'info':info,
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False)
        }
        return render(request, "shop_orders/cart.html", context)
    

class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            available = product.available_check()
            if available:
                try:
                    cart.add(product, form.cleaned_data['quantity'])
                    product.decrease_quantity(form.cleaned_data['quantity'])
                except:
                    messages.error(request, "موجودی این کالا در انبار تمام شده است", 'danger')
                    return redirect("home:index")

            else:
                messages.error(request, "موجودی این کالا در انبار تمام شده است", 'danger')
                return redirect("home:index")

        return redirect("shop_orders:cart") 


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = cart.remove(product)
        product.increase_quantity(quantity)
        return redirect('shop_orders:cart')
    

class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user1 = request.user
        customer = Customer.objects.get(user=user1)
        order = get_object_or_404(Order, id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        total_price = order.get_total_price()
        buy = True 
        if total_price <= 0:
            buy = False
        if Customer.objects.get(user=request.user).full_address is not None:

            context = {
                'order':order,
                'buy':buy,
                'left_cat':Category.objects.filter(left=True),
                'right_cat':Category.objects.filter(left=False),
                'customer':customer,
                'items':order_items
            }
            return render(request, "shop_orders/checkout.html", context)
        
        else:
            messages.error(request, "ابتدا اطلاعات حساب خود را تکمیل کنید", 'danger')
            return redirect("shop_orders:cart")
        
class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        user1 = request.user
        if Customer.objects.filter(user=user1).exists():

            customer = Customer.objects.get(user=user1) 
            if customer.full_address is not None and cart.get_total_price() is not 0:
                order = Order.objects.create(user=customer)
                for item in cart:
                    OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                return redirect('shop_orders:order_detail', order.id)
            else:
                messages.error(request, "لطفا مبلغ نهایی و اطلاعات تکمیلی حساب خود را چک کنید", 'danger')
                return redirect("shop_orders:cart")
        else:
            messages.error(request, "این کاربر یک مشتری نیست. لطفا با یک  کاربر مشتری وارد شوید", 'danger')
            return redirect("home:index")
    

#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'



ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8000/orders/vertify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id':order.id,
        }
    
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": description,
            "Phone": order.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    url = f"{ZP_API_STARTPAY}{response['Authority']}"
                    return redirect(url)
                else:
                    messages.error(request, "مشکل در اتصال به درگاه پرداخت", 'danger')
                    return {'status': False, 'code': str(response['Status'])}
                
            messages.error(request, "مشکل در اتصال به درگاه پرداخت", 'danger')
            return redirect("home:index")
        
        except requests.exceptions.Timeout:
            messages.error(request, "پایان مهلت زمان اتصال", 'danger')
            return redirect("home:index")
        except requests.exceptions.ConnectionError:
            messages.error(request, "مشکل در اتصال", 'danger')
            return redirect("home:index")
        

class OrderVertifyView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        user1 = request.user
        authority = request.GET['Authority']
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Authority":authority
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                customer = Customer.objects.get(user=user1)
                order.paid = True
                order.save()
                cart.clear()
                messages.success(request, "تراکنش موفق بود", 'success')
                return redirect("home:index")
            else:
                messages.error(request, "تراکنش ناموفق بود و یا توسط کاربر لغو شد", 'danger')
                return redirect("home:index")
        else:
            messages.error(request, "تراکنش ناموفق بود و یا توسط کاربر لغو شد", 'danger')
            return redirect("home:index")
 
