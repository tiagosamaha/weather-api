from json.decoder import JSONDecodeError

from django.forms import ValidationError
from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework.test import RequestsClient
from rest_framework import status

from .models import Weather


chicago = {
    "date": "2019-06-11",
    "lat": 41.8818,
    "lon": -87.6231,
    "city": "Chicago",
    "state": "Illinois",
    "temperatures": [24.0, 21.5, 24.0, 19.5, 25.5, 25.5, 24.0, 25.0, 23.0, 22.0, 18.0, 18.0, 23.5, 23.0, 23.0, 25.5, 21.0, 20.5, 20.0, 18.5, 20.5, 21.0, 25.0, 20.5]
}

oakland = {
    "date": "2019-06-12",
    "lat": 37.8043,
    "lon": -122.2711,
    "city": "Oakland",
    "state": "California",
    "temperatures": [24.0, 36.0, 28.5, 29.0, 32.0, 36.0, 28.5, 34.5, 30.5, 31.5, 29.5, 27.0, 30.5, 23.5, 29.0, 22.0, 28.5, 32.5, 24.5, 28.5, 22.5, 35.0, 26.5, 32.5],
}

london = {
    "date": "2019-03-12",
    "lat": 51.5098,
    "lon": -0.1180,
    "city": "London",
    "state": "N/A",
    "temperatures": [11.0, 11.0, 5.5, 7.0, 5.0, 5.5, 6.0, 9.5, 11.5, 5.0, 6.0, 8.0, 9.5, 5.0, 9.0, 9.5, 12.0, 6.0, 9.5, 8.5, 8.0, 8.0, 9.0, 6.5],
}

moscow1 = {
    "date": "2019-03-12",
    "lat": 55.7512,
    "lon": 37.6184,
    "city": "Moscow",
    "state": "N/A",
    "temperatures": [-2.0, -4.5, 1.0, -6.0, 1.0, 1.5, -9.0, -2.5, -3.0, -0.5, -13.5, -9.0, -11.5, -5.5, -5.5, -3.5, -14.0, -9.5, 1.5, -15.0, -6.5, -7.0, -13.5, -14.5],
}

moscow2 = {
    "date": "2018-03-12",
    "lat": 55.7512,
    "lon": 37.6184,
    "city": "Moscow",
    "state": "N/A",
    "temperatures": [-13.5, -15.5, -9.5, -19.5, -9.0, -18.0, -12.5, -18.5, -20.0, -7.0, -19.5, -17.0, -15.5, -12.0, -20.0, -14.0, -18.5, -20.0, -7.5, -14.5, -14.0, -11.0, -13.5, -11.0],
}

HOST = 'http://localhost:8000'

class WeatherModelTestCase(TestCase):
    def setUp(self):
        self.obj = Weather(**chicago)
        self.obj.save()
    
    def test_create(self):
        self.assertTrue(Weather.objects.exists())
    
    def test_missing_attributes(self):
        weather = Weather()
        with self.assertRaises(ValidationError):
            weather.full_clean()


class WeatherEndpointWithPOSTTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'

    def test_with_valid_data(self):
        r = self.client.post(self.url, data=chicago)
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        data = r.json()
        self.assertIn('id', data)
        self.assertIsInstance(data['id'], int)
        del data['id']
        self.assertDictEqual(data, chicago)
        
    def test_with_invalid_data(self):
        # implement the rest of the test
        invalid_payload = {
          "date": "2018-13-12",
          "lat": 55.75128,
          "lon": 137.61848,
          "city": "",
          "state": "",
          "temperatures": [10.5],
        }
        fields_with_error = [
            ['date', 'Date has wrong format. Use one of these formats instead: YYYY-MM-DD.'],
            ['temperatures', 'Define hourly temperatures.'],
            ['lat', 'Ensure that there are no more than 6 digits in total.'],
            ['lon', 'Ensure that there are no more than 7 digits in total.'],
            ['city', 'This field may not be blank.'],
            ['state', 'This field may not be blank.'],
        ]
        r = self.client.post(self.url, data=invalid_payload)
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        data = r.json()

        for field in fields_with_error:
            with self.subTest():
                self.assertIn(field[1], data.get(field[0]))
        # raise NotImplementedError()


class WeatherEndpointWithGETSingleTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'
        try:
            self.chicago = self.client.post(self.url, data=chicago).json()
        except JSONDecodeError:
            self.fail("/weather endpoint for POST request not implemented")

    def test_with_existing_record(self):
        # implement the rest of the test
        url = HOST + resolve_url('weather-detail', pk=1)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertEqual(data, self.chicago)
        # raise NotImplementedError()

    def test_with_non_existing_record(self):
        # implement the rest of the test
        url = HOST + resolve_url('weather-detail', pk=0)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        data = r.json()
        self.assertEqual(data, {'detail': 'Not found.'})
        # raise NotImplementedError()


class WeatherEndpointWithGETListTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'
        try:
            self.objects = [self.client.post(self.url, data=city).json()
                            for city in [chicago, oakland, london, moscow1]]
        except JSONDecodeError:
            self.fail("/weather endpoint for POST request not implemented")

    def test_list_matches(self):
        expected_objects = sorted(self.objects, key=lambda obj: obj['id'])

        r = self.client.get(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)


class WeatherEndpointWithGETListAndDateFilterTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'
        try:
            self.objects = [self.client.post(self.url, data=city).json()
                            for city in [chicago, oakland, london, moscow1]]
        except JSONDecodeError:
            self.fail("/weather endpoint for POST request not implemented")

    def test_list_matches(self):
        date = "2019-03-12"

        expected_objects = [self.objects[2], self.objects[3]]

        url = self.url + ('?date=%s' % date)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)

    def test_with_no_results(self):
        date = "2015-06-06"
        expected_objects = []
        # implement the rest of the test
        url = self.url + ('?date=%s' % date)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)
        # raise NotImplementedError()


class WeatherEndpointWithGETListAndCityFilterTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'
        try:
            self.objects = [self.client.post(self.url, data=city).json()
                            for city in [chicago, oakland, london, moscow1, moscow2]]
        except JSONDecodeError:
            self.fail("/weather endpoint for POST request not implemented")

    def test_list_matches(self):
        city = 'moscow'

        expected_objects = [self.objects[3], self.objects[4]]

        url = self.url + ('?city=%s' % city)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)

    def test_with_more_than_one_city(self):
        cities = ['moscow', 'London', 'ChicaGo']
        expected_objects = [self.objects[0], self.objects[2], self.objects[3], self.objects[4]]
        # implement the rest of the test
        cities = ','.join(cities)
        url = self.url + ('?city=%s' % cities)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)
        # raise NotImplementedError()

    def test_with_no_results(self):
        cities = "berlin,amsterdam"
        expected_objects = []
        # implement the rest of the test
        url = self.url + ('?city=%s' % cities)
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)
        # raise NotImplementedError()


class WeatherEndpointWithGETListAndDateOrderTestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'
        try:
            self.objects = [self.client.post(self.url, data=city).json()
                            for city in [chicago, oakland, london, moscow1, moscow2]]
        except JSONDecodeError:
            self.fail("/weather endpoint for POST request not implemented")

    def test_asc_order_list_matches(self):
        expected_objects = sorted(self.objects, key=lambda obj: (obj['date'], obj['id']))

        url = self.url + '?sort=date'
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)

    def test_desc_order_list_matches(self):
        expected_objects = sorted(self.objects, key=lambda obj: (obj['date'], -obj['id']), reverse=True)

        url = self.url + '?sort=-date'
        r = self.client.get(url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(data, expected_objects)


class WeatherEndpointWithDELETETestCase(TestCase):
    def setUp(self):
        self.client = RequestsClient()
        self.url = HOST + '/weather/'
        try:
            self.objects = [self.client.post(self.url, data=city).json()
                            for city in [chicago, oakland, london, moscow1, moscow2]]
        except JSONDecodeError:
            self.fail("/weather endpoint for POST request not implemented")
    
    def test_delete_weather(self):
        url = HOST + resolve_url('weather-detail', pk=1)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        r = self.client.get(self.url)
        data = r.json()
        self.assertEqual(len(data), 4)
