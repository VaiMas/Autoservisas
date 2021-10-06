from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Car, CarModel, Order, Service
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q


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
        'num_models': num_models,
        'num_order_status': num_order_status,
        'num_orders': num_orders,
        'num_services': num_services,
    }

    # renderiname index.html, su duomenimis kintamąjame context
    return render(request, 'index.html', context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars
    }
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 1
    template_name = 'orders.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(Q(owner__icontains=query) | Q(vin_code__icontains=query) | Q(
        licence_plate__icontains=query) | Q(car_model__manufacturer__icontains=query) | Q(
        car_model__model__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})
