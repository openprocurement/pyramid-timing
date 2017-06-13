# coding=utf-8
import unittest
import mock
import json
import webob
import webtest
from flask import Flask, g, request
from flask_testing import TestCase
from webob.dec import wsgify
from pyramidtiming.tween import get_request_metrics, factory, setup_middleware
from pyramidtiming.flask_middleware import before_request, after_request


def app(request, status_code):
    return webob.Response(json.dumps({'status': 'ok'}),
                          status_code=status_code,
                          content_type='application/json')


class TestPyramidTimingMiddleware(unittest.TestCase):

    def load_app(self):
        return get_request_metrics(wsgify(app,
                                          args=(self.status_code,)))

    @mock.patch('pyramidtiming.utils.time')
    def test_middleware(self, mock_time):
        mock_time.side_effect = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        for i in xrange(2, 6):
            self.status_code = i * 101
            self.app = webtest.TestApp(self.load_app())
            with mock.patch('pyramidtiming.utils.log') as log:
                self.app.get('/', status=self.status_code)
            log.debug.assert_called_with(
                'The request GET took 1.0 seconds with status code {}'.format(
                    self.status_code),
                extra={'RESPONSE_CODE': self.status_code,
                       'REQUEST_METHOD': 'GET',
                       'RANGE_CODE': '{}xx'.format(str(self.status_code)[0]),
                       'REQUEST_PROCESS_TIME': 1.0})

        self.status_code = 101
        self.app = webtest.TestApp(self.load_app())
        with mock.patch('pyramidtiming.utils.log') as log:
            self.app.get('/', status=self.status_code)
        log.debug.assert_called_with(
            'The request GET took 1.0 seconds with status code {}'.format(
                self.status_code),
            extra={'RESPONSE_CODE': self.status_code, 'REQUEST_METHOD': 'GET',
                   'RANGE_CODE': 'xxx', 'REQUEST_PROCESS_TIME': 1.0})

        with mock.patch('webob.Response') as mock_resp:
            mock_resp.side_effect = Exception('test_exc')
            with mock.patch('pyramidtiming.utils.log') as log:
                with self.assertRaises(Exception) as e:
                    self.app.post('/')
        log.debug.assert_called_with(
            'The request POST took 1.0 seconds with status code exc',
            extra={'RESPONSE_CODE': 'exc', 'REQUEST_METHOD': 'POST',
                   'REQUEST_PROCESS_TIME': 1.0})
        self.assertEqual(e.exception.message, 'test_exc')

    def test_factory(self):
        obj = factory({})
        self.assertEqual(obj.middleware.func_name, 'get_request_metrics')


class TestFlaskTimingMiddlewareWOBeforeRequest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.after_request(after_request)
        self.webapp = app.test_client()
        return app

    def test_after_request(self):
        with self.app.app_context():
            self.webapp.get('/')
            self.assertEqual(hasattr(g, 'flask_request_start_time'), False)


class TestFlaskTimingMiddleware(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        setup_middleware(app)
        self.webapp = app.test_client()
        return app

    @mock.patch('pyramidtiming.flask_middleware.time')
    def test_before_request(self, mock_time):
        mock_time.time.return_value = 1
        with self.app.app_context():
            resp = self.webapp.get('/')
            self.assertEqual(g.flask_request_start_time, 1)

    def test_setup_middleware(self):
        app = mock.Mock(name='app')
        setup_middleware(app)
        app.before_request.assert_called_once_with(before_request)
        app.after_request.assert_called_once_with(after_request)
