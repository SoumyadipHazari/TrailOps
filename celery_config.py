import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv


def make_celery():
    load_dotenv()
    celery = Celery(
        "trekking_app",
        broker=os.getenv("broker"),
        backend= os.getenv("backend"),
        include=["tasks"]
    )

    celery.conf.update(
        timezone="Asia/Kolkata",
        enable_utc=False,

        beat_schedule={
            "daily-trek-reminder": {
                "task": "tasks.daily_trek_reminder",
                "schedule": crontab(minute="*"),
            },

            "monthly-activity-report": {
                "task": "tasks.monthly_activity_report",
                "schedule": crontab(
                    day_of_month=1,
                    hour=8,
                    minute=0
                ),
            }
        }
    )
    return celery



celery = make_celery()  