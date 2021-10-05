from django.shortcuts import render
from django.http import HttpResponse
from .models import Car, CarModel, Order, Service

# Create your views here.

def index(request):
    num_cars = Car.objects.all().count()
    num_models = CarModel.objects.all().count()

    # Laisvos knygos (tos, kurios turi statusą 'g')
    num_order_status = Order.objects.filter(status__exact='d').count()

    # Kiek yra autorių
    num_orders = Order.objects.count()

    num_services = Service.objects.count()

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'num_cars': num_cars,
        'num_instances': num_models,
        'num_order_status': num_order_status,
        'num_orders': num_orders,
        'num_services': num_services,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)