from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from Pizza.models import Pizza,PizzaOptions
from Orders.models import Orders



# Create your views here.
@api_view(['GET'])
def home(request):
    pizzas = Pizza.objects.all()
    orders = Orders.objects.all()
    return render(request,'Home/all.html',{'pizzas':pizzas,'orders':orders})


