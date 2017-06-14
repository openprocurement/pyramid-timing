# coding=utf-8
import time
from pyramidtiming.utils import log_metrics
from flask import g, request
import logging

logger = logging.getLogger(__name__)


def before_request():
    g.flask_request_start_time = time.time()


def after_request(response):
    if not hasattr(g, 'flask_request_start_time'):
        return response

    endpoint = str(request.endpoint)

    delta = time.time() - g.flask_request_start_time
    log_metrics(request, delta, response, endpoint)

    return response


def setup_middleware(app):
    app.before_request(before_request)
    app.after_request(after_request)
    logger.info('Init timing middleware in flask app')
