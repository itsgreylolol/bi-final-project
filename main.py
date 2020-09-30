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

carrierFile = "US_CARRIER_SET.csv"
countyFile = "pres16results.csv"
covidFile = "us_counties_covid19_daily.csv"

def main():
    mergedStonks = stonks.ReadAndMerge(inpath, stockFiles)
    electionFrame = drumpf.Clean(pd.read_csv(inpath + countyFile))
    covidFrame = pd.read_csv(inpath + covidFile, parse_dates=[0])
    carrierFrame = planes.Clean(pd.read_csv(inpath + carrierFile))
    firstMerge = plague.CleanAndMerge(covidFrame, electionFrame)
    secondMerge = firstMerge.merge(mergedStonks, left_on='date', right_on='Date')
    secondMerge.drop(columns=['Date'], inplace=True)
    secondMerge.to_csv(outpath +  "SecondTry.csv", index=False)
  
main()