from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'main/home.html')

def all_products(request):
    return render(request,'product_list/register.html')
