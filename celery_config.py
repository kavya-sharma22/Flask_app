from celery.schedules import crontab

beat_schedule = {
    "reload-daily-tasks-everyday-7am": {
        "task": "app.tasks.celery_tasks.reload_daily_tasks",
        "schedule": crontab(hour=7, minute=0),  # Har subah 7 baje chalega
    },
}
