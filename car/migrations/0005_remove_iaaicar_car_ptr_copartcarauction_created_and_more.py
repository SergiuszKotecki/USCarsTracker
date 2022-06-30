# Generated by Django 4.0.5 on 2022-06-30 17:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0004_copartcarauction_delete_carauction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='iaaicar',
            name='car_ptr',
        ),
        migrations.AddField(
            model_name='copartcarauction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='copartcarauction',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='copartcarauction',
            name='loot_id',
            field=models.CharField(default=123456, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='copartcarauction',
            name='refresh_data',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='copartcarauction',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car'),
        ),
        migrations.DeleteModel(
            name='CopartCar',
        ),
        migrations.DeleteModel(
            name='IAAICar',
        ),
    ]