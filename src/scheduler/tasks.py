'''
Task file
this task running with celery beat every 1 min
'''
from sqlalchemy import insert
from src.model import RamUsage
from src.scheduler.config import app, DeleteKeysTask
from src.db import get_db
from src.utils import SystemUsage

@app.task(
    base=DeleteKeysTask
)
def automation_task():
    with SystemUsage() as system_usage:
        for db in get_db():
            data = {
                "total": system_usage['total'],
                "free": system_usage['free'],
                "used": system_usage['used'],
                }
            query = insert(RamUsage)
            db.execute(query, data)
            db.commit()
            return 'Done'