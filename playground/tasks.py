import time
from storefront.celery import celery # Importing celery object from that module
from celery import shared_task


# @celery.task    # This approach works but couples the storefront app to the playground app

@shared_task
def notify_customers(message):
    print('Sending 10l emails...')
    print(message)
    time.sleep(10)
    print('Emails were successfully send')