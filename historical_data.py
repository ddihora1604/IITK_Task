import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import os

def get_historical_data(ticker, period="5y"):

    # Calculate timestamps (Unix timestamp in seconds)
    end_date = datetime.now()
    if period == "5y":
        start_date = end_date - timedelta(days=5*365)
    else:
        # Default to 5 years if period is not recognized
        start_date = end_date - timedelta(days=5*365)

    period1 = int(start_date.timestamp())
    period2 = int(end_date.timestamp())

    # Yahoo Finance API endpoint for historical data
    url = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"

    # Parameters
    params = {
        "symbol": ticker,
        "period1": period1,
        "period2": period2,
        "interval": "1d",  # Daily data
        "includePrePost": False,
        "events": "div,split"
    }

    # Simple header to bypass restrictions
    headers = {'User-agent': 'BOT KUNAL'}

    try:
        response = requests.get(
            url.format(ticker=ticker),
            headers=headers,
            params=params
        )

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()

            # Extract relevant data
            timestamps = data["chart"]["result"][0]["timestamp"]
            quote = data["chart"]["result"][0]["indicators"]["quote"][0]

            # Convert to DataFrame
            df = pd.DataFrame({
                'Date': pd.to_datetime(timestamps, unit='s'),
                'Open': quote['open'],
                'High': quote['high'],
                'Low': quote['low'],
                'Close': quote['close'],
                'Volume': quote['volume']
            })

            # Set Date as index and convert to YYYY-MM-DD format without time component
            df.set_index('Date', inplace=True)
            df.index = pd.to_datetime(df.index).strftime('%Y-%m-%d')

            # Create a complete date range for exactly 5 years (including all days)
            all_dates = pd.date_range(end=end_date.strftime('%Y-%m-%d'),
                                     start=(end_date - timedelta(days=5*365)).strftime('%Y-%m-%d'),
                                     freq='D')  # 'D' for calendar days
            all_dates = all_dates.strftime('%Y-%m-%d')

            # Reindex with all dates and interpolate missing values using mean
            df_reindexed = df.reindex(all_dates)

            # Use interpolation (linear) for mean imputation of missing values
            df_reindexed = df_reindexed.interpolate(method='linear')

            # Sort in descending order (newest first)
            df_reindexed = df_reindexed.sort_index(ascending=False)

            return df_reindexed

        else:
            print(f"Error fetching data for {ticker}: HTTP {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # List of tickers to fetch
    
    tickers = ['MSFT', 'NVDA', 'AAPL', 'GOOGL', 'META', 'AMZN', 'META', 'AVGO', 'TSLA', 'GOOGL', 'BRK.B', 'GOOG', 'JPM', 'V', 'LLY', 'NFLX', 'XOM', 'MA', 'COST', 'WMT', 'PG', 'HD', 'JNJ', 'ABBV', 'BAC', 'UNH', 'CRM', 'KO', 'PLTR', 'ORCL', 'PM', 'WFC', 'CSCO', 'GE', 'IBM', 'CVX', 'ABT', 'MCD', 'LIN', 'NOW', 'DIS', 'ISRG', 'ACN', 'GS', 'AMD', 'T', 'UBER', 'MRK', 'INTU', 'VZ', 'PEP', 'RTX', 'ADBE', 'BKNG', 'TXN', 'QCOM', 'CAT', 'AXP', 'PGR', 'MS', 'SPGI', 'TMO', 'BA', 'BSX', 'SCHW', 'NEE', 'TJX', 'AMAT', 'C', 'HON', 'AMGN', 'BLK', 'UNP', 'SYK', 'CMCSA', 'ETN', 'LOW', 'PANW', 'DE', 'ADP', 'PFE', 'GILD', 'DHR', 'GEV', 'COP', 'TMUS', 'ADI', 'MMC', 'LRCX', 'BX', 'VRTX', 'MDT', 'FI', 'CRWD', 'KLAC', 'MU', 'CB', 'APH', 'ANET', 'PLD', 'ICE', 'SBUX', 'CME', 'AMT', 'MO', 'TT', 'LMT', 'INTC', 'SO', 'CEG', 'BMY', 'CDNS', 'WELL', 'DUK', 'KKR', 'ELV', 'PH', 'MCK', 'AJG', 'EQIX', 'CI', 'MDLZ', 'SHW', 'WM', 'MMM', 'SNPS', 'TDG', 'AON', 'ORLY', 'CVS', 'COF', 'MCO', 'CTAS', 'UPS', 'NKE', 'PYPL', 'CL', 'WMB', 'CMG', 'PNC', 'MSI', 'ZTS', 'USB', 'GD', 'EMR', 'DASH', 'HCA', 'FTNT', 'ITW', 'EOG', 'HWM', 'APO', 'JCI', 'ADSK', 'BK', 'ECL', 'MAR', 'RCL', 'NOC', 'AZO', 'HLT', 'ROP', 'APD', 'REGN', 'CSX', 'TRV', 'ABNB', 'CARR', 'WDAY', 'FCX', 'NEM', 'CPRT', 'NSC', 'TFC', 'OKE', 'NXPI', 'ALL', 'KMI', 'AXON', 'VST', 'AEP', 'DLR', 'FICO', 'MPC', 'PSX', 'AFL', 'FDX', 'PWR', 'SLB', 'DFS', 'AMP', 'GM', 'ROST', 'PCAR', 'SPG', 'BDX', 'PAYX', 'AIG', 'RSG', 'COR', 'TEL', 'O', 'GWW', 'SRE', 'PSA', 'URI', 'CTVA', 'MET', 'FAST', 'CMI', 'D', 'EW', 'KVUE', 'KDP', 'KMB', 'MSCI', 'KR', 'TGT', 'MNST', 'CCI', 'VRSK', 'VLO', 'EXC', 'IDXX', 'AME', 'F', 'LHX', 'FIS', 'YUM', 'CHTR', 'CTSH', 'XEL', 'PEG', 'CBRE', 'OTIS', 'PRU', 'TTWO', 'BKR', 'HES', 'PCG', 'TRGP', 'RMD', 'HIG', 'GLW', 'CAH', 'LULU', 'VMC', 'MPWR', 'EA', 'WAB', 'SYY', 'ROK', 'DELL', 'DHI', 'ETR', 'ED', 'IT', 'ACGL', 'DXCM', 'EFX', 'EQT', 'NDAQ', 'IR', 'GEHC', 'EBAY', 'MLM', 'VICI', 'MCHP', 'DAL', 'WEC', 'ODFL', 'CSGP', 'A', 'NRG', 'EXR', 'GRMN', 'MTB', 'XYL', 'ANSS', 'WTW', 'OXY', 'CNC', 'GIS', 'STZ', 'AVB', 'IRM', 'DD', 'KEYS', 'STT', 'VTR', 'RJF', 'BR', 'HUM', 'NUE', 'DTE', 'TSCO', 'FANG', 'HPQ', 'TPL', 'IP', 'GDDY', 'FITB', 'AWK', 'UAL', 'PPG', 'BRO', 'AEE', 'DOV', 'LEN', 'CDW', 'FTV', 'PPL', 'VLTO', 'CPAY', 'DRI', 'ATO', 'TYL', 'HSY', 'SBAC', 'CCL', 'SYF', 'IQV', 'EXE', 'CNP', 'KHC', 'ADM', 'EQR', 'HPE', 'HBAN', 'MTD', 'SW', 'TDY', 'CINF', 'CHD', 'SMCI', 'PODD', 'VRSN', 'STE', 'LYV', 'DVN', 'CBOE', 'ES', 'STX', 'K', 'EIX', 'TROW', 'NVR', 'WRB', 'DOW', 'WSM', 'FE', 'AMCR', 'NTRS', 'EXPE', 'HUBB', 'FSLR', 'PHM', 'PTC', 'GPN', 'WBD', 'CMS', 'WAT', 'RF', 'LH', 'NTAP', 'LDOS', 'DECK', 'DG', 'DGX', 'IFF', 'INVH', 'ULTA', 'ON', 'ZBH', 'LII', 'STLD', 'WY', 'LUV', 'MKC', 'MAA', 'HAL', 'JBL', 'CTRA', 'CFG', 'ESS', 'NI', 'BIIB', 'FDS', 'DLTR', 'TRMB', 'MOH', 'GPC', 'TPR', 'PKG', 'SNA', 'PFG', 'WDC', 'DPZ', 'KEY', 'CLX', 'FFIV', 'PNR', 'EXPD', 'COO', 'APTV', 'BALL', 'LNT', 'GEN', 'TSN', 'BAX', 'ROL', 'J', 'L', 'ZBRA', 'LYB', 'EL', 'WST', 'CF', 'OMC', 'EVRG', 'EG', 'LVS', 'AVY', 'BBY', 'IEX', 'KIM', 'MAS', 'BLDR', 'TER', 'TXT', 'ALGN', 'JKHY', 'HOLX', 'UDR', 'CPT', 'ALLE', 'PAYC', 'JNPR', 'FOXA', 'DOC', 'REG', 'JBHT', 'SJM', 'POOL', 'AKAM', 'SWKS', 'CHRW', 'SWK', 'RVTY', 'UHS', 'BG', 'ARE', 'NDSN', 'LKQ', 'HST', 'RL', 'TKO', 'NWSA', 'CAG', 'MOS', 'KMX', 'EPAM', 'VTRS', 'AIZ', 'PNW', 'GL', 'SOLV', 'INCY', 'BXP', 'TAP', 'EMN', 'DAY', 'IPG', 'ERIE', 'AES', 'HII', 'HSIC', 'WYNN', 'NCLH', 'HAS', 'HRL', 'MRNA', 'AOS', 'WBA', 'MKTX', 'MGM', 'GNRC', 'TECH', 'MTCH', 'LW', 'FRT', 'ALB', 'CRL', 'PARA', 'IVZ', 'BEN', 'CPB', 'APA', 'FOX', 'CZR', 'ENPH', 'BF.B']


    # Dictionary to store DataFrames
    stock_data = {}

    # Create directory structure if it doesn't exist
    save_dir = "Datasets/Historical Data/"
    os.makedirs(save_dir, exist_ok=True)

    for ticker in tickers:
        stock_data[ticker] = get_historical_data(ticker)

        # Add delay between requests to avoid hitting rate limits
        time.sleep(1)

        # Save to csv in the specified folder structure
        if stock_data[ticker] is not None:
            file_path = f"{save_dir}{ticker}_historical_data.csv"
            stock_data[ticker].to_csv(file_path)
    print(f"Successfully Fetched Historical Data for All Tickers!")
    print("Data collection complete, files saved to 'Datasets/Historical Data/' folder.")