import time

from itest_utils import wait_for_metronome


def before_all(context):
    wait_for_metronome()


def after_scenario(context, scenario):
    """If a metronome client object exists in our context, delete any apps in Marathon and wait until they die."""
    if context.client:
        while True:
            jobs = context.client.list_jobs()
            if not jobs:
                break
            for job in jobs:
                context.client.delete_job(job.id)
            time.sleep(0.5)
