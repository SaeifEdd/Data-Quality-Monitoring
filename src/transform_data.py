import os
import duckdb
import pandas as pd


class DataTransformer:
    def __init__(self):
        pass

    def read_df(self) -> pd.DataFrame:
        data_dir = "data/raw"
        months_data_list = []
        for file in os.listdir(data_dir):
            csv_filename = os.path.join(data_dir, file)
            months_data_list.append(pd.read_csv(csv_filename))

        df = pd.concat(months_data_list)
        print(df)
        return df

    def add_daily_traffic(self, df):
        df["daily_store_sensor_traffic"] = df.groupby(["date", "store_id", "sensor_id"])[
            "nb_visitors"].transform("sum")

        return df

    def remove_unreliable_data(self, df):
        """ remove none sensor_id, unit different than visitors"""
        df = df.drop(df[(df['unit'] != "visitors") | (df["sensor_id"].isnull())].index)
        df = df.drop(df[(df['nb_visitors'] == 0) | (df['nb_visitors'] == -1)].index)
        return df

    def apply_rolling_avg(self, group):
        group = group.sort_values('date')
        group['last_4_day_avg'] = group['daily_store_sensor_traffic'].rolling(window=4, min_periods=1).mean()
        return group

    def add_same_day_average(self, df):
        """ add column of average of daily sensor traffic of
        last same 4 week days (same last 4 mondays for example)"""
        # add week day column
        df["date"] = pd.to_datetime(df["date"])
        df["week_day"] = [r.weekday() for r in df["date"]]
        # copy original data
        df_copy = df.copy()
        # drop duplicates rows:
        df_copy = df_copy.drop_duplicates(subset=["date", "store_id", "sensor_id"])
        # compute the same days average
        df_wind = df_copy.groupby(['week_day', 'store_id', 'sensor_id']).apply(self.apply_rolling_avg).reset_index(drop=True)
        # merge back the dataset:
        res_df = pd.merge(df, df_wind[['date', 'store_id', 'sensor_id', 'last_4_day_avg']],
                          on=['date', 'store_id', 'sensor_id'], how='left')
        return res_df

    def add_pct_change(self, df):
        """ add column: percentage of change between current row and last
        4 same days average, we can use a threshold later on to remove some rows"""
        df["pct_change"] = round(
            abs(df["daily_store_sensor_traffic"] - df["last_4_day_avg"]) / df["last_4_day_avg"] * 100,
            2)
        return df



if __name__ == "__main__":
    transform = DataTransformer()
    transform.read_df()