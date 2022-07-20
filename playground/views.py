from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage # this is a third party but extends the Django EmailMessage
import logging

import requests
from .tasks import notify_customers

Key = 'httpbin_result'

@cache_page(5) # Timeout = 5 seconds
def say_hello(request):
    # try:
        # send_mail('subject', 'message', 'hammad@starmech.com', ['hamadstarmech@yahoo.com'])
        # mail_admins('subject', 'message',html_message='<p>HTML MESSAGE </p>') # This will send email to configured site admins
        # Above 2 are direct methods
        # Below is the EmailMessage class wwith more customization options
        # msg = EmailMessage('subject', 'this is message body','from@starmechyahoo.com', ['joshnyboy@djano_ult.com'])
        # msg.attach_file('playground/static/images/nature.jpg')
        # msg.send()
    # --------------------------------------
    #     msg = BaseEmailMessage(template_name='emails/email_hello.html', context={'name': 'StarMech'})
    #     msg.send(to=['StarAdmin@mybuy.com'])
    #
    # except BadHeaderError:
    #     pass
    # notify_customers.delay('Hello Boiy')
    # if cache.get(Key) is None: # Meaning the data is not in cache
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(Key, data, 5)
    # return render(request, 'hello.html', {'name': cache.get(Key)})

    response = requests.get('https://httpbin.org/delay/2')
    data = response.json()
    return render(request, 'hello.html', {'name': data})

logger = logging.getLogger(__name__) #__name__ here == playground.views

class HellowView(APIView):
    # @method_decorator(cache_page(5+60))
    def get(self, request):
        try:
            logger.info('Calling HttpBin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received The Response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')
        return render(request, 'hello.html', {'name': 'Hammad'})