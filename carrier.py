import pandas as pd 

def Clean(df):
    df.drop(columns=['CARRIER_NAME', 'YEAR', 'QUARTER', 'ORIGIN_STATE_NM'], inplace=True)
    carriersToKeep = ["American Airlines Inc.",
                      "Delta Air Lines Inc.",
                      "Southwest Airlines Co.",
                      "United Air Lines Inc."
        ]
    df = df[df['UNIQUE_CARRIER_NAME'].isin(carriersToKeep)]
    grouped = df.groupby(['UNIQUE_CARRIER_NAME', 'MONTH'])
    newDfList = []
    for key, item in grouped:
        newDfList.append(grouped.get_group(key))
    newDf = pd.concat(newDfList)