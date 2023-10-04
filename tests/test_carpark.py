import unittest

import smartpark
from smartpark.carpark import CarPark


class TestCarPark(unittest.TestCase):
    def test_no_negative_spaces(self):
        car_park = CarPark({"broker": "localhost",
                            "port": 1883,
                            "topic-root": "lot",
                            "name": "raf-park",
                            "location": "L306",
                            "topic-qualifier": "car-park",
                            "total-spaces": 0,
                            "total-cars": 5
                            })

        car_park.on_car_entry()
        car_park.on_car_entry()
        self.assertEqual(car_park.available_spaces, 0)

        car_park.on_car_exit()
        car_park.on_car_exit()
        self.assertEqual(car_park.available_spaces, 1)
