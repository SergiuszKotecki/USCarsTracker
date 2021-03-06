# Generated by Django 4.0.5 on 2022-06-30 17:40

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
                ('VIN', models.CharField(blank=True, max_length=17, null=True)),
                ('odometer_mi', models.IntegerField(blank=True, null=True)),
                ('odometer_km', models.IntegerField(blank=True, null=True)),
                ('run_and_drive', models.BooleanField(default=False)),
                ('year', models.IntegerField(default=2000)),
                ('make', models.CharField(blank=True, max_length=20, null=True)),
                ('model', models.CharField(blank=True, max_length=20, null=True)),
                ('color', models.CharField(choices=[('BK', 'Black'), ('WE', 'White'), ('RD', 'Red'), ('BE', 'Blue')], default='BK', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='CopartCarAuction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_bid', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('buy_now', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('last_update', models.DateTimeField(blank=True, null=True)),
                ('auction_date', models.DateTimeField(blank=True, null=True)),
                ('loot_id', models.CharField(max_length=20, unique=True)),
                ('refresh_data', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car')),
            ],
        ),
        migrations.AddConstraint(
            model_name='copartcarauction',
            constraint=models.UniqueConstraint(fields=('car', 'auction_date'), name='Uniqe car and auction date'),
        ),
    ]
