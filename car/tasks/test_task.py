from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from car.models import CopartCar
from car.models import CopartCarAuction
from car.tasks.CopartScrapper import read_car_data


def copart_cart_updater():
    copart_cars = CopartCar.objects.all()
    for car in copart_cars:
        copart_car_data = read_car_data(car.loot_id)
        car.VIN = copart_car_data['VIN']
        car.odometer_mi = copart_car_data['odometer_mi']
        car.odometer_km = copart_car_data['odometer_km']
        car.run_and_drive = copart_car_data['r&d']
        car.year = copart_car_data['year']
        car.make = copart_car_data['make']
        car.model = copart_car_data['model']
        car.save(force_update=True)

        if copart_car_data['auction_date']:
            CopartCarAuction.objects.get_or_create(
                auction_date=copart_car_data['auction_date'],
                last_update=copart_car_data['last_update'],
                current_bid=copart_car_data['current_bid'],
                car=car,
            )


def start_aps():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(jobstore=DjangoJobStore())
    scheduler.start()
    scheduler.add_job(copart_cart_updater,
                      'interval',
                      seconds=300,
                      name="Copart_cart_updater",
                      replace_existing=True,
                      max_instances=1)
