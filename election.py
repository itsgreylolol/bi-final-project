import pandas as pd
import numpy as np

def Clean(df):
    df['fips'] = pd.to_numeric(df['fips'], errors='coerce')
    df.dropna(subset=['lead', 'fips'], inplace=True)
    df['fips'] = df['fips'].astype('int64')
    df['color'] = 0
    return EncodeNewColumns(df)
    
def EncodeNewColumns(df):
    # Since Trump won, red will be 1 and blue will be 0
    df['color'] = df['lead'].apply(lambda x: 1 if 'Trump' in x else 0)
    return df.groupby(['fips', 'color']).size().reset_index()[['fips', 'color']]

# blue is still 0, red is still 1, and mixed flights will be 2.
# mixed is a flight with different color origin and destinations
def ColorFlights(carrierFrame, electionFrame):
    carrierFrame.reset_index(inplace=True, drop=True)
    originMerge = carrierFrame.merge(electionFrame, how='left', left_on='ORIGIN_FIPS', right_on='fips')
    carrierFrame['origin_color'] = originMerge['color'][originMerge['fips'] == carrierFrame['ORIGIN_FIPS']]
    destMerge = carrierFrame.merge(electionFrame, how='left', left_on='DEST_FIPS', right_on='fips')
    carrierFrame['dest_color'] = destMerge['color'][destMerge['fips'] == carrierFrame['DEST_FIPS']]
    carrierFrame['flight_color'] = 2
    carrierFrame['flight_color'][carrierFrame['dest_color'] == carrierFrame['origin_color']] = carrierFrame['dest_color']
    carrierFrame.dropna(inplace=True)
    carrierFrame.drop(columns=['origin_color', 'dest_color'], inplace=True)
    return carrierFrame
    
    