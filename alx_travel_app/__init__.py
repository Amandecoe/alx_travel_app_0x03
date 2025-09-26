from .celery import app as celery_app

__all__ = ['celery_app']
#This ensure django load celery when we start the project