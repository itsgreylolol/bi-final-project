def CleanAndMerge(covidFrame, electionFrame):
    covidFrame['fips'][covidFrame['county'] == 'New York City'] = 36061
    covidFrame.dropna(subset=['fips'], inplace=True)
    return covidFrame.merge(electionFrame, on='fips')