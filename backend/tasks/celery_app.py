

from celery import Celery
import os
from celery.schedules import crontab

CELERY_BROKER = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(
    "hospital_app",
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND,
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True,

    task_track_started=True,
    task_send_sent_event=True,

    result_backend="redis://localhost:6379/1",
    broker_url="redis://localhost:6379/0",

    task_ignore_result=False,
    worker_send_task_events=True,
    task_serializer="json",
    result_serializer="json",

    beat_scheduler="celery.beat.PersistentScheduler",

    beat_schedule={...}
)


celery.conf.beat_schedule = {

    "daily-appointment-reminders": {

        "task": "tasks.daily_appointment_reminder",
        "schedule": crontab(hour=7, minute=0),
    },


    "monthly-doctor-reports": {

        "task": "tasks.monthly_doctor_report",
        "schedule": crontab(hour=8, minute=0, day_of_month="1"),
    },
}
