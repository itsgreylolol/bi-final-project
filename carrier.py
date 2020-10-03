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
    return newDf
    
def Upsample(df):
    flights_by_month = df[['PASSENGERS', 'MONTH', 'CARRIER_NAME', 'flight_color']].groupby('CARRIER_NAME')
    final = pd.DataFrame()
    for key, item in flights_by_month:
        passFieldName = str(item['CARRIER_NAME'].iloc[0] + '_avg_passengers')
        ranges = pd.to_datetime(['1/1/2020','2/1/2020', '3/1/2020', '4/1/2020', '5/1/2020', '6/1/2020', '6/30/2020'])
        newDf = pd.DataFrame({ 'date': ranges })
        newDf.set_index(ranges, inplace=True)
        newDf[passFieldName] = np.nan
        passGroup = item.groupby(['MONTH'])
        for innerKey, innerItem in passGroup:
            newDf[passFieldName][innerKey-1 % 7] = innerItem['PASSENGERS'].mean()
            innerGroup = innerItem.groupby(['flight_color'])
            for innestKey, innestItem in innerGroup:
                print(innerGroup.count())
                colorFieldName = passFieldName + str(innestItem['flight_color'].iloc[0])
                newDf[colorFieldName] = np.nan
                newDf[colorFieldName][innerKey-1 % 7] = innestItem['PASSENGERS'].mean()
        upsampled = newDf[passFieldName].resample('D').mean()
        final[passFieldName] = upsampled.interpolate(method='spline', order=2)
    final['date'] = final.index
    print(final.count())
    return final