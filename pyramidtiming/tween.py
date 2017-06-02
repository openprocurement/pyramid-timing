from pyramid.settings import asbool
from .utils import get_response
from webob.dec import wsgify
import logging

log = logging.getLogger(__name__)


def timing_tween_factory(handler, registry):

    # if timing support is enabled, return a wrapper
    def timing_tween(request):
        try:
            response = get_response(request, handler=handler)
        except:
            raise
        return response
    return timing_tween


@wsgify.middleware
def get_request_metrics(request, app):
    try:
        response = get_response(request, app=app)
    except:
        raise
    return response


def factory(global_config):
    log.info('Init pyramidtiming middleware')
    return get_request_metrics


def includeme(config):
    if asbool(config.registry.settings.get('pyramid_timing', True)):
        log.info('Init timing tween factory')
        config.add_tween(
            'pyramidtiming.tween.timing_tween_factory')
