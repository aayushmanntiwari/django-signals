from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from Pizza.models import Pizza,PizzaOptions
from .models import Orders

# Create your views here.

@api_view(['POST'])
def create_order(request):
    size = PizzaOptions.objects.get(id = int(request.POST.get('size')))
    pizza = Pizza.objects.get(id= int(request.POST.get('product_id')))
    quantity = int(request.POST.get('quantity'))
    orders = Orders.objects.create(pizza=pizza,size=size,user=User.objects.get(id = 1),quantity=quantity)
    orders.save()
    return redirect('/')

@api_view(['GET'])
def view_order(request,id=None):
    order = Orders.objects.get(id = id)
    progress_percentage = 20
    if order.status == 'Order Recieved':
        progress_percentage = 20
    elif order.status == 'Baking':
        progress_percentage = 40
    elif order.status == 'Baked':
        progress_percentage = 60
    elif order.status == 'Out for delivery':
        progress_percentage = 80
    elif order.status == 'Order delivered':
        progress_percentage = 100
    return render(request,'Orders/orders.html',{'order':order,'progress_percentage':progress_percentage})






