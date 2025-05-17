import pandas as pd
import requests
from datetime import datetime
import time
import os

def get_esg_data(ticker):

    # Yahoo Finance API endpoint for ESG data
    url = "https://query2.finance.yahoo.com/v1/finance/esgChart"

    # Simple header to bypass restrictions
    headers = {'User-agent': 'BOT KUNAL'}

    # Parameters
    params = {"symbol": ticker}

    try:
        response = requests.get(url, headers=headers, params=params)

        # Check if request was successful
        if response.ok:
            data = response.json()

            # Extract ESG data
            df = pd.DataFrame(data["esgChart"]["result"][0]["symbolSeries"])
            df["symbol"] = ticker

            # Convert timestamp to datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

            # Sort in descending order by timestamp
            df = df.sort_values(by="timestamp", ascending=False)

            # Handle missing values using mean imputation from nearest rows
            # First, handle all columns except 'esgScore'
            for column in df.columns:
                if column not in ['timestamp', 'symbol', 'esgScore']:
                    # Check if there are any missing values in this column
                    if df[column].isna().any():
                        # Use nearest neighbor interpolation (mean of values above and below)
                        df[column] = df[column].interpolate(method='linear', limit_direction='both')

            # Handle 'esgScore' column specially if it exists
            if 'esgScore' in df.columns:
                # First check if all component columns exist
                component_columns = ['governanceScore', 'environmentalScore', 'socialScore']
                if all(col in df.columns for col in component_columns):
                    # For rows with missing esgScore, calculate as sum of components
                    mask = df['esgScore'].isna()
                    df.loc[mask, 'esgScore'] = (
                        df.loc[mask, 'governanceScore'] +
                        df.loc[mask, 'environmentalScore'] +
                        df.loc[mask, 'socialScore']
                    )
                    
                    # Add validation to check for discrepancies
                    calculated_esg = df[component_columns].sum(axis=1)
                    discrepancy_mask = (df['esgScore'] != calculated_esg) & (df[component_columns].sum(axis=1) > 0)
                    if discrepancy_mask.any():
                        print(f"Warning: ESG score discrepancy found for {ticker} on dates: {df.loc[discrepancy_mask, 'timestamp'].dt.strftime('%Y-%m-%d').tolist()}")
                        print("Original ESG scores:", df.loc[discrepancy_mask, 'esgScore'].tolist())
                        print("Calculated from components:", calculated_esg[discrepancy_mask].tolist())
                else:
                    # If component columns don't exist, use the same interpolation as other columns
                    df['esgScore'] = df['esgScore'].interpolate(method='linear', limit_direction='both')

            return df
        else:
            print(f"Error fetching ESG data for {ticker}: HTTP {response.status_code}")
            return None

    except Exception as e:
        print(f"Error fetching ESG data for {ticker}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # List of tickers to fetch
    tickers = ['MSFT', 'NVDA', 'AAPL', 'GOOGL', 'META', 'AMZN', 'META', 'AVGO', 'TSLA', 'GOOGL', 'BRK.B', 'GOOG', 'JPM', 'V', 'LLY', 'NFLX', 'XOM', 'MA', 'COST', 'WMT', 'PG', 'HD', 'JNJ', 'ABBV', 'BAC', 'UNH', 'CRM', 'KO', 'PLTR', 'ORCL', 'PM', 'WFC', 'CSCO', 'GE', 'IBM', 'CVX', 'ABT', 'MCD', 'LIN', 'NOW', 'DIS', 'ISRG', 'ACN', 'GS', 'AMD', 'T', 'UBER', 'MRK', 'INTU', 'VZ', 'PEP', 'RTX', 'ADBE', 'BKNG', 'TXN', 'QCOM', 'CAT', 'AXP', 'PGR', 'MS', 'SPGI', 'TMO', 'BA', 'BSX', 'SCHW', 'NEE', 'TJX', 'AMAT', 'C', 'HON', 'AMGN', 'BLK', 'UNP', 'SYK', 'CMCSA', 'ETN', 'LOW', 'PANW', 'DE', 'ADP', 'PFE', 'GILD', 'DHR', 'GEV', 'COP', 'TMUS', 'ADI', 'MMC', 'LRCX', 'BX', 'VRTX', 'MDT', 'FI', 'CRWD', 'KLAC', 'MU', 'CB', 'APH', 'ANET', 'PLD', 'ICE', 'SBUX', 'CME', 'AMT', 'MO', 'TT', 'LMT', 'INTC', 'SO', 'CEG', 'BMY', 'CDNS', 'WELL', 'DUK', 'KKR', 'ELV', 'PH', 'MCK', 'AJG', 'EQIX', 'CI', 'MDLZ', 'SHW', 'WM', 'MMM', 'SNPS', 'TDG', 'AON', 'ORLY', 'CVS', 'COF', 'MCO', 'CTAS', 'UPS', 'NKE', 'PYPL', 'CL', 'WMB', 'CMG', 'PNC', 'MSI', 'ZTS', 'USB', 'GD', 'EMR', 'DASH', 'HCA', 'FTNT', 'ITW', 'EOG', 'HWM', 'APO', 'JCI', 'ADSK', 'BK', 'ECL', 'MAR', 'RCL', 'NOC', 'AZO', 'HLT', 'ROP', 'APD', 'REGN', 'CSX', 'TRV', 'ABNB', 'CARR', 'WDAY', 'FCX', 'NEM', 'CPRT', 'NSC', 'TFC', 'OKE', 'NXPI', 'ALL', 'KMI', 'AXON', 'VST', 'AEP', 'DLR', 'FICO', 'MPC', 'PSX', 'AFL', 'FDX', 'PWR', 'SLB', 'DFS', 'AMP', 'GM', 'ROST', 'PCAR', 'SPG', 'BDX', 'PAYX', 'AIG', 'RSG', 'COR', 'TEL', 'O', 'GWW', 'SRE', 'PSA', 'URI', 'CTVA', 'MET', 'FAST', 'CMI', 'D', 'EW', 'KVUE', 'KDP', 'KMB', 'MSCI', 'KR', 'TGT', 'MNST', 'CCI', 'VRSK', 'VLO', 'EXC', 'IDXX', 'AME', 'F', 'LHX', 'FIS', 'YUM', 'CHTR', 'CTSH', 'XEL', 'PEG', 'CBRE', 'OTIS', 'PRU', 'TTWO', 'BKR', 'HES', 'PCG', 'TRGP', 'RMD', 'HIG', 'GLW', 'CAH', 'LULU', 'VMC', 'MPWR', 'EA', 'WAB', 'SYY', 'ROK', 'DELL', 'DHI', 'ETR', 'ED', 'IT', 'ACGL', 'DXCM', 'EFX', 'EQT', 'NDAQ', 'IR', 'GEHC', 'EBAY', 'MLM', 'VICI', 'MCHP', 'DAL', 'WEC', 'ODFL', 'CSGP', 'A', 'NRG', 'EXR', 'GRMN', 'MTB', 'XYL', 'ANSS', 'WTW', 'OXY', 'CNC', 'GIS', 'STZ', 'AVB', 'IRM', 'DD', 'KEYS', 'STT', 'VTR', 'RJF', 'BR', 'HUM', 'NUE', 'DTE', 'TSCO', 'FANG', 'HPQ', 'TPL', 'IP', 'GDDY', 'FITB', 'AWK', 'UAL', 'PPG', 'BRO', 'AEE', 'DOV', 'LEN', 'CDW', 'FTV', 'PPL', 'VLTO', 'CPAY', 'DRI', 'ATO', 'TYL', 'HSY', 'SBAC', 'CCL', 'SYF', 'IQV', 'EXE', 'CNP', 'KHC', 'ADM', 'EQR', 'HPE', 'HBAN', 'MTD', 'SW', 'TDY', 'CINF', 'CHD', 'SMCI', 'PODD', 'VRSN', 'STE', 'LYV', 'DVN', 'CBOE', 'ES', 'STX', 'K', 'EIX', 'TROW', 'NVR', 'WRB', 'DOW', 'WSM', 'FE', 'AMCR', 'NTRS', 'EXPE', 'HUBB', 'FSLR', 'PHM', 'PTC', 'GPN', 'WBD', 'CMS', 'WAT', 'RF', 'LH', 'NTAP', 'LDOS', 'DECK', 'DG', 'DGX', 'IFF', 'INVH', 'ULTA', 'ON', 'ZBH', 'LII', 'STLD', 'WY', 'LUV', 'MKC', 'MAA', 'HAL', 'JBL', 'CTRA', 'CFG', 'ESS', 'NI', 'BIIB', 'FDS', 'DLTR', 'TRMB', 'MOH', 'GPC', 'TPR', 'PKG', 'SNA', 'PFG', 'WDC', 'DPZ', 'KEY', 'CLX', 'FFIV', 'PNR', 'EXPD', 'COO', 'APTV', 'BALL', 'LNT', 'GEN', 'TSN', 'BAX', 'ROL', 'J', 'L', 'ZBRA', 'LYB', 'EL', 'WST', 'CF', 'OMC', 'EVRG', 'EG', 'LVS', 'AVY', 'BBY', 'IEX', 'KIM', 'MAS', 'BLDR', 'TER', 'TXT', 'ALGN', 'JKHY', 'HOLX', 'UDR', 'CPT', 'ALLE', 'PAYC', 'JNPR', 'FOXA', 'DOC', 'REG', 'JBHT', 'SJM', 'POOL', 'AKAM', 'SWKS', 'CHRW', 'SWK', 'RVTY', 'UHS', 'BG', 'ARE', 'NDSN', 'LKQ', 'HST', 'RL', 'TKO', 'NWSA', 'CAG', 'MOS', 'KMX', 'EPAM', 'VTRS', 'AIZ', 'PNW', 'GL', 'SOLV', 'INCY', 'BXP', 'TAP', 'EMN', 'DAY', 'IPG', 'ERIE', 'AES', 'HII', 'HSIC', 'WYNN', 'NCLH', 'HAS', 'HRL', 'MRNA', 'AOS', 'WBA', 'MKTX', 'MGM', 'GNRC', 'TECH', 'MTCH', 'LW', 'FRT', 'ALB', 'CRL', 'PARA', 'IVZ', 'BEN', 'CPB', 'APA', 'FOX', 'CZR', 'ENPH', 'BF.B']


    # List to store DataFrames
    dataframes = []

    # Create directory structure if it doesn't exist
    save_dir = "Datasets/ESG Data/"
    os.makedirs(save_dir, exist_ok=True)

    for ticker in tickers:
        df = get_esg_data(ticker)

        if df is not None:
            dataframes.append(df)

            # Save individual ticker data - exclude the 'symbol' column
            file_path = f"{save_dir}{ticker}_esg_data.csv"
            df = df.drop(columns=['symbol'])
            df.to_csv(file_path, index=False)

        # Add delay between requests to avoid hitting rate limits
        time.sleep(1)

    print(f"Successfully Fetched ESG Data for All Tickers!")
    print("Data collection complete, files saved to 'Datasets/ESG Data/' folder.")