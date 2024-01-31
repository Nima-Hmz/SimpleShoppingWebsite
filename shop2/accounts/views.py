from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, OtpCode
from django.contrib import messages
from utils import send_otp_code
import random
from django.views import View
import datetime as my_datetime
from django.utils import timezone
from shop_orders.models import Order, OrderItem
from home.models import Category

# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:index")
        else:
            messages.error(request, "wrong", 'danger')

    context = {
        'left_cat':Category.objects.filter(left=True),
        'right_cat':Category.objects.filter(left=False)

    }

    return render(request, "accounts/login.html", context)

def user_register(request):
    if request.method == "POST":
        username_filed = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')

        if password == confirm_password:
            if Customer.objects.filter(phone_number=phone).exists():
                messages.error(request, "شماره موبایل تکراری است", 'danger')
                return redirect("accounts:user_register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "ایمیل تکراری است", 'danger')
                    return redirect("accounts:user_register")
                else:
                    if User.objects.filter(username=username_filed).exists():
                        messages.error(request, "نام کاربری تکراری است", 'danger')
                        return redirect("accounts:user_register")
                    else:
                        if OtpCode.objects.filter(phone_number=phone).exists():
                            messages.error(request, "دوباره تلاش کنید", 'danger')
                            OtpCode.objects.filter(phone_number=phone).delete()
                            return redirect("accounts:user_register")
                        else:
                            reandom_code = random.randint(1000, 9999)
                            send_otp_code(phone_number=phone, code=reandom_code)
                            OtpCode.objects.create(phone_number= phone, code=reandom_code)
                            request.session["user_registration_info"] = {

                                'phone_number':phone,
                                'email':email,
                                'username':username_filed,
                                'password':password

                            }
                            messages.success(request, "کد را برای شما از طریق پیامک ارسال کردیم", 'success')
                            return redirect("accounts:register_vertify")
    context = {
        'left_cat':Category.objects.filter(left=True),
        'right_cat':Category.objects.filter(left=False)
        
    }
                        
    return render(request, "accounts/register.html", context) 

class UserRegisterVertifyCode(View):

    def get(self, request):
        try:
            x = request.session['user_registration_info'] 
            context = {
                'left_cat':Category.objects.filter(left=True),
                'right_cat':Category.objects.filter(left=False)
                }
            return render(request, "accounts/register_vertify.html", context)

        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")
            
    
    def post(self, request):
        try:
            user_session = request.session['user_registration_info']
            code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
            user_input = int(request.POST.get("vertifycode"))
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")


        if user_input == code_instance.code:
            temp = code_instance.created
            temp += my_datetime.timedelta(seconds=120)
            now = timezone.now()
            if now < temp:

                user = User.objects.create_user(username=user_session['username'], email=user_session['email'], password=user_session['password'])
                user.save()
                data = Customer(user=user, phone_number=user_session["phone_number"])
                data.save()
                code_instance.delete()
                messages.success(request, "حساب کاربری شما ایجاد شد", 'success')

                #  login after register 
                our_user = authenticate(username=user_session['username'], password=user_session['password'])
                if our_user is not None:
                    login(request, user)
                    return redirect("home:index")
            
            
            else:
                code_instance.delete()
                messages.error(request, "زمان شما به اتمام رسید", 'danger')
                return redirect('accounts:user_register')

        else:
            messages.error(request, "کد وارد شده اشتباه است", 'danger')
            return redirect('accounts:register_vertify')
        



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home:index")


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        user1 = request.user
        my_order = False
        if Customer.objects.filter(user=user1).exists():

            customer = Customer.objects.get(user=user1)
            try:
                orders = Order.objects.filter(user=customer, paid=True)
                last_order = orders.first()
                my_order = True
                
                total_price = last_order.get_total_price()
                items = OrderItem.objects.filter(order=last_order)

            except:
                total_price = 0
                items = {}

            context = {
            'city' : customer.city,
            'province' : customer.province,
            'full_address' : customer.full_address,
            'postal_code' : customer.postal_code,
            'receiver' : customer.receiver,
            'phone_number':customer.phone_number,
            'user_name':user1.username,
            'total_price':total_price,
            'items':items,
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),
            'my_order':my_order
            }

            return render(request, "accounts/address.html", context)
        
        else:
            messages.error(request, "این کاربر یک مشتری نیست. لطفا با یک  کاربر مشتری وارد شوید", 'danger')
            return redirect("home:index")

    def post(self, request):
        province = request.POST.get('province')
        city = request.POST.get('city')
        full_address = request.POST.get('full_address')
        postal_code = request.POST.get('postal_code')
        receiver = request.POST.get('receiver')

        if province != "":
            if city != "":
                if full_address != "" and len(str(full_address)) > 8:
                    if postal_code != "":
                        if receiver != "":
                            user1 = request.user
                            if Customer.objects.filter(user=user1).exists():   
                                customer = Customer.objects.get(user=user1)
                                customer.province = province
                                customer.city = city
                                customer.full_address = full_address
                                customer.postal_code = postal_code
                                customer.receiver = receiver
                                customer.save()
                                messages.success(request, "مشخصات شما ثبت شد", 'success')
                                return redirect("home:index")
                            else:
                                messages.error(request, "این کاربر یک مشتری نیست. لطفا با یک  کاربر مشتری وارد شوید", 'danger')
                                return redirect("home:index")
        messages.error(request, "تمام موارد خواسته شده را به درستی پر کنید", 'danger') 
        return redirect("home:index")
    


class ForgotPasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.error(request, "شما در حساب خود حضور دارید", 'danger')
            return redirect("home:index")
        else:
            context = {
                'left_cat':Category.objects.filter(left=True),
                'right_cat':Category.objects.filter(left=False)
        
            }
            return render(request, "accounts/reset-password.html", context)
            

    def post(self, request):
        if request.user.is_authenticated:
            messages.error(request, "شما در حساب خود حضور دارید", 'danger')
            return redirect("home:index")
        else:
            phone_number = request.POST.get("phone_number")
            if phone_number != "":
                if Customer.objects.filter(phone_number=phone_number).exists():
                    if OtpCode.objects.filter(phone_number=phone_number).exists():
                        messages.error(request, "دوباره تلاش کنید", 'danger')
                        OtpCode.objects.filter(phone_number=phone_number).delete()
                        return redirect("accounts:forgot_password")

                    reandom_code = random.randint(1000, 9999)
                    send_otp_code(phone_number=phone_number, code=reandom_code)
                    OtpCode.objects.create(phone_number= phone_number, code=reandom_code)

                    request.session[0] = phone_number
                    request.session.save()

                    messages.success(request, "پیامک برای شما ارسال شد", 'success')
                    return redirect("accounts:forgot_password_vertify")
                else:
                    messages.error(request, "چنین کاربری وجود ندارد دوباره امتحان کنید", 'danger')
                    return redirect("accounts:forgot_password")
            else:
                messages.error(request, "فیلد درخواست شده را به درستی پر کنید", 'danger')
                return redirect("accounts:forgot_password")


class ForgotPasswordVertifyView(View):
    def get(self, request):
        try:
            x = request.session['0'] 
            context = {
                'left_cat':Category.objects.filter(left=True),
                'right_cat':Category.objects.filter(left=False)
        
            }
            return render(request, "accounts/register_vertify.html", context)
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")
        
    def post(self, request):
        try:
            user_session = request.session["0"]
            code_instance = OtpCode.objects.get(phone_number=user_session)
            user_input = int(request.POST.get("vertifycode"))
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")

        if user_input == code_instance.code:
            temp = code_instance.created
            temp += my_datetime.timedelta(seconds=120)
            now = timezone.now()
            if now < temp:
                code_instance.delete()
                messages.success(request, "شماره شما تایید شد. اکنون رمز جدید برای حساب خود ایجاد کنید", 'success')
                return redirect("accounts:new_password")
            else:
                code_instance.delete()
                messages.error(request, "زمان شما به اتمام رسید", 'danger')
                return redirect("home:index")
        else:
            messages.error(request, "کد اشتباه است دوباره امتحان کنید", 'danger')
            return redirect("accounts:forgot_password_vertify")
        
class ForgotPasswordNewView(View):
    def get(self, request):
        try:
            x = request.session['0'] 
            context = {
                'left_cat':Category.objects.filter(left=True),
                'right_cat':Category.objects.filter(left=False)
        
            }
            return render(request, "accounts/reset-password2.html", context)
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")
    
    def post(self, request):
        try:
            x = request.session['0']
        except:
            messages.error(request, "خطا دوباره تلاش کنید", 'danger')
            return redirect("home:index")

        password = request.POST.get("password")
        if password != "":
            customer = Customer.objects.get(phone_number=request.session['0'])
            customer.user.set_password(password)
            customer.user.save()    
            customer.save()
            messages.success(request, "رمز شما تغییر کرد اکنون میتوانید با رمز جدید وارد حساب خود شوید", 'success')
            return redirect("home:index")





        
                
        