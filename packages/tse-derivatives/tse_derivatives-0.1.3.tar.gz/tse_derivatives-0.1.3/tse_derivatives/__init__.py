import requests as rq
import pandas as pd

def tse_options(ticker:str ='خودرو',type:str ='call')-> pd.DataFrame:
    """
    Inputs:
    ticker (str): The options underlying asset ticker. example 'خودرو'
    type (str): option type. 'call' or 'put'

    Returns:
    Dataframe: options data
    """
    url = 'https://cdn.tsetmc.com/api/Instrument/GetInstrumentOptionMarketWatch/0'
    headers = {'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

    result = rq.get(url, headers=headers)
    if result.status_code != 200:
        raise Exception(f"Failed to retrieve data. Status code: {result.status_code}")

    data = result.json()
    data = pd.DataFrame(data)
    data = data['instrumentOptMarketWatch'].apply(pd.Series)
    data = data[(data['lval30_UA'].str.contains(ticker))].reset_index(drop=True)
    options = pd.DataFrame(columns=['options ticker','options price','strike price', 'volume', 'days to maturity','underlying asset price'])
    options['strike price'] = data['strikePrice'].astype(float)
    options['days to maturity'] = data['remainedDay'].astype(float)
    options['underlying asset price']=data['pClosing_UA']
    if type=='call':
        options['options price'] = data['pClosing_C'].astype(float)
        options['options ticker'] = data['lVal18AFC_C'].astype(str)
        options['volume'] = data['qTotTran5J_C'].astype(float)

    elif type=='put':
        options['options price'] = data['pClosing_P'].astype(float)
        options['options ticker'] = data['lVal18AFC_P'].astype(str)
        options['volume'] = data['qTotTran5J_P'].astype(float)

    else:
        print(f'Define the option type as call or put')

    return options
