import pandas as pd
import requests
import os
import time
import random
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_statistics_data(ticker, max_retries=3):
    
    # Yahoo Finance statistics URL
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics"
    
    # More realistic headers that mimic a regular browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    # Create a session with retry capability
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=0.5,  # Exponential backoff
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    try:
        # Make the request with the session
        
        response = session.get(url, headers=headers, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Create dictionary to store data
            stats_data = {}
            
            # Find all statistics tables
            tables = soup.find_all('table')
            
            # Extract data from each table
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    # Get cells
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        stat_name = cells[0].text.strip()
                        stat_value = cells[1].text.strip()
                        stats_data[stat_name] = stat_value
            
            # Convert to DataFrame
            df = pd.DataFrame(list(stats_data.items()), columns=['Statistic', 'Value'])
            
            if len(df) == 0:
                print(f"Warning: No data found for {ticker}. The page structure might have changed.")
                
            return df
            
        else:
            print(f"Error fetching statistics for {ticker}: HTTP {response.status_code}")
            print(f"Response content: {response.text[:200]}...")  # Print first 200 chars of response
            return None
            
    except Exception as e:
        print(f"Error fetching statistics for {ticker}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # List of tickers to fetch
    tickers = ['MSFT', 'NVDA', 'AAPL', 'GOOGL', 'META', 'AMZN', 'META', 'AVGO', 'TSLA', 'GOOGL', 'BRK.B', 'GOOG', 'JPM', 'V', 'LLY', 'NFLX', 'XOM', 'MA', 'COST', 'WMT', 'PG', 'HD', 'JNJ', 'ABBV', 'BAC', 'UNH', 'CRM', 'KO', 'PLTR', 'ORCL', 'PM', 'WFC', 'CSCO', 'GE', 'IBM', 'CVX', 'ABT', 'MCD', 'LIN', 'NOW', 'DIS', 'ISRG', 'ACN', 'GS', 'AMD', 'T', 'UBER', 'MRK', 'INTU', 'VZ', 'PEP', 'RTX', 'ADBE', 'BKNG', 'TXN', 'QCOM', 'CAT', 'AXP', 'PGR', 'MS', 'SPGI', 'TMO', 'BA', 'BSX', 'SCHW', 'NEE', 'TJX', 'AMAT', 'C', 'HON', 'AMGN', 'BLK', 'UNP', 'SYK', 'CMCSA', 'ETN', 'LOW', 'PANW', 'DE', 'ADP', 'PFE', 'GILD', 'DHR', 'GEV', 'COP', 'TMUS', 'ADI', 'MMC', 'LRCX', 'BX', 'VRTX', 'MDT', 'FI', 'CRWD', 'KLAC', 'MU', 'CB', 'APH', 'ANET', 'PLD', 'ICE', 'SBUX', 'CME', 'AMT', 'MO', 'TT', 'LMT', 'INTC', 'SO', 'CEG', 'BMY', 'CDNS', 'WELL', 'DUK', 'KKR', 'ELV', 'PH', 'MCK', 'AJG', 'EQIX', 'CI', 'MDLZ', 'SHW', 'WM', 'MMM', 'SNPS', 'TDG', 'AON', 'ORLY', 'CVS', 'COF', 'MCO', 'CTAS', 'UPS', 'NKE', 'PYPL', 'CL', 'WMB', 'CMG', 'PNC', 'MSI', 'ZTS', 'USB', 'GD', 'EMR', 'DASH', 'HCA', 'FTNT', 'ITW', 'EOG', 'HWM', 'APO', 'JCI', 'ADSK', 'BK', 'ECL', 'MAR', 'RCL', 'NOC', 'AZO', 'HLT', 'ROP', 'APD', 'REGN', 'CSX', 'TRV', 'ABNB', 'CARR', 'WDAY', 'FCX', 'NEM', 'CPRT', 'NSC', 'TFC', 'OKE', 'NXPI', 'ALL', 'KMI', 'AXON', 'VST', 'AEP', 'DLR', 'FICO', 'MPC', 'PSX', 'AFL', 'FDX', 'PWR', 'SLB', 'DFS', 'AMP', 'GM', 'ROST', 'PCAR', 'SPG', 'BDX', 'PAYX', 'AIG', 'RSG', 'COR', 'TEL', 'O', 'GWW', 'SRE', 'PSA', 'URI', 'CTVA', 'MET', 'FAST', 'CMI', 'D', 'EW', 'KVUE', 'KDP', 'KMB', 'MSCI', 'KR', 'TGT', 'MNST', 'CCI', 'VRSK', 'VLO', 'EXC', 'IDXX', 'AME', 'F', 'LHX', 'FIS', 'YUM', 'CHTR', 'CTSH', 'XEL', 'PEG', 'CBRE', 'OTIS', 'PRU', 'TTWO', 'BKR', 'HES', 'PCG', 'TRGP', 'RMD', 'HIG', 'GLW', 'CAH', 'LULU', 'VMC', 'MPWR', 'EA', 'WAB', 'SYY', 'ROK', 'DELL', 'DHI', 'ETR', 'ED', 'IT', 'ACGL', 'DXCM', 'EFX', 'EQT', 'NDAQ', 'IR', 'GEHC', 'EBAY', 'MLM', 'VICI', 'MCHP', 'DAL', 'WEC', 'ODFL', 'CSGP', 'A', 'NRG', 'EXR', 'GRMN', 'MTB', 'XYL', 'ANSS', 'WTW', 'OXY', 'CNC', 'GIS', 'STZ', 'AVB', 'IRM', 'DD', 'KEYS', 'STT', 'VTR', 'RJF', 'BR', 'HUM', 'NUE', 'DTE', 'TSCO', 'FANG', 'HPQ', 'TPL', 'IP', 'GDDY', 'FITB', 'AWK', 'UAL', 'PPG', 'BRO', 'AEE', 'DOV', 'LEN', 'CDW', 'FTV', 'PPL', 'VLTO', 'CPAY', 'DRI', 'ATO', 'TYL', 'HSY', 'SBAC', 'CCL', 'SYF', 'IQV', 'EXE', 'CNP', 'KHC', 'ADM', 'EQR', 'HPE', 'HBAN', 'MTD', 'SW', 'TDY', 'CINF', 'CHD', 'SMCI', 'PODD', 'VRSN', 'STE', 'LYV', 'DVN', 'CBOE', 'ES', 'STX', 'K', 'EIX', 'TROW', 'NVR', 'WRB', 'DOW', 'WSM', 'FE', 'AMCR', 'NTRS', 'EXPE', 'HUBB', 'FSLR', 'PHM', 'PTC', 'GPN', 'WBD', 'CMS', 'WAT', 'RF', 'LH', 'NTAP', 'LDOS', 'DECK', 'DG', 'DGX', 'IFF', 'INVH', 'ULTA', 'ON', 'ZBH', 'LII', 'STLD', 'WY', 'LUV', 'MKC', 'MAA', 'HAL', 'JBL', 'CTRA', 'CFG', 'ESS', 'NI', 'BIIB', 'FDS', 'DLTR', 'TRMB', 'MOH', 'GPC', 'TPR', 'PKG', 'SNA', 'PFG', 'WDC', 'DPZ', 'KEY', 'CLX', 'FFIV', 'PNR', 'EXPD', 'COO', 'APTV', 'BALL', 'LNT', 'GEN', 'TSN', 'BAX', 'ROL', 'J', 'L', 'ZBRA', 'LYB', 'EL', 'WST', 'CF', 'OMC', 'EVRG', 'EG', 'LVS', 'AVY', 'BBY', 'IEX', 'KIM', 'MAS', 'BLDR', 'TER', 'TXT', 'ALGN', 'JKHY', 'HOLX', 'UDR', 'CPT', 'ALLE', 'PAYC', 'JNPR', 'FOXA', 'DOC', 'REG', 'JBHT', 'SJM', 'POOL', 'AKAM', 'SWKS', 'CHRW', 'SWK', 'RVTY', 'UHS', 'BG', 'ARE', 'NDSN', 'LKQ', 'HST', 'RL', 'TKO', 'NWSA', 'CAG', 'MOS', 'KMX', 'EPAM', 'VTRS', 'AIZ', 'PNW', 'GL', 'SOLV', 'INCY', 'BXP', 'TAP', 'EMN', 'DAY', 'IPG', 'ERIE', 'AES', 'HII', 'HSIC', 'WYNN', 'NCLH', 'HAS', 'HRL', 'MRNA', 'AOS', 'WBA', 'MKTX', 'MGM', 'GNRC', 'TECH', 'MTCH', 'LW', 'FRT', 'ALB', 'CRL', 'PARA', 'IVZ', 'BEN', 'CPB', 'APA', 'FOX', 'CZR', 'ENPH', 'BF.B']

    
    # Dictionary to store DataFrames
    stats_data = {}
    
    # Create directory structure if it doesn't exist
    save_dir = "Datasets/Statistics/"
    os.makedirs(save_dir, exist_ok=True)
    
    for ticker in tickers:
        # Try to get the data
        stats_data[ticker] = get_statistics_data(ticker)
        
        # Add random delay between requests to avoid being flagged as a bot
        delay = random.uniform(2, 5)
        time.sleep(delay)
        
        # Save to csv in the specified folder structure
        if stats_data[ticker] is not None and not stats_data[ticker].empty:
            file_path = f"{save_dir}{ticker}_statistics.csv"
            stats_data[ticker].to_csv(file_path, index=False)
            
        else:
            print(f"No data saved for {ticker}")
    print(f"Successfully Fetched Statistical Data for All Tickers!")
    print(f"Data collection complete, files saved to 'Datasets/Statistics/' folder.")