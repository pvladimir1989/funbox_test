import time

import unittest

from django.test import Client


class ApiTest(unittest.TestCase):
    post_url = '/visited_links'
    get_url = '/visited_domains'

    def setUp(self) -> None:
        self.client = Client()

    def test_wrong_methods(self):
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, 405)
        response = self.client.post(self.get_url)
        self.assertEqual(response.status_code, 405)

    def test_check_post_errors(self):
        inputs = [
            None,  # пусто
            {},  # пустой json
            b'{link: [[}',  # неправильный json
            b'[]',  # не json
        ]
        for data in inputs:
            response = self.client.post(self.post_url, data,
                                        content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_post_no_links(self):
        json_input = {'links': []}
        json_output = {'status': 'ok'}

        response = self.client.post(self.post_url, json_input,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), json_output)

    def test_save_links(self):
        json_input = {
            'links': [
                'https://ya.ru',
                'https://ya.ru?q=123',
                'funbox.ru',
                'https://stackoverflow.com/questions/11828270/how-to-exit-the-vim'
                '-editor ',
            ],
        }
        json_output = {'status': 'ok'}

        response = self.client.post(self.post_url, json_input,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), json_output)

    def test_get_empty_links(self):
        json_output = {'status': 'ok', 'domains': []}

        response = self.client.get(self.get_url + '?from=0&to=1',
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), json_output)

    def test_check_get_errors(self):
        inputs = [
            (None, None),
            ('from=10', None),
            (None, 'to=10'),
            ('from=', 'to='),
            ('from=10', 'to='),
            ('from=', 'to=10'),
            ('from=a', 'to=b'),
        ]
        for start, end in inputs:
            response = self.client.get(
                self.get_url + '?{0}&{1}'.format(start, end),
                content_type='application/json',
            )
            # print(str(response.content))
            self.assertEqual(response.status_code, 400)

    def test_post_and_get_links(self):
        json_input = {
            'links': [
                'https://ya.ru',
                'https://ya.ru?q=123',
                'funbox.ru',
                'https://stackoverflow.com/questions/11828270/how-to-exit-the-vim'
                '-editor ',
            ],
        }
        curr_time = round(time.time())

        # post
        response = self.client.post(self.post_url, json_input,
                                    content_type='application/json')
        self.assertTrue(response.status_code == 201)

        # get
        response = self.client.get(
            self.get_url + '?from={}&to={}'.format(curr_time, curr_time + 200),
            content_type='application/json',
        )
        self.assertTrue(response.status_code == 200)
        domains = (response.json())['domains']
        # print('cur1', response.json(), domains)
        self.assertTrue('ya.ru' in domains)
        self.assertTrue('funbox.ru' in domains)
        self.assertTrue('stackoverflow.com' in domains)
        self.assertTrue(domains.count('ya.ru') == 1)

        response = self.client.get(
            self.get_url + '?from={}&to={}'.format(curr_time + 200, curr_time + 500),
            content_type='application/json',
        )
        self.assertTrue(response.status_code == 200)
        domains = (response.json())['domains']
        # print('cur2', domains)
        self.assertTrue('ya.ru' not in domains)
        self.assertTrue('funbox.ru' not in domains)
        self.assertTrue('stackoverflow.com' not in domains)
