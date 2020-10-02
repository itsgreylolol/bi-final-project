import pandas as pd 
import numpy as np

def Clean(df):
    df.drop(columns=['YEAR', 
                     'QUARTER', 
                     'MAIL', 
                     'ORIGIN', 
                     'ORIGIN_STATE_ABR', 
                     'ORIGIN_STATE_FIPS', 
                     'DEST', 
                     'DEST_STATE_ABR', 
                     'DEST_STATE_FIPS'], 
            inplace=True)
    carriersToKeep = ["American Airlines Inc.",
                      "Delta Air Lines Inc.",
                      "Southwest Airlines Co.",
                      "United Air Lines Inc."
        ]
    df = df[df['CARRIER_NAME'].isin(carriersToKeep)]
    grouped = df.groupby(['CARRIER_NAME', 'MONTH'])
    newDfList = []
    for key, item in grouped:
        newDfList.append(grouped.get_group(key))
    newDf = pd.concat(newDfList)
    newDf.dropna(inplace=True)
    newDf['DEST_FIPS'] = newDf['DEST_FIPS'].astype('int64')
    newDf['ORIGIN_FIPS'] = newDf['ORIGIN_FIPS'].astype('int64')
    return Upsample(newDf)
    
def Upsample(df):
    #Get the flight counts for each month
    #Can use any arbitrary column, I used passengers
    flights_by_month = df.groupby(['CARRIER_NAME', 'MONTH'])

    #List of days for every month in the dataset
    days_of_month = [31,29,31,30,31,30]
    newerDfList = []
    for key, item in flights_by_month:
        newerDf = pd.DataFrame({ 'date': pd.date_range('2020-' + str(item['MONTH'].iloc[0]) + '-1', periods=days_of_month[item['MONTH'].iloc[0] - 1]),
                                 'avgPassengers': np.nan})
        newerDf['avgPassengers'].iloc[0] = item['PASSENGERS'].sum() / days_of_month[item['MONTH'].iloc[0] - 1]
        newerDf['carrier'] = item['CARRIER_NAME'].iloc[0]
        newerDf.set_index(['date'], inplace=True)
        newerDf.index = pd.to_datetime(newerDf.index)
        newerDfList.append(newerDf)
    newestDf = pd.concat(newerDfList)
    
    #Upsample and interpolate
    upsampled = newestDf.avgPassengers.resample('D').mean()
    newestDf['avgPassengers'] = upsampled.interpolate(method='spline', order=2)
    return newestDf