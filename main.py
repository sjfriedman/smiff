import numpy as np
import pandas as pd
import pandas_datareader as read
import scipy.stats as stats

# Will load our stock data into a data DataFrame
# Input: String Arrary of tickers, defaults to given by assignment KO, TSLA, SPY
# Output: Pandas DataFrame
def main(tickers = ['KO', 'TSLA', 'SPY']):
    df = pd.DataFrame()
    # for each ticker in list
    for ticker in tickers:
        # get the tickers stokck data from start to end_date and append data to stock_info
        info = read.DataReader(ticker, 'yahoo', '2021-01-01', '2021-12-31')
        info['ticker'] = ticker
        # gets day to day percent change and z_value
        info['percent_change'] = info['Adj Close'].pct_change()
        info['z_value'] = (info['Adj Close'] - info['Adj Close'].mean()) / info['Adj Close'].std()
        df = pd.concat([df, info])
    df = df.fillna(0)

    return df

# Computes statistics of a comparison between the two stocks
# Input: df - dataframe to process with all stock data
# Input: array of 2 tickers to compare symbols
# Outputs: None, will print data to console
def statistics(df, tickers = ['KO', 'TSLA']):

    # Commented inline with print statement to explain the logic
    def variance(df, tickers = ['KO', 'TSLA']):
        print("VARIANCE TEST")
        print("Looking at dataset through the assumption that the year 2021 is a randomly picked year"
        + "\nsince there are more than 30 samples, Central limit thereom states that data is approximately normal"
        + "\nnull hypothesis: σ^2(of stock 1)=σ^2(stock 2) with p = 0.05"
        + "\nalternative hypothesis: σ^2(of stock 1)≠σ^2(stock 2)"
        + "\nusing levenes test to test for statiscal difference between stocks")
        # true if p value is significant and false if not
        p_value = stats.levene(df.loc[df['ticker'] == tickers[0]]['percent_change'],df.loc[df['ticker'] == tickers[1]]['percent_change'], center='mean')[1]
        # print(p_value)
        print("since the p value(" + str(p_value) + ") p < 0.05, there is sufficient evidence to say the"
        + "\nreject the null hypothesis and accept the alternative hypothesis that"
        + "\nthe variances between the two tickers are significantly different")
        print('\n-------------------------------------------------------------\n')

    # Commented inline with print statement to explain the logic
    def welches_test(df, tickers = ['KO', 'TSLA']):
        print("WELCHES TEST")
        # gets ride of outliers
        df.loc[np.abs(df['z_value']) < 3]
        print("Looking at dataset through the assumption that the year 2021 is a randomly picked year"
        + "\nsince there are larger than 30 samples, Central limit thereom states that data is approximately normal"
        + "\nWhile the number of datapoints is equal, the variances between KO and TSLA are not similar"
        + "\nBecause of this, The Welches T test will be used instead of the student t test"
        + "\nTo test for a significant difference in mean daily returns, I used a"
        + "\nthe Welches T test To perform this test, I am assuming that the"
        + "\nobservations in each sample are: independent"
        + "\nnormally distributed, and have difference variances."
        + "\nnull hypothesis: μ1=μ2 with p = 0.05")
        # return true if p value is significant and false if not
        p_value = stats.ttest_ind(df.loc[df['ticker'] == tickers[0]]['percent_change'], df.loc[df['ticker'] == tickers[1]]['percent_change'], equal_var=False)[1]
        print("\nalternative hypothesis: μ1≠μ2"
            + "\nbecause the p-value (" + str(p_value) + ") is greater than the significance level of"
            + "\n0.05, we fail to reject the null hypothesis, meaning that there is no"
            + "\nsignificant difference between the mean daily returns of the two equities")
        print('\n-------------------------------------------------------------\n')

    return variance(df), welches_test(df)



# Computes and prints metrics of a chosen ticker
# Input: df - dataframe to process with all stock data
# Input: array of 2 tickers to compare symbols
# Outputs: None, will print data to console
def metrics(df, ticker = 'KO'):
    # gets data from dataframe that includes KO
    df = df.loc[df['ticker'] == ticker]

    # Commented inline with print statement to explain the logic
    def volatility(df):
        print('VOLATILITY')
        mean_price = df['Adj Close'].mean()
        annual_volatility = str(100*df['percent_change'].std() * len(df)**.5)
        weekly_volatility = str(100*df['percent_change'].std() * 5**.5)
        daily_volatility = str(100*df['percent_change'].std())
        print("volatility is a measure of how much a stock will fluctuate from its average price within a given time period(in this case a year)"
        "During 2021 the ticker KO's mean price was" + str(mean_price)
        +"\nThe annual volatility of KO is " + annual_volatility + " percent meaning that over 2021 the price of KO flucatuated " + annual_volatility + " percent from its mean price"
        +"\nThe weekly volatility of KO is " + weekly_volatility + " percent meaning that over 2021 the price of KO flucatuated " + weekly_volatility + " percent from its mean price from week to week"
        +"\nThe daily volatility of KO is " + daily_volatility + " percent meaning that over 2021 the price of KO flucatuated " + daily_volatility + " percent from its mean price from day to day")
        print('\n-------------------------------------------------------------\n')
    # Commented inline with print statement to explain the logic
    def value_at_risk(df):
        print('VALUE AT RISK')
        # there is 95% confidence that the max amount that a stock can lose to a day is 1.46 percent
        var_95 = str(100*stats.norm.ppf(1-0.95, df['percent_change'].mean(), df['percent_change'].std()))
        print("there is 95% confidence that the max amount that a stock can lose to a day is " + var_95 + " percent")
        print('\n-------------------------------------------------------------\n')

    # Commented inline with print statement to explain the logic
    def sharpe_ratio(df, risk_free_rate = 0.011):
        print('SHARPE RATIO')
        annual_sharpe_ratio = str(df['percent_change'].mean() - risk_free_rate / len(df) / df['percent_change'].std() * len(df)**.5)
        print("using a risk free rate of 0.11 because that was the cost of a 1 year US"
        + "\ntreasury bond on Jan 4th 2021"
        + "\nOver the year of 2021 the annual sharpe ratio was " + annual_sharpe_ratio + " ≈ 1 meaning that there was a acceptable risk factor"
        + "\ncompared to a treasury bonds for the given returns")
        print('\n-------------------------------------------------------------\n')

    # Commented inline with print statement to explain the logic
    def downside_deviation(df, risk_free_rate = 0.011):
        print('DOWNSIDE DEVIATION')
        # gets the percent_change of the day - the risk_free_rate of that day
        change_risk_free = df['percent_change'] - risk_free_rate / len(df)
        # gets all the percent_change - risk_free_rate < 0, puts them in percentage form and squares them
        change_risk_free = (change_risk_free.loc[change_risk_free.values < 0] * 100) ** 2
        # adds up the squares divides by the number of items and square roots
        downside_dev =str((sum(change_risk_free) / len(change_risk_free)) ** .5)
        print("using a risk free rate of 0.11 because that was the cost of a 1 year US"
        + "\ntreasury bond on Jan 4th 2021"
        + "\nThe downside risk is " + downside_dev + " meaning that there is very little downside potential to KO")
        print('\n-------------------------------------------------------------\n')

    def max_drawdown(df):
        print('MAX DRAWDOWN')
        # gets cumaltive maximums over time(identifying peaks)
        rolling_maxiumums = df['Adj Close'].rolling(len(df), min_periods=1).max()

        # finds how far away other days prices are way from nearby peak
        day_down = df['Adj Close']/rolling_maxiumums - 1.0

        # finds the largest negative value from a peak to a trough
        max_down = (str(-100*day_down.cummin()[-1]))

        print("The maximum loss on this stock from a peak to a trough is " + max_down +  " percent")
        print('\n-------------------------------------------------------------\n')

    # Here we call for each metric the related function to display metric and how it is computed
    volatility(df)
    value_at_risk(df)
    sharpe_ratio(df)
    downside_deviation(df)
    max_drawdown(df)

# Computes and prints the beta and alpha of chosen symbol
# Input: df - dataframe to process with all stock data
# Input: singular ticker
# Outputs: None, will print data to console
def capm(df, ticker = 'TSLA'):

    # Commented inline with print statement to explain the logic
    def beta(df, ticker = 'TSLA', show_text = True):


        # gets the correlation between spy and KO
        correlation = np.corrcoef(df.loc[df['ticker'] == 'SPY']['percent_change'], df.loc[df['ticker'] == ticker]['percent_change'])[1,0]
        std_div = (df.loc[df['ticker'] == ticker]['percent_change'].std()/df.loc[df['ticker'] == 'SPY']['percent_change'].std())
        if show_text:
            print( "\nBETA\nbeta is how much the markets volatility affects a stock."
            +"\nTSLA's beta is " + str(correlation*std_div)
            +"\nThis means that TSLA is " + str(correlation*std_div) + " times as volatile as the market")
            print('\n-------------------------------------------------------------\n')
        else:
            return correlation*std_div

    # Commented inline with print statement to explain the logic
    def alpha(df, ticker = 'TSLA', risk_free_rate = 0.0126):
        print("ALPHA")

        # gets the return of holding the ticker and SPY over the year
        stock_return = (df.loc[df['ticker'] == ticker]['Close'].iloc[-1] - df.loc[df['ticker'] == ticker]['Open'].iloc[0]) / df.loc[df['ticker'] == ticker]['Open'].iloc[0]
        spy_change = str(100*((df.loc[df['ticker'] == 'SPY']['Close'].iloc[-1] - df.loc[df['ticker'] == 'SPY']['Open'].iloc[0]) / df.loc[df['ticker'] == 'SPY']['Open'].iloc[0]))

        # gets the percentage change of KO and subtracts the free risk rate
        stock_min_risk = stock_return - risk_free_rate - beta(df, show_text=False) *  - risk_free_rate
        print(stock_min_risk)
        print("If 1 stock of TSLA and S&P is purchased at the open of the first day"
        + "\nand sold at the last day the TSLA would underperform"
        + "\nby " + str(stock_min_risk)+ " percent")
        print('\n-------------------------------------------------------------\n')

    # calling alpha and beta for Capm function to print each value
    alpha(df)
    beta(df)


# start the process of loading data and expect a returned DataFrame
df = main()

# Call the required funtions from the assignment using default values for tickers
# statistics(df)
# metrics(df)
capm(df)
