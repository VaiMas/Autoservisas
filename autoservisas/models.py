from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
import pytz
from tinymce.models import HTMLField
from PIL import Image
utc = pytz.UTC



# Create your models here.
class CarModel(models.Model):
    manufacturer = models.CharField(verbose_name='Manufacturer', max_length=200, help_text='Enter Car manufacturer')
    model = models.CharField(verbose_name='Model', max_length=200, help_text='Enter model name')

    def __str__(self):
        return f"{self.manufacturer} {self.model}"

    class Meta:
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'


class Car(models.Model):
    licence_plate = models.CharField(verbose_name='Licence plate', max_length=10)
    owner = models.CharField(verbose_name='Owner', null=True, max_length=200)
    vin_code = models.CharField(verbose_name='VIN code', max_length=13)
    car_model = models.ForeignKey('CarModel', verbose_name='Model', on_delete=models.SET_NULL, null=True, blank=True)
    cover = models.ImageField('Image', upload_to='covers', null=True, blank=True)
    description = HTMLField('Description', null=True, blank=True)

    def __str__(self):
        return f"{self.owner} {self.car_model} {self.licence_plate} {self.vin_code}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Service(models.Model):
    name = models.CharField(verbose_name='Name', max_length=200)
    price = models.FloatField(verbose_name='Price')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Order(models.Model):
    due_date = models.DateTimeField(verbose_name='Due Date', null=True, blank=True)
    car = models.ForeignKey('Car', verbose_name='Car', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    @property
    def is_overdue(self):
        if self.due_date and datetime.datetime.today().replace(tzinfo=utc) > self.due_date.replace(tzinfo=utc):
            return True
        return False

    @property
    def total_sum(self):
        sum = 0
        orderline = OrderLine.objects.filter(order=self.id)
        for line in orderline:
            sum += line.service.price * line.qty
        return sum

    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('order-detail', args=[str(self.id)])


    CAR_STATUS = (
        ('a', 'Approved'),
        ('p', 'Processing'),
        ('d', 'Done'),
        ('c', 'Canceled'),
    )

    status = models.CharField(
        max_length=1,
        choices=CAR_STATUS,
        blank=True,
        default='p',
        help_text='Status',
    )

    def __str__(self):
        return f"{self.car}: {self.car.owner}, {self.due_date}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderReview(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Review', max_length=2000)


class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name="Order", on_delete=models.CASCADE, null=True, related_name='lines')
    service = models.ForeignKey('Service', verbose_name="Service", on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField("Quantity")

    @property
    def item_sum(self):
        return self.service.price * self.qty

    def get_absolute_url(self):
        """Nurodo konkretaus aprašymo galinį adresą"""
        return reverse('order-detail', args=[str(self.id)])


    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'


    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default="default.png", upload_to="profile_pics")

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self,  *args, **kwargs):
        super().save()
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
