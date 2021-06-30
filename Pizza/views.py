from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http.response import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from .models import PizzaOptions

# Create your views here.
@api_view(['GET'])
def loadpizzaoptions(request,id=None):
    pizzoptions= PizzaOptions.objects.filter(pizza_id = id)
    context = {
        'pizzoptions':pizzoptions,
    } 
    data = {'rendered_table': render_to_string('Pizza/load-option.html',context=context)}
    return JsonResponse(data)

@api_view(['GET'])
def optionbasedonselection(request,option_id=None):
    pizzoption= PizzaOptions.objects.get(id = option_id)
    pizzoptions = PizzaOptions.objects.filter(pizza_id = pizzoption.pizza.id)
    context = {
        'pizzoptions':pizzoptions,
        'pizzoption':pizzoption,
        'option_id':option_id,
    } 
    data = {'rendered_table': render_to_string('Pizza/option-selected-data.html',context=context)}
    return JsonResponse(data)