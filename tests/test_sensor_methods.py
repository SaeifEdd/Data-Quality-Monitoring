import unittest
from datetime import date
from src.sensor import SensorVisitors


class tests_sensor_visits(unittest.TestCase):

    def test_sensor_malfunction(self):
        sensor = SensorVisitors(1500, 150)
        sensor_visitors = sensor.get_exact_visits(
            business_date=date(2024, 1, 18), hour=10
        )
        self.assertEqual(sensor_visitors, 7.0)

    def test_sensor_break(self):
        sensor = SensorVisitors(1500, 150)
        sensor_visitors = sensor.get_exact_visits(
            business_date=date(2023, 11, 13), hour=10
        )
        self.assertEqual(sensor_visitors, 0)

    def test_sensor_working_hours(self):
        sensor = SensorVisitors(1500, 150)
        sensor_visitors = sensor.get_exact_visits(
            business_date=date(2024, 3, 20), hour=20
        )
        self.assertEqual(sensor_visitors, 0)


if __name__ == "__main__":
    unittest.main()