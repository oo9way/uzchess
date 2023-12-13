from django.http import HttpResponse
from django.conf import settings
import traceback
import requests


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                # Format your message here
                message = "**{url}**\n\n{error}\n\n````{tb}````".format(
                    url=request.build_absolute_uri(),
                    error=repr(exception),
                    tb=traceback.format_exc()
                )

                requests.get(url='https://api.telegram.org/bot6545930354:AAHhY_eh2rqs_mSrcFg60TWUoKCtohc9lFY/sendMessage?chat_id=1921103181&text=error')
                # Do now whatever with this message
                # e.g. requests.post(<slack channel/teams channel>, data=message)
                
            return HttpResponse("Error processing the request.", status=500)