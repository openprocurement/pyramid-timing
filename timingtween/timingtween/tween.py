import time
from pyramid.settings import asbool
import logging

log = logging.getLogger(__name__)


def timing_tween_factory(handler, registry):

    # if timing support is enabled, return a wrapper
    def timing_tween(request):
        start = time.time()
        try:
            response = handler(request)
        except:
            delta = time.time() - start
            log_info = {
                'REQUEST_PROCESS_TIME': delta,
                'REQUEST_METHOD': request.method,
                'RESPONSE_CODE': 'exc'
            }
            log.debug('The request {REQUEST_METHOD} took '
                      '{REQUEST_PROCESS_TIME} seconds with status code '
                      '{RESPONSE_CODE}'.format(**log_info),
                      extra=log_info)
            raise

        else:
            delta = time.time() - start
            if 200 <= response.status_code < 300:
                range_code = '2xx'
            elif 300 <= response.status_code < 400:
                range_code = '3xx'
            elif 400 <= response.status_code < 500:
                range_code = '4xx'
            elif 500 <= response.status_code < 600:
                range_code = '5xx'
            else:
                range_code = 'xxx'
            log_info = {
                'REQUEST_PROCESS_TIME': delta,
                'REQUEST_METHOD': request.method,
                'RESPONSE_CODE': response.status_code,
                'RANGE_CODE': range_code
            }
            log.debug('The request {REQUEST_METHOD} took '
                      '{REQUEST_PROCESS_TIME} seconds with status code '
                      '{RESPONSE_CODE}'.format(**log_info),
                      extra=log_info)
        return response
    return timing_tween


def includeme(config):
    if asbool(registry.settings.get('do_timing')):
        log.info('Init timing tween factory')
        config.add_tween('timingtween.timingtween.tween.timing_tween_factory')
