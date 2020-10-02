import pandas as pd
import stocks as stonks
import election as drumpf
import covid as plague
import carrier as planes

inpath = "Datasets\\"
outpath = "Output\\"
stockFiles = ["AAL - Stock price.csv", 
              "DAL - Stock Price.csv", 
              "LUV - Stock Price.csv",
              "UAL - Stock Price.csv"]

carrierFile = "AirlineCityCountyFIPS.csv"
electionFile = "pres16results.csv"
covidFile = "us_counties_covid19_daily.csv"

def main():
    mergedStonks = stonks.ReadAndMerge(inpath, stockFiles)
    electionFrame = drumpf.Clean(pd.read_csv(inpath + electionFile))
    covidFrame = pd.read_csv(inpath + covidFile, parse_dates=[0])
    carrierFrame = planes.Clean(pd.read_csv(inpath + carrierFile))
    firstMerge = plague.CleanAndMerge(covidFrame, electionFrame)
    secondMerge = firstMerge.merge(mergedStonks, left_on='date', right_on='Date', how='left')
    secondMerge.drop(columns=['Date'], inplace=True)
    secondMerge.fillna(method='ffill', inplace=True)
    thirdMerge = secondMerge.merge(carrierFrame, on='date')
    deltaFrame = plague.EncodeNewColumns(thirdMerge)
    deltaFrame.sort_values(by=['date', 'fips'], inplace=True)
    deltaFrame.to_csv(outpath + "Final.csv", index=False)
  
main()