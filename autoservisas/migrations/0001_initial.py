# Generated by Django 3.2.7 on 2021-10-05 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automobilio_modelis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marke', models.CharField(help_text='Įveskite atomobili marke', max_length=200, verbose_name='Marke')),
                ('modelis', models.CharField(help_text='Įveskite atomobili modelis', max_length=200, verbose_name='Modelis')),
            ],
            options={
                'ordering': ['marke', 'modelis'],
            },
        ),
        migrations.CreateModel(
            name='Automobilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val_numeris', models.CharField(help_text='Įveskite Valstybini numeri', max_length=10, verbose_name='Vasltybinis numeris')),
                ('klientas', models.CharField(max_length=200, verbose_name='Klientas')),
                ('vin', models.CharField(max_length=13, verbose_name='VIN')),
                ('automobilis', models.ForeignKey(help_text='Pasirinkite automobilio modeli', null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.automobilio_modelis')),
            ],
        ),
        migrations.CreateModel(
            name='Paslauga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(max_length=200, verbose_name='Pavadinimas')),
                ('kaina', models.FloatField(max_length=200, verbose_name='Kaina')),
            ],
        ),
        migrations.CreateModel(
            name='Uzsakymas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('suma', models.FloatField(max_length=200, verbose_name='Suma')),
                ('automobilis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.automobilis')),
            ],
        ),
        migrations.CreateModel(
            name='Uzsakymo_eilute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiekis', models.IntegerField(max_length=4, verbose_name='Kiekis')),
                ('kaina', models.FloatField(max_length=10, verbose_name='Kaina')),
                ('paslauga', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.paslauga')),
                ('uzsakymas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservisas.uzsakymas')),
            ],
        ),
    ]
