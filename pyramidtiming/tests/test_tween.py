# coding=utf-8
import unittest
import mock
from pyramidtiming.tween import includeme
from pyramid import testing


class TestPyramidTimingIncludme(unittest.TestCase):

    def test_includme(self):
        config = mock.Mock()
        config.registry.settings = {}

        includeme(config)
        self.assertEqual(config.add_tween.call_count, 0)

        config.registry.settings = {'do_timing': True}

        includeme(config)
        config.add_tween.assert_called_once_with(
            'pyramidtiming.pyramidtiming.tween.timing_tween_factory')


class TestPyramidTimingFactory(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.registry = self.config.registry
        self.handler = mock.Mock(name='handler')

    def test_tween_factory(self):
        from pyramidtiming.tween import timing_tween_factory

        timing_tween_factory(self.handler, self.registry)

    def test_tween_factory_name(self):
        from pyramidtiming.tween import timing_tween_factory

        tween = timing_tween_factory(self.handler, self.registry)

        self.assertEqual(tween.__name__, 'timing_tween')


class TestPyramidTween(unittest.TestCase):

    def setUp(self):
        self.response = mock.Mock(name='response', status_code=200)
        self.handler = mock.Mock(name='handler', return_value=self.response)
        self.request = mock.Mock(name='request')

        from pyramidtiming.tween import timing_tween_factory
        self.tween = timing_tween_factory(self.handler, None)

    def _call(self):
        return self.tween(self.request)

    @mock.patch('pyramidtiming.tween.time')
    def test_tween(self, mock_time):
        mock_time.side_effect = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
        self.response.status_code = 200
        self.request.method = 'GET'
        with mock.patch('pyramidtiming.tween.log') as log:
            self._call()
        log.debug.assert_called_with(
            'The request {} took 1.0 seconds with status code {}'.format(
                self.request.method, self.response.status_code),
            extra={'RESPONSE_CODE': self.response.status_code,
                   'REQUEST_METHOD': self.request.method,
                   'RANGE_CODE': '{}xx'.format(str(
                       self.response.status_code)[0]),
                   'REQUEST_PROCESS_TIME': 1.0})

        self.request.method = 'POST'
        self.response.status_code = 302
        with mock.patch('pyramidtiming.tween.log') as log:
            self._call()
        log.debug.assert_called_with(
            'The request {} took 1.0 seconds with status code {}'.format(
                self.request.method, self.response.status_code),
            extra={'RESPONSE_CODE': self.response.status_code,
                   'REQUEST_METHOD': self.request.method,
                   'RANGE_CODE': '{}xx'.format(str(
                       self.response.status_code)[0]),
                   'REQUEST_PROCESS_TIME': 1.0})

        self.request.method = 'PUT'
        self.response.status_code = 403
        with mock.patch('pyramidtiming.tween.log') as log:
            self._call()
        log.debug.assert_called_with(
            'The request {} took 1.0 seconds with status code {}'.format(
                self.request.method, self.response.status_code),
            extra={'RESPONSE_CODE': self.response.status_code,
                   'REQUEST_METHOD': self.request.method,
                   'RANGE_CODE': '{}xx'.format(str(
                       self.response.status_code)[0]),
                   'REQUEST_PROCESS_TIME': 1.0})

        self.request.method = 'PATCH'
        self.response.status_code = 501
        with mock.patch('pyramidtiming.tween.log') as log:
            self._call()
        log.debug.assert_called_with(
            'The request {} took 1.0 seconds with status code {}'.format(
                self.request.method, self.response.status_code),
            extra={'RESPONSE_CODE': self.response.status_code,
                   'REQUEST_METHOD': self.request.method,
                   'RANGE_CODE': '{}xx'.format(str(
                       self.response.status_code)[0]),
                   'REQUEST_PROCESS_TIME': 1.0})

        self.request.method = 'DELETE'
        self.response.status_code = 601
        with mock.patch('pyramidtiming.tween.log') as log:
            self._call()
        log.debug.assert_called_with(
            'The request {} took 1.0 seconds with status code {}'.format(
                self.request.method, self.response.status_code),
            extra={'RESPONSE_CODE': self.response.status_code,
                   'REQUEST_METHOD': self.request.method,
                   'RANGE_CODE': 'xxx', 'REQUEST_PROCESS_TIME': 1.0})

    @mock.patch('pyramidtiming.tween.time')
    def test_tween_exception(self, mock_time):
        mock_time.side_effect = [1, 2]

        self.response.status_code = 200
        self.handler.side_effect = Exception('test')
        self.request.method = 'GET'
        with mock.patch('pyramidtiming.tween.log') as log:
            with self.assertRaises(Exception) as e:
                self._call()
            self.assertEqual(e.exception.message, 'test')
        log.debug.assert_called_with(
            'The request {} took 1.0 seconds with status code {}'.format(
                self.request.method, 'exc'),
            extra={'RESPONSE_CODE': 'exc',
                   'REQUEST_METHOD': self.request.method,
                   'REQUEST_PROCESS_TIME': 1.0})


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPyramidTimingIncludme))
    suite.addTest(unittest.makeSuite(TestPyramidTimingFactory))
    suite.addTest(unittest.makeSuite(TestPyramidTween))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
