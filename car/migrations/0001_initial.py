# Generated by Django 4.0.1 on 2022-06-19 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VIN', models.CharField(max_length=17)),
                ('odometer_mi', models.IntegerField(blank=True, null=True)),
                ('odometer_km', models.IntegerField(blank=True, null=True)),
                ('run_and_drive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CarAuction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bid', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('buy_now', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('last_update', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CopartCar',
            fields=[
                ('car_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.car')),
                ('loot_id', models.IntegerField()),
            ],
            bases=('car.car',),
        ),
        migrations.CreateModel(
            name='IAAICar',
            fields=[
                ('car_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='car.car')),
                ('loot_id', models.CharField(max_length=20)),
            ],
            bases=('car.car',),
        ),
    ]