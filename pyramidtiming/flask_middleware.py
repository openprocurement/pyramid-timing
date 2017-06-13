# coding=utf-8
import time
from pyramidtiming.utils import log_metrics
from flask import g, request

def before_request():
    g.flask_request_start_time = time.time()


def after_request(response):
    if not hasattr(g, 'flask_request_start_time'):
        return response

    endpoint = str(request.endpoint)

    delta = time.time() - g.flask_request_start_time
    log_metrics(request, delta, response, endpoint)

    return response
