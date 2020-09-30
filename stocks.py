import pandas as pd

def ReadAndMerge(inpath, stockFiles):
    stockFrames = {}
    for fileName in stockFiles:
        initialFile = pd.read_csv(inpath + fileName, parse_dates=[0])
        stockFrames[fileName[0:3]] = initialFile
    return Merge(stockFrames)
    

def Clean(dfs):
    newDfs = []
    for key in dfs:
        df = dfs[key]
        df = df.loc[df["Date"] >= pd.Timestamp(2020, 1, 21), ]
        df[key + " Open"] = df["Open"]
        df[key + " High"] = df["High"]
        df[key + " Low"] = df["Low"]
        df[key + " Close"] = df["Close"]
        df[key + " Adj Close"] = df["Adj Close"]
        df[key + " Volume"] = df["Volume"]
        df.drop(columns=["Open", "High", "Low", "Close", "Adj Close", "Volume"], inplace=True)
        newDfs.append(df)
    return newDfs
        
def Merge(dfs):
    newerDfs = Clean(dfs)
    merge = newerDfs[0]
    for df in newerDfs[1:]:
        merge = merge.merge(df, on='Date')
    return merge
    