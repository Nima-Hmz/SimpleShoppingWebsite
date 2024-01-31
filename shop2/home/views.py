from typing import Any
from django.shortcuts import render
from django.views import View
from .models import Product
from django.shortcuts import get_object_or_404
from shop_orders.forms import CartAddForm
from .models import Category
from comment.models import Comment
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.contrib import messages
from shop_orders.models import OrderItem
# Create your views here.



class Index(View):

    def get(self, request):

        context = {

            'products':Product.objects.filter(available=True)[:4],
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),
            'best_cat':Category.objects.filter(marked=True)[:3],
            'star_pro':Product.objects.filter(star=True)[:4],
            'offer_pro':Product.objects.filter(offer=True)[:4],
            'sell_star_pro':Product.objects.filter(sell_star=True)[:4],
            'best_day':Product.objects.filter(best_day=True)[:1],
            'best':Product.objects.filter(best=True)[:2],
            'last_one':Product.objects.filter(available=True)[:12] 

        }
        return render(request, "Home/index.html", context)

class CategoryView(View):
    def get(self, request, slug):

        products = Product.objects.filter(category__slug=slug)
        print('------------------' , products)
        paginator = Paginator(products , 6)
        page = request.GET.get('page',1)

        try :
            result = paginator.page(page)
        except PageNotAnInteger :
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)

        context = {

            "category": result,
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),

        }
        return render(request, "Home/category.html", context)

class ProductDetails(View):
    def get(self, request, slug):

        context = {

            'product' : get_object_or_404(Product, slug=slug),
            'form': CartAddForm(),
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),
            'comments' : Comment.objects.filter(forProduct__slug=slug , isActive=True)

        }

        return render(request, "Home/product_details.html", context)
    
    def post(self , request ,slug):
        username = request.user
        product = get_object_or_404(Product, slug=slug)
        orders   = OrderItem.objects.filter(order__user__user=username , order__paid=True , product__slug = slug)
        
        if orders :
            name = request.POST['Name']
            textComment = request.POST['textComment']
            if name and textComment :
                comment = Comment(forProduct=product , userComment=username , nameUser=name , textComment=textComment)
                comment.save()

                messages.success(request, "نظر شما با موفقیت ثبت شد", 'success')

        else:
            messages.error(request, "این محصول توسط شما خریداری نشده است", 'danger')

        context = {
            'product' : get_object_or_404(Product, slug=slug),
            'form': CartAddForm(),
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),
            'comments' : Comment.objects.filter(forProduct__slug=slug , isActive=True)
        }

        
        return render(request, "Home/product_details.html", context) 

class SearchView(View):
    def get(self, request):
        q = request.GET.get("search")
        
        product_list = Product.objects.filter(name__icontains=q)
        
        paginator = Paginator(product_list , 6)
        page = request.GET.get('page',1)

        try :
            result = paginator.page(page)
        except PageNotAnInteger :
            result = paginator.page(1)
        except EmptyPage:
            result = paginator.page(paginator.num_pages)
            
        url = request.get_full_path()
        context = {
            'product_list':result,
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),
            'q':q,
            "url_path" : url,

        }

        return render(request, "Home/search.html", context)
    

class AboutUsView(View):
    def get(self, request):
        context = {
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False)

        }
        return render(request, "Home/about.html", context)

class Contact(View):
    def get(self, request):
        context = {
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False)

        }
        return render(request, "Home/contact.html")

class FAQ(View):
    def get(self, request):
        context = {
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False),

        }
        return render(request, "Home/faq.html", context)
    
class BlogView(View):
    def get(self, request):
        context = {
            'left_cat':Category.objects.filter(left=True),
            'right_cat':Category.objects.filter(left=False)

        }
        return render(request, "Home/blog.html", context)