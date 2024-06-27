import sys
import numpy as np
from datetime import date, timedelta


class SensorVisitors:
    def __init__(
        self, avg_visits, std_visits, perc_mal: float = 0.085, perc_break: float = 0.05
    ) -> None:
        self.avg_visits = avg_visits
        self.std_visits = std_visits
        self.perc_mal = perc_mal
        self.perc_break = perc_break

    def simulate_visits(self, business_date: date, hour: int) -> int:
        """
        simulate the number of persons detected by a sensor on
        a specific date and hour
        """
        # to always get the same number of visitors in the same day
        np.random.seed(seed=business_date.toordinal())
        visits = np.random.normal(self.avg_visits, self.std_visits)

        day = business_date.weekday()
        # higher traffic on wednesday, fridays, saturdays
        # no traffic on sundays
        if day == 2:
            visits *= 1.10
        if day == 4:
            visits *= 1.25
        if day == 5:
            visits *= 1.35
        if day == 6:
            visits = -1

        # we suppose the traffic is the same in hours between 8 and 19
        # no traffic after 19 and before 8
        if (day != 6) and (8 <= hour <= 19):
            visits = visits / 11
        if (day != 6) and (hour < 8 or hour > 19):
            visits = 0

        return np.floor(visits)

    def get_exact_visits(self, business_date: date, hour: int) -> int:
        """
        return number of visitors considering break or mal functionality
        possibility
        """

        np.random.seed(seed=business_date.toordinal())
        functionality_proba = np.random.random()
        number_visits = self.simulate_visits(business_date, hour)

        if number_visits != -1:
            if functionality_proba < self.perc_break:
                return 0
            elif functionality_proba < self.perc_mal:
                number_visits *= functionality_proba
                return np.floor(number_visits)
            else:
                return number_visits

        return -1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
        if sys.argv[2]:
            hour = int(sys.argv[2])
    else:
        year, month, day, hour = 2023, 10, 25, 10
    queried_date = date(year, month, day)

    sensor = SensorVisitors(1500, 150)
    current_date = queried_date
    for day in range(1,100):
        print(current_date, "nb of visitors",sensor.get_exact_visits(current_date, hour))
        current_date= queried_date + timedelta(days = day)
