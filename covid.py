def CleanAndMerge(covidFrame, electionFrame):
    covidFrame['fips'][covidFrame['county'] == 'New York City'] = 36061
    covidFrame.dropna(subset=['fips'], inplace=True)
    mergedFrame = covidFrame.merge(electionFrame, on='fips')
    return EncodeNewColumns(mergedFrame)

def EncodeNewColumns(df):
    # https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States#Standard_Federal_Regions for region reference
    regions = [
            ["Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island", "Vermont"],
            ["New Jersey", "New York", "Puerto Rico", "US Virgin Islands"],
            ["Delaware", "District of Columbia", "Maryland", "Pennsylvania", "Virginia", "West Virginia"],
            ["Alabama", "Florida", "Georgia", "Kentucky", "Mississippi", "North Carolina", "South Carolina", "Tennessee"],
            ["Illinois", "Indiana", "Michigan", "Minnesota", "Ohio", "Wisconsin"],
            ["Arkansas", "Louisiana", "New Mexico", "Oklahoma", "Texas"],
            ["Iowa", "Kansas", "Missouri", "Nebraska"],
            ["Colorado", "Montana", "North Dakota", "South Dakota", "Utah", "Wyoming"],
            ["Arizona", "California", "Hawaii", "Nevada", "American Samoa", "Guam", "Northern Mariana Islands"],
            ["Alaska", "Idaho", "Oregon", "Washington"]
        ]
    df['region'] = 0
    for index, item in enumerate(regions):
        df['region'][df['state'].isin(item)] = index+1
    
    df.sort_values(['fips', 'date'], inplace=True)
    df['casedelta'] = df['cases'][df['cases'] >= df['cases'].shift()].sub(df['cases'].shift())
    df['casedelta'].fillna(df['cases'], inplace=True)
    df['casedelta'] = df['casedelta'].astype('int64')
    df['deathdelta'] = df['deaths'][df['deaths'] >= df['deaths'].shift()].sub(df['deaths'].shift())
    df['deathdelta'].fillna(df['deaths'], inplace=True)
    df['deathdelta'] = df['deathdelta'].astype('int64')
    return df
