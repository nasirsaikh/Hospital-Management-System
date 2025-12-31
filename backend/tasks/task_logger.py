import json
import redis
from celery.signals import task_prerun, task_postrun, task_failure

redis_client = redis.Redis(host="localhost", port=6379, db=2)


def save_log(task_id, status, info):
    log = {
        "task_id": task_id,
        "status": status,
        "info": info,
    }
    redis_client.set(task_id, json.dumps(log))


@task_prerun.connect
def task_start_handler(sender=None, task_id=None, **kwargs):
    save_log(task_id, "STARTED", {"task": sender.name})


@task_postrun.connect
def task_success_handler(sender=None, task_id=None, retval=None, **kwargs):
    save_log(task_id, "SUCCESS", {
        "task": sender.name,
        "result": retval
    })


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, traceback=None, **kwargs):
    save_log(task_id, "FAILED", {
        "task": sender.name,
        "error": str(exception),
        "traceback": traceback
    })
