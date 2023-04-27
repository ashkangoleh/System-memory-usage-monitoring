'''
Celery Config file
'''
from abc import ABC
from celery import Celery, Task
from celery.backends.redis import RedisBackend
from src.schemas import settings


CELERY_BEAT_SCHEDULE = {
    'ram_usage_every_min': {
        'task': 'src.scheduler.tasks.automation_task',
        'schedule': 60  # every 3 minutes
    },

}

app = Celery('tasks')
app.autodiscover_tasks(['src.scheduler.tasks'])

app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.timezone = settings.CELERY_TIMEZONE

backend = RedisBackend(app=app, url=settings.CELERY_RESULT_BACKEND)


class DeleteKeysTask(Task, ABC):
    """Deleting class for remove celery keys in redis

    Args:
        Task (_type_): Celery class
        ABC (_type_): Abstraction
    """
    def on_success(self, retval, task_id, args, kwargs):
        with backend.client as redis:
            keys = redis.keys('celery*')
            for key in keys:
                redis.delete(key)