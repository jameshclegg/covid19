#!/usr/bin/env python

import tweets
import plotting
import os
import pandas as pd
import numpy as np
import datetime

PATH_TO_TIME_SERIES = r'../COVID-19/csse_covid_19_data/csse_covid_19_time_series'
FILE_NAME_TEMPLATE = lambda st: f'time_series_covid19_{st:s}_global'
DATA_TYPES = ['confirmed', 'deaths']
EXT = '.csv'

COUNTRIES = ['United Kingdom', 'Brazil', 'Spain', 'Germany', 'India', 'US', 'Russia', 'South Africa', 'Mexico']

MIN_CASES = 20  # don't calculate the confirmed doubling time if total n deaths less than this

FIRST_DATA_COL = 4
DATE_FORMAT = '%m/%d/%y'


def get_data_frames():

    dfs = []

    def get_path(type_string):
        file_name = FILE_NAME_TEMPLATE(type_string) + EXT
        p = os.path.join(PATH_TO_TIME_SERIES, file_name)
        return p
    
    for suffix in DATA_TYPES:
        path = get_path(suffix)
        df = pd.read_csv(path)
        dfs.append(df)

    return dfs


def get_stats(data_frames):
    
    def extract_data(df):
        # extract only the data, ignore the latitude, longitude etc
        d = df.iloc[:, FIRST_DATA_COL:]
        return d
    
    all_confirmed_data = data_frames[0]
    all_deaths_data = data_frames[1]
    
    # initialise class to hold data
    data = Data()
    
    data.dates = pd.to_datetime(extract_data(all_confirmed_data).columns, format=DATE_FORMAT)
    
    first_date = datetime.datetime(year=2020, month=7, day=16)
    data.dates = data.dates[data.dates > first_date]
    whole_world_confirmed = extract_data(all_confirmed_data).sum()
    whole_world_deaths = extract_data(all_deaths_data).sum()
    
    def get_stats_by_country(data_frame, country_region):
        """
        Fiddle around with the weird province/state information and get out the deaths by country
        """
        selected_by_country = data_frame.loc[data_frame['Country/Region'] == country_region]
     
        # find the data where the Province/State is NaN.  In many cases this seems to 
        # indicate the "main" country and not another territory
        no_province = selected_by_country.loc[pd.isna(selected_by_country['Province/State'])]
        
        # if there is just one NaN, then this is probably the data we want
        if no_province.shape[0] == 1:
            # the final [0,:] just returns a series instead of a frame
            data_vs_time = extract_data(no_province).iloc[0, :]
        else:
            # otherwise data has been reported by state, e.g. in the case of China.  Just sum up.
            data_vs_time = extract_data(selected_by_country).sum()

        return data_vs_time

    date_name = f"{first_date.month}/{first_date.day}/{first_date.strftime('%y')}"

    for c in COUNTRIES:
        here_confirmed = get_stats_by_country(all_confirmed_data, c)
        here_deaths = get_stats_by_country(all_deaths_data, c)

        here_confirmed -= here_confirmed[date_name]
        here_confirmed = here_confirmed[-len(data.dates):]

        here_deaths -= here_deaths[date_name]
        here_deaths = here_deaths[-len(data.dates):]

        data.confirmed_cases[c] = here_confirmed
        data.deaths[c] = here_deaths
    
    whole_world_confirmed = whole_world_confirmed[-len(data.dates):]
    whole_world_deaths = whole_world_deaths[-len(data.dates):]

    rest_of_world_confirmed = whole_world_confirmed - pd.DataFrame(data.confirmed_cases).transpose().sum()
    rest_of_world_deaths = whole_world_deaths - pd.DataFrame(data.deaths).transpose().sum()
    
    rest_of_world_confirmed -= rest_of_world_confirmed[0]
    rest_of_world_deaths -= rest_of_world_deaths[0]

    data.confirmed_cases['Rest of world'] = rest_of_world_confirmed
    data.deaths['Rest of world'] = rest_of_world_deaths
    
    return data


class Data():
    # number of data points to look backwards over when calculating 
    # exponential growth rate
    window = 3
    doubling_limit = 5  # don't calculate the doubling time if total n less than this

    def __init__(self):
        self.confirmed_cases = {}
        self.deaths = {}
        self.dates = None
    
    def get_doubling_times(self, data, limit):
        day_numbers = (self.dates.year-2020)*365 + self.dates.dayofyear
        
        doubling_times = []
        
        # rolling linear fit, window size w
        w = Data.window
        for ii in range(w, day_numbers.size):
            start_pos = ii - w
            end_pos = ii + 1
            
            if np.mean(data[start_pos:end_pos]) < limit:
                doubling_times.append(np.nan)
            else:
                days_to_fit = day_numbers[start_pos:end_pos]
                n_to_fit = np.log(data[start_pos:end_pos])
                p = np.polyfit(days_to_fit, n_to_fit, 1)
                
                if p[0] > 0:
                    doubling_time = 1/p[0]*np.log(2)
                else:
                    doubling_time = 0

                doubling_times.append(doubling_time)

        np_doubling_times = np.array(doubling_times)
        return np_doubling_times

    def get_death_rate(self, country_name):
        death_rate = self.deaths[country_name]/self.confirmed_cases[country_name]
        death_rate[self.confirmed_cases[country_name]<MIN_CASES] = np.nan
        return death_rate
   

def main():
    # read in data from csv files. This returns a list of data frames.  
    # the list has one entry for each element in DATA_TYPES
    data_frames = get_data_frames()

    # extract the data
    data = get_stats(data_frames)

    # do plots
    folder_name = plotting.plot(data)

    # tweet
    tweets.initialise_and_tweet(folder_name)


if __name__ == '__main__':
    main()
