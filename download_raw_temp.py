import requests
import urllib
import pandas as pd

if __name__ == '__main__':
    #######################################
    # To Load Raw Data from NOAA
    # Takes a while...
    #######################################

    url = 'https://www.ncei.noaa.gov/access/services/data/v1'
    st = pd.read_csv('noaa_stations2.csv')

    st_list = st.STATION.to_list()

    tt = pd.DataFrame()
    for s in st_list:

        params = urllib.parse.urlencode(dict(
            dataset='daily-summaries',
            stations=s,
            startDate='2015-01-01',
            endDate='2021-04-15',
            format='json',
            includeStationName='false',
            units='metric',
            includeStationLocation='false'
        ))

        r = requests.get(url, params=params)

        tt = tt.append(pd.DataFrame(r.json()))

    tt.to_pickle('tx_temp_raw.pkl')

    ######################################
    # Transform Raw Temp Date to daily Mean
    ######################################

    tt = tt[['DATE','STATION','TMAX','TMIN']].dropna()

    tt.DATE = pd.to_datetime(tt.DATE)

    tt.TMAX = pd.to_numeric(tt.TMAX)
    tt.TMIN = pd.to_numeric(tt.TMIN)

    tt = tt.merge(st, on='STATION')

    tt['TEMP'] = (tt.TMAX + tt.TMIN)/2

    tt.to_pickle('tx_temp.pkl')
