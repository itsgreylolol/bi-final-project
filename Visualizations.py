import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def Visualize(df, outpath):
#Shorten the column names for the correlation matrix
    corrdf = df.rename(columns = {'AAL Adj Close':'AAL_Adj_Cls','DAL Adj Close':'DAL_Adj_Cls',
                    'UAL Adj Close':'UAL_Adj_Cls','LUV Adj Close':'LUV_Adj_Cls',
                    'American Airlines Inc._avg_passengers':'AAL_Avg_Psgers',
                    'Delta Air Lines Inc._avg_passengers':'DAL_Avg_Psgers',
                    'United Air Lines Inc._avg_passengers':'UAL_Avg_Psgers',
                    'Southwest Airlines Co._avg_passengers':'LUV_Avg_Psgers',
                    'avg_passengers_blue_flights':'Blue_Avg_Psgers',
                    'avg_passengers_red_flights':'Red_Avg_Psgers',
                    'avg_passengers_mixed_flights':'Mxd_Avg_Psgers'})

    #Correlation matrix
    #Round to 2 decimal digits
    corrs = corrdf.corr().round(2)
    #There are -0 values from the rounding, set these to 0
    corrs[corrs==-0.00] = 0
    #Create correlation heatmap from the pandas df
    corrs.style.background_gradient(cmap='coolwarm')
    sns.heatmap(corrs, annot=True, annot_kws={"fontsize":5.5})
    plt.tight_layout()
    plt.tick_params(axis='both', which='major', labelsize=7)
    plt.tick_params(axis='both', which='minor', labelsize=6)
    #Save and show the plot
    plt.savefig(outpath + "correlationMatrix", dpi = 300)
    plt.show()

    new = df[['date','casedelta']].groupby('date').transform(np.sum)
    df['cases_by_day'] = new
    
    #Airline stocks over time
    df_airline_plt = df[['date', 'UAL Adj Close', 'AAL Adj Close', 'DAL Adj Close', 'LUV Adj Close']].groupby('date').mean()
    plt.plot(df_airline_plt.index, df_airline_plt['UAL Adj Close'], label = 'UAL Closing Price')
    plt.plot(df_airline_plt.index, df_airline_plt['DAL Adj Close'], label = 'DAL Closing Price')
    plt.plot(df_airline_plt.index, df_airline_plt['AAL Adj Close'], label = 'AAL Closing Price')
    plt.plot(df_airline_plt.index, df_airline_plt['LUV Adj Close'], label = ' Closing Price')
    plt.xticks(df_airline_plt.index[::10], rotation = 'vertical')
    plt.title('Big Four Airline Stock Prices Over Time')
    plt.xlabel('Dates')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()

    #COVID cases by political party box plot
    #Find the total cases by finding cumulative cases for each county on the most recent day
    total_dfs = df.loc[df['date'] == '2020-09-11']
    box = plt.boxplot([np.log10(total_dfs[total_dfs['color']==0]['cases']), 
                       np.log10(total_dfs[total_dfs['color']==1]['cases'])],
                       patch_artist=True, medianprops = dict(color="black",linewidth=1.5))
    plt.xticks([1,2],['Blue Counties','Red Counties'])
    plt.xlabel('Political Stance')
    plt.ylabel('Log Base 10 Transformed COVID Cases By County')
    plt.title('Total COVID Cases By County And Political Stance')
    colors = ['blue','red']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

    #COVID cases by political party time plot
    case_by_date = df[['date', 'cases', 'color']].groupby(['date','color']).sum()
    case_red = case_by_date.xs((1), level=('color'))
    case_blue = case_by_date.xs((0), level=('color'))
    plt.plot(case_blue.index, case_blue['cases'], label = 'Cumulative Blue County Covid Cases', color = 'blue')
    plt.plot(case_red.index, case_red['cases'], label = 'Cumulative Red County Covid Cases', color = 'red')
    plt.xticks(case_red.index[::10], rotation = 'vertical')
    plt.xlabel('Dates')
    plt.ylabel('Cumulative COVID Cases')
    plt.title('County COVID Cases Grouped By Political Stance')
    plt.legend()
    plt.show()


    #Group by region and date for the region plots
    case_by_date = df[['date', 'cases', 'region']].groupby(['date','region']).sum()
    case_one = case_by_date.xs((1), level=('region'))
    case_two = case_by_date.xs((2), level=('region'))
    case_three = case_by_date.xs((3), level=('region'))
    case_four = case_by_date.xs((4), level=('region'))
    case_five = case_by_date.xs((5), level=('region'))
    case_six = case_by_date.xs((6), level=('region'))
    case_seven = case_by_date.xs((7), level=('region'))
    case_eight = case_by_date.xs((8), level=('region'))
    case_nine = case_by_date.xs((9), level=('region'))
    case_ten = case_by_date.xs((10), level=('region'))
    
    #Lower COVID magnitude regions timeplots
    plt.plot(case_ten, label = 'Region 10', color = 'red')
    plt.plot(case_eight, label = 'Region 8', color = 'purple')
    plt.plot(case_seven, label = 'Region 7', color = 'green')
    plt.plot(case_three, label = 'Region 3', color = 'tan')
    plt.plot(case_one, label = 'Region 1', color = 'blue')
    plt.xticks(case_one.index[::10], rotation = 'vertical')
    plt.legend()
    plt.title('COVID Cases By Region (Lower Magnitude)')
    plt.xlabel('Dates')
    plt.ylabel('COVID Count')
    plt.show()

    #Higher COVID magnitude regions timeplots
    plt.plot(case_five, label = 'Region 5', color = 'maroon')
    plt.plot(case_nine, label = 'Region 9', color = 'gold')
    plt.plot(case_six, label = 'Region 6', color = 'cyan')
    plt.plot(case_four, label = 'Region 4', color = 'slategrey')
    plt.plot(case_two, label = 'Region 2', color = 'lime')
    plt.xticks(case_one.index[::10], rotation = 'vertical')
    plt.legend()
    plt.title('COVID Cases By Region (Higher Magnitude)')
    plt.xlabel('Dates')
    plt.ylabel('COVID Count')
    plt.show()

    #Lower Magnitude Region Boxplots
    total_dfs = df.loc[df['date'] == '2020-09-11']
    box = plt.boxplot([np.log(total_dfs[total_dfs['region']==10]['cases']),
                       np.log(total_dfs[total_dfs['region']==8]['cases']),
                       np.log(total_dfs[total_dfs['region']==7]['cases']),
                       np.log(total_dfs[total_dfs['region']==3]['cases']),
                       np.log(total_dfs[total_dfs['region']==1]['cases'])], 
                      patch_artist=True, medianprops = dict(color="black",linewidth=1.5))
    plt.xticks([1,2,3,4,5],['Region 10', 'Region 8', 'Region 7',  'Region 3' ,'Region 1'])
    plt.xlabel('Political Stance')
    plt.ylabel('Log Transformed COVID Cases For Each County')
    plt.title('Total COVID Cases By County And Region (Lower Magnitude)')
    colors = ['red', 'purple', 'green', 'tan', 'blue']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

    #Higher Magnitude Region Boxplots
    box = plt.boxplot([np.log(total_dfs[total_dfs['region']==5]['cases']),
                       np.log(total_dfs[total_dfs['region']==9]['cases']),
                       np.log(total_dfs[total_dfs['region']==6]['cases']),
                       np.log(total_dfs[total_dfs['region']==4]['cases']),
                       np.log(total_dfs[total_dfs['region']==2]['cases'])],
                      patch_artist=True, medianprops = dict(color="black",linewidth=1.5))
    plt.xticks([1,2,3,4,5],['Region 5', 'Region 9', 'Region 6', 'Region 4' , 'Region 2'])
    plt.xlabel('Political Stance')
    plt.ylabel('Log Transformed COVID Cases For Each County')
    plt.title('Total COVID Cases By County And Region (Higher Magnitude)')
    colors = ['gold', 'cyan', 'crimson', 'slategrey', 'lime']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()

    #Airlines and COVID plots
    cases = df[['date', 'casedelta']].groupby(['date',]).sum()
    #UAL linear
    df_airline_plt['cases'] = cases.replace(0,1)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Stock Price', color='green')
    ax1.tick_params(axis='y', labelcolor='green')
    ax1.plot(df_airline_plt.index, df_airline_plt['UAL Adj Close'], label = 'UAL ADJ Closing Price', color = 'green')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, df_airline_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('UAL Adj. Closing VS COVID Cases Over Time (Linear Scale)')
    plt.show()

    #AAL linear
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Stock Price', color='brown')
    ax1.tick_params(axis='y', labelcolor='brown')
    ax1.plot(df_airline_plt.index, df_airline_plt['AAL Adj Close'], label = 'AAL ADJ Closing Price', color = 'brown')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, df_airline_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('AAL Adj. Closing VS COVID Cases Over Time (Linear Scale)')
    plt.show()

    #DAL linear
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Stock Price', color='m')
    ax1.tick_params(axis='y', labelcolor='m')
    ax1.plot(df_airline_plt.index, df_airline_plt['DAL Adj Close'], label = 'DAL ADJ Closing Price', color = 'm')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, df_airline_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('DAL Adj. Closing VS COVID Cases Over Time (Linear Scale)')
    plt.show()

    #LUV linear
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Stock Price', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1.plot(df_airline_plt.index, df_airline_plt['LUV Adj Close'], label = 'LUV ADJ Closing Price', color = 'r')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, df_airline_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('LUV Adj. Closing VS COVID Cases Over Time (Linear Scale)')
    plt.show()

    #UAL Log
    df_airline_plt['cases'] = cases.replace(0,1)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Log Stock Price', color='green')
    ax1.tick_params(axis='y', labelcolor='green')
    ax1.plot(df_airline_plt.index, np.log10(df_airline_plt['UAL Adj Close']), label = 'UAL ADJ Closing Price', color = 'green')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Log Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, np.log10(df_airline_plt['cases']), label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('UAL Adj. Closing VS COVID Cases Over Time (Log Base 10 Scale)')
    plt.show()

    #AAL Log
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Log Stock Price', color='brown')
    ax1.tick_params(axis='y', labelcolor='brown')
    ax1.plot(df_airline_plt.index, np.log10(df_airline_plt['AAL Adj Close']), label = 'AAL ADJ Closing Price', color = 'brown')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Log Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, np.log10(df_airline_plt['cases']), label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('AAL Adj. Closing VS COVID Cases Over Time (Log Base 10 Scale)')
    plt.show()

    #DAL Log
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Log Stock Price', color='m')
    ax1.tick_params(axis='y', labelcolor='m')
    ax1.plot(df_airline_plt.index, np.log10(df_airline_plt['DAL Adj Close']), label = 'DAL ADJ Closing Price', color = 'm')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Log Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, np.log10(df_airline_plt['cases']), label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('DAL Adj. Closing VS COVID Cases Over Time (Log Base 10 Scale)')
    plt.show()

    #LUV Log
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Log Stock Price', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1.plot(df_airline_plt.index, np.log10(df_airline_plt['LUV Adj Close']), label = 'LUV ADJ Closing Price', color = 'r')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Log Daily Cases', color='blue')
    ax2.plot(df_airline_plt.index, np.log10(df_airline_plt['cases']), label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_airline_plt.index[::50])
    plt.title('LUV Adj. Closing VS COVID Cases Over Time (Log Base 10 Scale)')
    plt.show()

    #Passengers over time
    df_passenger_plt = df[['date', 'United Air Lines Inc._avg_passengers', 'American Airlines Inc._avg_passengers', 'Delta Air Lines Inc._avg_passengers','Southwest Airlines Co._avg_passengers']].groupby('date').mean()
    df_passenger_plt.drop(df_passenger_plt.index[162:], inplace = True)
    plt.plot(df_passenger_plt.index, df_passenger_plt['United Air Lines Inc._avg_passengers'], label = 'United Airlines')
    plt.plot(df_passenger_plt.index, df_passenger_plt['American Airlines Inc._avg_passengers'], label = 'American Airlines')
    plt.plot(df_passenger_plt.index, df_passenger_plt['Delta Air Lines Inc._avg_passengers'], label = 'Delta Airlines')
    plt.plot(df_passenger_plt.index, df_passenger_plt['Southwest Airlines Co._avg_passengers'], label = 'Southwest Airlines')
    plt.xticks(df_passenger_plt.index[::10], rotation = 'vertical')
    plt.title('Big Four Airline Average Passenger Count Over Time')
    plt.xlabel('Dates')
    plt.ylabel('Average Passengers')
    plt.legend()
    plt.show()

    #Passengers and COVID
    cases = df[['date', 'casedelta']].groupby(['date',]).sum()
    #UAL linear
    df_passenger_plt['cases'] = cases.replace(0,1)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('United Avg. Passengers', color='goldenrod')
    ax1.tick_params(axis='y', labelcolor='goldenrod')
    ax1.plot(df_passenger_plt.index, df_passenger_plt['United Air Lines Inc._avg_passengers'], label = 'UAL ADJ Closing Price', color = 'goldenrod')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_passenger_plt.index, df_passenger_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_passenger_plt.index[::40])
    plt.title('United Airlines VS COVID Cases Over Time')
    plt.show()

    #AAL linear
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('American Avg. Passengers', color='deepskyblue')
    ax1.tick_params(axis='y', labelcolor='deepskyblue')
    ax1.plot(df_passenger_plt.index, df_passenger_plt['American Airlines Inc._avg_passengers'], label = 'AAL ADJ Closing Price', color = 'deepskyblue')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_passenger_plt.index, df_passenger_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_passenger_plt.index[::40])
    plt.title('American Airlines VS COVID Cases Over Time')
    plt.show()

    #DAL linear
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Delta Avg. Passengers', color='darkorchid')
    ax1.tick_params(axis='y', labelcolor='darkorchid')
    ax1.plot(df_passenger_plt.index, df_passenger_plt['Delta Air Lines Inc._avg_passengers'], label = 'DAL ADJ Closing Price', color = 'darkorchid')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_passenger_plt.index, df_passenger_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_passenger_plt.index[::40])
    plt.title('Delta Airlines VS COVID Cases Over Time')
    plt.show()

    #LUV linear
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Southwest Avg. Passengers', color='firebrick')
    ax1.tick_params(axis='y', labelcolor='firebrick')
    ax1.plot(df_passenger_plt.index, df_passenger_plt['Southwest Airlines Co._avg_passengers'], label = 'LUV ADJ Closing Price', color = 'firebrick')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Cases', color='blue')
    ax2.plot(df_passenger_plt.index, df_passenger_plt['cases'], label = 'COVID Cases', color = 'blue')
    ax2.tick_params(axis='y', labelcolor = 'blue')
    plt.xticks(df_passenger_plt.index[::40])
    plt.title('Southwest Airlines VS COVID Cases Over Time')
    plt.show()

    #Passengers by party over time
    politics_by_flights = df[['date', 'avg_passengers_blue_flights', 'avg_passengers_red_flights', 'avg_passengers_mixed_flights']].groupby('date').mean()
    politics_by_flights.drop(politics_by_flights.index[162:], inplace = True)
    plt.plot(politics_by_flights.index, politics_by_flights['avg_passengers_blue_flights'], label = 'Blue to Blue Flights', color = 'b')
    plt.plot(politics_by_flights.index, politics_by_flights['avg_passengers_red_flights'], label = 'Red to Red Flights', color = 'r')
    plt.plot(politics_by_flights.index, politics_by_flights['avg_passengers_mixed_flights'], label = 'Mixed Flights', color = 'g')
    plt.xticks(politics_by_flights.index[::10], rotation = 'vertical')
    plt.title('Passenger Count By Political Stance Over Time')
    plt.xlabel('Dates')
    plt.ylabel('Average Passengers')
    plt.legend()
    plt.show()

    #Create DFs for Flights vs Cases by Party
    case_party = df[['date', 'casedelta', 'color']].groupby(['date','color']).sum()
    case_blueflights = case_party.xs((0), level=('color'))
    case_blueflights.drop(case_blueflights.index[162:], inplace = True)
    case_blueflights['flights'] = politics_by_flights['avg_passengers_blue_flights']
    
    case_redflights = case_party.xs((1), level=('color'))
    case_redflights.drop(case_redflights.index[157:], inplace = True)
    case_redflights['flights'] = politics_by_flights['avg_passengers_red_flights']

    #Blue Flights vs Blue County Cases
    fig, ax1 = plt.subplots()
    ax1.plot(case_blueflights.index, case_blueflights['casedelta'], label = 'Blue State Cases', color = 'slateblue')
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Daily Cases', color='slateblue')
    ax1.tick_params(axis='y', labelcolor='slateblue')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Flight Passengers', color='deepskyblue')
    ax2.plot(case_blueflights.index, case_blueflights['flights'], label = 'Blue to Blue Flights', color = 'deepskyblue')
    ax2.tick_params(axis='y', labelcolor = 'deepskyblue')
    plt.xticks(case_redflights.index[::36])
    plt.title('Blue Flights VS Blue County COVID Cases Over Time')
    plt.show()

    #Red Flights vs Red County Cases
    fig, ax1 = plt.subplots()
    ax1.plot(case_redflights.index, case_redflights['casedelta'], label = 'Red State Cases', color = 'r')
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Daily Cases', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Flight Passengers', color='m')
    ax2.plot(case_redflights.index, case_redflights['flights'], label = 'Red to Red Flights', color = 'm')
    ax2.tick_params(axis='y', labelcolor = 'm')
    plt.xticks(case_redflights.index[::36])
    plt.title('Red Flights VS Red County COVID Cases Over Time')
    plt.show()

    #Create DFs for Red and Blue Flights vs Total County Cases
    case_allflights = df[['date', 'casedelta']].groupby('date').sum()
    case_allflights.drop(case_allflights.index[162:], inplace = True)
    case_allflights['blueflights'] = politics_by_flights['avg_passengers_blue_flights']
    case_allflights['redflights'] = politics_by_flights['avg_passengers_red_flights']

    #Red and Blue Flights vs Total County Cases
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Dates')
    ax1.set_ylabel('Daily Cases', color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    ax1.plot(case_allflights.index, case_allflights['casedelta'], label = 'National Cases', color = 'g')
    ax2 = ax1.twinx()
    ax2.set_ylabel('Average Flight Passengers', color='black')
    ax2.tick_params(axis='y', labelcolor = 'black')
    ax2.plot(case_allflights.index, case_allflights['redflights'], label = 'Red to Red Flights', color = 'r')
    ax2.plot(case_allflights.index, case_allflights['blueflights'], label = 'Blue to Blue Flights', color = 'b')
    ax2.legend()
    plt.xticks(case_allflights.index[::36])
    plt.title('Red and Blue Flights VS Cases Over Time')
    plt.show()
