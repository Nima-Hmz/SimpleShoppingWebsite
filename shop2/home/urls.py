from django.urls import path 
from .views import *


app_name = "home"

urlpatterns = [

    path("", Index.as_view(), name="index"),
    path("Product/<slug:slug>", ProductDetails.as_view(), name="product_details"),
    path("search/", SearchView.as_view(), name="search"),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    path("contact/", Contact.as_view(), name="contact"),
    path("faq/", FAQ.as_view(), name="faq"),
    path("blog/", BlogView.as_view(), name="blog"),
    path("category/<slug:slug>/", CategoryView.as_view(), name="category"),


]