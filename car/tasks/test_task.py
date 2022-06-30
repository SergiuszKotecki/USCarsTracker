from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from car.models import CopartCar
from car.models import CopartCarAuction
from car.tasks.CopartScrapper import read_car_data


@util.close_old_connections
def delete_old_job_executions(max_age=304_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

# @sync_to_async
def async_copart_updater():
    print("Start run_async_scrapper()")
    # run_async_scrapper()
    copart_cars = CopartCar.objects.all()
    print([car.loot_id for car in copart_cars])
    print("End run_async_scrapper()")


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

    scheduler.add_job(copart_cart_updater,
                      trigger=CronTrigger(second="*/59"),
                      name="Copart_cart_updater",
                      id="Copart_cart_updater",
                      replace_existing=True,
                      max_instances=1
                      )

    scheduler.add_job(async_copart_updater,
                      trigger=CronTrigger(second="*/30"),
                      name="Async_Copart_cart_updater",
                      id="Async_Copart_cart_updater",
                      replace_existing=True,
                      max_instances=1
                      )

    scheduler.add_job(delete_old_job_executions,
                      trigger=CronTrigger(
                          day_of_week="mon", hour="00", minute="00"
                      ),  # Midnight on Monday, before start of the next work week.
                      id="delete_old_job_executions",
                      max_instances=1,
                      replace_existing=True,
                      )

    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()
