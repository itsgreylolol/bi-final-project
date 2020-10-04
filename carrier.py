import pandas as pd 
import numpy as np

def Clean(df):
    grouped = df.groupby(['CARRIER_NAME', 'MONTH'])
    newDfList = []
    for key, item in grouped:
        newDfList.append(grouped.get_group(key))
    newDf = pd.concat(newDfList)
    newDf.dropna(inplace=True)
    newDf['DEST_FIPS'] = newDf['DEST_FIPS'].astype('int64')
    newDf['ORIGIN_FIPS'] = newDf['ORIGIN_FIPS'].astype('int64')
    return newDf
    
def Upsample(df):
    carriersToKeep = ["American Airlines Inc.",
                      "Delta Air Lines Inc.",
                      "Southwest Airlines Co.",
                      "United Air Lines Inc."
        ]
    flightsByCarrier = df[df['CARRIER_NAME'].isin(carriersToKeep)]
    flightsByCarrier = flightsByCarrier[['PASSENGERS', 'MONTH', 'CARRIER_NAME']].groupby('CARRIER_NAME')
    final = pd.DataFrame()
    ranges = pd.to_datetime(['1/1/2020','2/1/2020', '3/1/2020', '4/1/2020', '5/1/2020', '6/1/2020', '6/30/2020'])
    for key, item in flightsByCarrier:
        passFieldName = str(item['CARRIER_NAME'].iloc[0] + '_avg_passengers')
        newDf = pd.DataFrame({ 'date': ranges })
        newDf.set_index(ranges, inplace=True)
        newDf[passFieldName] = np.nan
        passGroup = item.groupby(['MONTH'])
        for innerKey, innerItem in passGroup:
            newDf[passFieldName][innerKey-1 % 7] = innerItem['PASSENGERS'].mean()
        upsampled = newDf[passFieldName].resample('D').mean()
        final[passFieldName] = upsampled.interpolate(method='spline', order=2)
    flightsByColor = df[['PASSENGERS', 'MONTH', 'CARRIER_NAME', 'flight_color']].groupby('flight_color')
    for key, item in flightsByColor:
        color = 'blue'
        if item['flight_color'].mean() == 1:
            color = 'red'
        elif item['flight_color'].mean() == 2:
            color = 'mixed'
        colorFieldName = 'avg_passengers_' + color + '_flights' 
        newDf = pd.DataFrame({ 'date': ranges })
        newDf.set_index(ranges, inplace=True)
        newDf[colorFieldName] = np.nan
        colorGroup = item.groupby(['MONTH'])
        for innerKey, innerItem in colorGroup:
            newDf[colorFieldName][innerKey-1 % 7] = innerItem['PASSENGERS'].mean()
        upsampled = newDf[colorFieldName].resample('D').mean()
        final[colorFieldName] = upsampled.interpolate(method='spline', order=2)
    final['date'] = final.index
    return final