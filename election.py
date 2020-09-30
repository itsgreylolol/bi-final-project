import pandas as pd

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
    
    