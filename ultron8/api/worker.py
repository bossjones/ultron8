from raven import Client

from ultron8.api import settings
from ultron8.api.core.celery_app import celery_app

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str):
    return f"test task return {word}"
