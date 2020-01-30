import pandas as pd


def tidy_data(df):
    """The dataset we are interested in has a column with only `n/a` values,
    and also 101 rows (you may have been expecting 100!).

    This is because one of the companies (Royal Dutch Shell) has two entries.
    We can get rid of the first instance of these (RDSA).

    Create a function which will, given a dataset loaded into a DataFrame as an argument:
    - Drop the `Strong Buy` column
    - Drop the row with a `Ticker` value of `RDSA`
    - Return the modified DataFrame

    :param df: a DataFrame we want to tidy
    :type df: pd.DataFrame
    :return: a new DataFrame that has been cleaned as above
    :rtype: pd.DataFrame
    """

    return df.drop(df[df['Ticker'] == 'RDSA'].index).drop(columns=['Strong Buy'])


def format_change_values(df):
    """Take a look at the values in the `Change` column.
    You'll see that they are in an inconsistent format, and stored as strings.
    The positive values need to be multiplied by 100, and rounded to two decimal places.
    The negative values need to have the `%` sign removed.

    Also look at the values in the `Mid-price (p)` column.
    At first glance they may look like floats but in fact they have been interpreted as text.
    We need to change them to floats for them to be more useful.

    Create a function which will, taking a DataFrame that has already been processed by the previous
    function as an argument,
    return a new DataFrame with the following changes:

    - A new column called `Change (%)`, with values based on those in the original `Change` column:
        - if a negative value, remove the % sign and convert to a float
        - if a positive value, convert to a float, multiply by 100, and round to two decimal places
    - Remove the original `Change` column (the new `Change (%)` column will be the rightmost column)
    - Convert the values in the `Mid-price (p)` column to floats (keeping the column in the same place)
    - Return the modified DataFrame

    :param df:  a DataFrame pre-tidied by previous function
    :type df: pd.DataFrame
    :return: modified DataFrame
    :rtype: pd.DataFrame
    """

    def munge_changes(row):
        if '-' in row['Change']:
            return float(row['Change'][:-1])
        else:
            return round(float(row['Change']) * 100, 2)

    df['Change (%)'] = df.apply(munge_changes, axis=1)
    df['Mid-price (p)'] = df['Mid-price (p)'].str.replace(',',
                                                          '').astype(float)

    return df.drop(columns=['Change'])


def portfolio_overview(df, portfolio):
    """Let's say we are given the details of a portfolio of shares in a list of tuples,
    each containing the company ticker code, number of shares, and price paid, such as the one below:

        [('BP.', 500, 1535.21), ('GSK', 300, 1821.56), ('HSBA', 2000, 523.45)]

    Create a function which, taking the dataset as processed by both functions above, and a list of tuples
    (such as given above) as arguments, returns a dictionary containing the following keys and the appropriate
    values in the given data formats:

        {
             # The total cost (in £, not pence) of the portfolio (given the number of shares in each holding)
            portfolio_cost: float,

            # The total value (in £, not pence) of the portfolio (given the number of shares in each holding) at the
            # current mid-price
            portfolio_value: float,

            # The percentage change from the original cost of the portfolio to the current value, rounded to one decimal
            # place
            change_in_value: float,

            # A set of any holdings which have increased in value since purchase
            profit: set
        }

    :param df: DataFrame processed with two functions above
    :type df: pd.DataFrame
    :param portfolio: list of tuples representing the portfolio we are interested in
    :type portfolio: list of tuples
    :return: dictionary with attributes described above
    :rtype: dict
    """

    profits = set()
    total_cost = 0.0
    value = 0.0

    for item in portfolio:
        cost = item[1] * item[2]
        total_cost += cost
        price = df[df['Ticker'] == item[0]]['Mid-price (p)'].values[0]
        value += item[1] * price
        if price > item[2]:
            profits.add(item[0])

    return {'portfolio_cost': total_cost/100,
            'portfolio_value': value/100,
            'change_in_value': round(((value - total_cost)/total_cost) * 100, 1),
            'profit': profits}


def sector(df):
    """We're provided with a tidied DataFrame of the FTSE data (such as the one returned after the first two functions).
    We would like to compare the % change in the mid-price for each company to the average % change for all companies in
    the sector,
    along with a summary of the broker recommendations.

    Create a function which returns a DataFrame with the following columns:

        - Company
        - Mid-price (p)
        - Sector
        - Change (%)
        - Avg. Sector Change (%)
        - Our view
        - Beat Sector    # This should be a Boolean column with `True` for holdings where `Change (%)` exceeds that of
        `Avg. Sector Change (%)`
        - Buy Ratio    # This should equal the `Buy` column divided by the `Brokers` column.

    :param df: DataFrame processed with first two functions
    :type df: pd.DataFrame
    :return: new DataFrame with columns described above
    :rtype: pd.DataFrame
    """

    df['Avg. Sector Change (%)'] = df.groupby(
        'Sector')['Change (%)'].transform(pd.Series.mean)
    df['Beat Sector'] = df.apply(
        lambda x: x['Change (%)'] > x['Avg. Sector Change (%)'], axis=1)
    df['Buy Ratio'] = df.apply(
        lambda x: x['Buy'] / x['Brokers'] if x['Brokers'] > 0 else 0, axis=1)

    df['Avg. Sector Change (%)'] = df['Avg. Sector Change (%)'].round(
        decimals=3)

    return df.filter(['Company', 'Mid-price (p)', 'Sector', 'Change (%)', 'Avg. Sector Change (%)',
                      'Our view', 'Beat Sector', 'Buy Ratio'])


def investigate(df, wl):
    """We want to identify any companies which match a given set of rules,
    so that we can look into them further. The rules come in two parts:

        i) Any company on a provided watchlist, whose prices is equal to or lower than the given target price).
        ii) Any company where `Beat Sector` is `False`, `Our view` is `Buy`, and `Buy Ratio` is 0.5 or greater.

    Create a function which, taking a DataFrame such as that returned by the previous function (sector)
    and a watchlist (given as a list of tuples, such as the one below) as arguments,
    returns a list of any companies meeting either requirement. A company meeting both requirements should only appear
    once in the list.

    An example of watchlist:

        [('TUI', 820.0),('Whitbread', 4300.0), ('AstraZeneca', 7500.0), ('Standard Chartered', 920.0)]

    :param df: DataFrame as returned by previous function
    :type df: pd.DataFrame
    :param wl: watchlist as described above
    :type wl: list
    :return: list of companies meeting requirement
    :rtype: list of company names (as string)
    """

    wl_filter = [item[0] for item in wl if not df[(
        df['Company'] == item[0]) & (df['Mid-price (p)'] <= item[1])].empty]
    buy_filter = list(df[(~df['Beat Sector']) & (df['Our view'] == 'Buy') & (
        df['Buy Ratio'] >= 0.5)]['Company'].values)
    return pd.Series(wl_filter + buy_filter).drop_duplicates().tolist()
