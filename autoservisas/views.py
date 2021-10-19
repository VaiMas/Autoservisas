from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Car, CarModel, Order, Service,  OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import OrderReviewForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from .forms import OrderReviewForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext as _


# Create your views here.

def index(request):
    num_cars = Car.objects.all().count()
    num_models = CarModel.objects.all().count()

    # Laisvos knygos (tos, kurios turi statusą 'g')
    num_order_status = Order.objects.filter(status__exact='d').count()

    # Kiek yra autorių
    num_orders = Order.objects.count()

    num_services = Service.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # perduodame informaciją į šabloną žodyno pavidale:
    context = {
        'num_cars': num_cars,
        'num_models': num_models,
        'num_order_status': num_order_status,
        'num_orders': num_orders,
        'num_services': num_services,
        'num_visits': num_visits,
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


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order.html'
    form_class = OrderReviewForm

    class Meta:
        ordering = ['car']

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderReviewForm(initial={'order': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


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

class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).filter(status__exact='p').order_by('due_date')


class OrderByUserDetailView(FormMixin, LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = 'user_order.html'
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(OrderByUserDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderReviewForm(initial={'order': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderByUserDetailView, self).form_valid(form)

class OrderByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = ['car', 'due_date']
    success_url = "/autoservisas/myorders/"
    template_name = 'user_order_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

class OrderByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    fields = ['car', 'due_date']
    success_url = "/autoservisas/myorders/"
    template_name = 'user_order_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.client

class OrderByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    success_url = "/autoservisas/myorders/"
    template_name = 'user_order_delete.html'

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.client

class OrderLineByUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderLine
    fields = ['service', 'qty']
    template_name = 'user_orderline_form.html'

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("my-order", kwargs={"pk": pk})


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, _('User name {} already in use!'.format(username)))
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, _(f'Email {email} already in use!'))
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
        else:
            messages.error(request, _('Passwords do not match'))
            return redirect('register')
    return render(request, 'register.html')

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _(f"Profile updated"))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)