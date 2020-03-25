#!/usr/bin/env python

import tweets
import plotting

PATH_TO_TIME_SERIES = r'COVID-19/csse_covid_19_data/csse_covid_19_time_series'
FILE_NAME_TEMPLATE = lambda st: f'time_series_covid19_{st:s}_global'
DATA_TYPES = ['confirmed', 'deaths']
EXT = '.csv'

COUNTRIES = ['United Kingdom', 'Italy', 'Spain', 'Germany', 'France', 'US', 'China', 'Korea, South', 'Japan']


def get_doubling_times(dates, data, window=1, limit=100):
    """
    Get rolling doubling times
    """
    day_numbers = (dates.year-2020)*365 + dates.dayofyear
    
    doubling_times = []
    
    # rolling linear fit, window size w
    w = window
    for ii in range(w, (day_numbers.size)):
        start_pos = ii - w
        end_pos = ii + 1
        
        if np.mean(data[start_pos:end_pos]) < limit:
            doubling_times.append(np.nan)
        else:
            days_to_fit = day_numbers[start_pos:end_pos]
            n_to_fit = np.log(data[start_pos:end_pos])
            p = np.polyfit(days_to_fit, n_to_fit, 1)

            doubling_time = 1/p[0]*np.log(2)


            if doubling_time < 0:
                doubling_time = 0

            doubling_times.append(doubling_time)

    np_out = np.array(doubling_times)
    return np_out

def get_days_to_n_cases(doubling_time, cases_now, cases_proj):
    factor_to_go = cases_proj / cases_now    
    doubling_times_to_go = np.log(factor_to_go)/np.log(2)
    
    doubling_times_to_go[doubling_times_to_go<0] = 0
    
    days_to_go = doubling_times_to_go*doubling_time
    
    return days_to_go

def get_path(suffix):
    file_name = FILE_NAME_PREFIX + suffix + EXT
    p = os.path.join(PATH_TO_TIME_SERIES, file_name)
    return p

def get_data_frames():
    
    dfs = []

    for suffix in FILE_SUFFIXES:
        path = get_path(suffix)
        df = pd.read_csv(path)
        dfs.append(df)
    
    return dfs
    
    confirmed_cases = {}
    doubling_times = {}
    deaths_ = {}
    death_doubling_times = {}

def get_stats():
    window = 3
    n_cases_proj = np.logspace(3, np.log10(3e6), 45);
    n_deaths_proj = 0.01 * n_cases_proj

    MIN_CASES = 20  # don't calculate the confirmed doubling time if total n deaths less than this
    MIN_DEATHS = 5  # don't calculate the death doubling time if total n deaths less than this

    dates = pd.to_datetime(dfs[0].iloc[:, 4:].columns, format='%m/%d/%y')

    for c in countries:
        confirmed = dfs[0].loc[dfs[0]['Country/Region'] == c]
        deaths = dfs[1].loc[dfs[1]['Country/Region'] == c]

        n = confirmed.iloc[:,4:].sum()
        x = deaths.iloc[:, 4:].sum()

        confirmed_cases[c] = n
        deaths_[c] = x

        #ax1.plot_date(dates, n, '.', label=c)
        
        d = get_doubling_times(dates, n, window=window, limit=MIN_CASES)
        doubling_times[c] = d

        #ax2.plot_date(dates[window:], d, '-', label=c)
        
        days_to_n_cases = get_days_to_n_cases(d[-1], n[-1], n_cases_proj)

        #ax3.plot(n_cases_proj, days_to_n_cases, label=c)
        
        death_rate_pct = 100*x/n
        death_rate_pct[n<MIN_CASES] = np.nan
        #ax4.plot_date(dates, death_rate_pct, '-', label=c)
        
        #ax5.plot_date(dates, x, '-', label=c)
        
        dd = get_doubling_times(dates, x, window=window, limit=MIN_DEATHS)
        death_doubling_times[c] = dd
        #ax6.plot_date(dates[window:], dd, '-', label=c)
        
        d_days_to_n_cases = get_days_to_n_cases(dd[-1], x[-1], n_deaths_proj)
        #ax7.plot(n_deaths_proj, d_days_to_n_cases, label=c)

def main():
    print("Hello, world")

if __name__ == '__main__':
    main()
