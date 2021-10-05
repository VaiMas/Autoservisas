from django.db import models


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
    car_model = models.ForeignKey('CarModel', verbose_name='Model', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.owner}: {self.car_model}, {self.licence_plate}, {self.vin_code}"

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


class OrderLine(models.Model):
    order = models.ForeignKey('Order', verbose_name="Order", on_delete=models.SET_NULL, null=True, related_name='lines')
    service = models.ForeignKey('Service', verbose_name="Service", on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField("Quantity")

    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'


    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"
