import logging
import traceback


logger = logging.getLogger("reviews_app")


class LogExceptionsMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)

        return response

    def process_exception(self, request, exception):
        logger.error("THIS IS ERRROR")
        logger.exception("this is an error!!")




