import unittest

from cron_monitor import http_client


class TestHttpClient(unittest.TestCase):
    def test_get(self):
        def on_next(response):
            self.assertEqual(response.status_code, 200)
            self.assertIn('json', response.headers['Content-Type'])

        http_client.HttpClient.get('https://jsonplaceholder.typicode.com/posts/1').subscribe(on_next)

    def test_post(self):
        def on_next(response):
            self.assertEqual(response.status_code, 201)
            self.assertIn('json', response.headers['Content-Type'])

        http_client.HttpClient.post('https://jsonplaceholder.typicode.com/posts', json={
            'title': 'foo',
            'body': 'bar',
            'userId': 1
        }).subscribe(on_next)


if __name__ == '__main__':
    unittest.main()
