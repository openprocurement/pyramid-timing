# coding=utf-8
import time
import logging
from flask import g, request

log = logging.getLogger(__name__)


def get_response(request, app=None, handler=None):
    start = time.time()
    try:
        if app is not None:
            response = request.get_response(app)
        if handler is not None:
            response = handler(request)
    except:
        delta = time.time() - start
        log_metrics(request, delta)
        raise
    else:
        delta = time.time() - start
        log_metrics(request, delta, response)
        return response


def log_metrics(request, delta, response=None, endpoint=None):
    if response is None:
        log_info = {
            'REQUEST_PROCESS_TIME': round(delta, 4),
            'REQUEST_METHOD': request.method,
            'RESPONSE_CODE': 'exc'
        }
    else:
        if 200 <= response.status_code < 600:
            range_code = '{}xx'.format(response.status_code/100)
        else:
            range_code = 'xxx'
        log_info = {
            'REQUEST_PROCESS_TIME': round(delta, 4),
            'REQUEST_METHOD': request.method,
            'RESPONSE_CODE': response.status_code,
            'RANGE_CODE': range_code
        }
    if endpoint is not None:
        log_info['ENDPOINT'] = endpoint
    log.debug('The request {REQUEST_METHOD} took '
              '{REQUEST_PROCESS_TIME} seconds with status code '
              '{RESPONSE_CODE}'.format(**log_info),
              extra=log_info)

def before_request():
    g.flask_request_start_time = time.time()


def after_request(response):
    if not hasattr(g, 'flask_request_start_time'):
        return response

    endpoint = str(request.endpoint)

    delta = time.time() - g.flask_request_start_time
    log_metrics(request, delta, response, endpoint)

    return response
