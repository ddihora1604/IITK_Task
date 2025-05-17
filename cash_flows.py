import yfinance as yf
import os
import time
import random

# Define the ticker symbols (replace with your 390 tickers)
tickers = ['MSFT', 'NVDA', 'AAPL', 'GOOGL', 'META', 'AMZN', 'META', 'AVGO', 'TSLA', 'GOOGL', 'BRK.B', 'GOOG', 'JPM', 'V', 'LLY', 'NFLX', 'XOM', 'MA', 'COST', 'WMT', 'PG', 'HD', 'JNJ', 'ABBV', 'BAC', 'UNH', 'CRM', 'KO', 'PLTR', 'ORCL', 'PM', 'WFC', 'CSCO', 'GE', 'IBM', 'CVX', 'ABT', 'MCD', 'LIN', 'NOW', 'DIS', 'ISRG', 'ACN', 'GS', 'AMD', 'T', 'UBER', 'MRK', 'INTU', 'VZ', 'PEP', 'RTX', 'ADBE', 'BKNG', 'TXN', 'QCOM', 'CAT', 'AXP', 'PGR', 'MS', 'SPGI', 'TMO', 'BA', 'BSX', 'SCHW', 'NEE', 'TJX', 'AMAT', 'C', 'HON', 'AMGN', 'BLK', 'UNP', 'SYK', 'CMCSA', 'ETN', 'LOW', 'PANW', 'DE', 'ADP', 'PFE', 'GILD', 'DHR', 'GEV', 'COP', 'TMUS', 'ADI', 'MMC', 'LRCX', 'BX', 'VRTX', 'MDT', 'FI', 'CRWD', 'KLAC', 'MU', 'CB', 'APH', 'ANET', 'PLD', 'ICE', 'SBUX', 'CME', 'AMT', 'MO', 'TT', 'LMT', 'INTC', 'SO', 'CEG', 'BMY', 'CDNS', 'WELL', 'DUK', 'KKR', 'ELV', 'PH', 'MCK', 'AJG', 'EQIX', 'CI', 'MDLZ', 'SHW', 'WM', 'MMM', 'SNPS', 'TDG', 'AON', 'ORLY', 'CVS', 'COF', 'MCO', 'CTAS', 'UPS', 'NKE', 'PYPL', 'CL', 'WMB', 'CMG', 'PNC', 'MSI', 'ZTS', 'USB', 'GD', 'EMR', 'DASH', 'HCA', 'FTNT', 'ITW', 'EOG', 'HWM', 'APO', 'JCI', 'ADSK', 'BK', 'ECL', 'MAR', 'RCL', 'NOC', 'AZO', 'HLT', 'ROP', 'APD', 'REGN', 'CSX', 'TRV', 'ABNB', 'CARR', 'WDAY', 'FCX', 'NEM', 'CPRT', 'NSC', 'TFC', 'OKE', 'NXPI', 'ALL', 'KMI', 'AXON', 'VST', 'AEP', 'DLR', 'FICO', 'MPC', 'PSX', 'AFL', 'FDX', 'PWR', 'SLB', 'DFS', 'AMP', 'GM', 'ROST', 'PCAR', 'SPG', 'BDX', 'PAYX', 'AIG', 'RSG', 'COR', 'TEL', 'O', 'GWW', 'SRE', 'PSA', 'URI', 'CTVA', 'MET', 'FAST', 'CMI', 'D', 'EW', 'KVUE', 'KDP', 'KMB', 'MSCI', 'KR', 'TGT', 'MNST', 'CCI', 'VRSK', 'VLO', 'EXC', 'IDXX', 'AME', 'F', 'LHX', 'FIS', 'YUM', 'CHTR', 'CTSH', 'XEL', 'PEG', 'CBRE', 'OTIS', 'PRU', 'TTWO', 'BKR', 'HES', 'PCG', 'TRGP', 'RMD', 'HIG', 'GLW', 'CAH', 'LULU', 'VMC', 'MPWR', 'EA', 'WAB', 'SYY', 'ROK', 'DELL', 'DHI', 'ETR', 'ED', 'IT', 'ACGL', 'DXCM', 'EFX', 'EQT', 'NDAQ', 'IR', 'GEHC', 'EBAY', 'MLM', 'VICI', 'MCHP', 'DAL', 'WEC', 'ODFL', 'CSGP', 'A', 'NRG', 'EXR', 'GRMN', 'MTB', 'XYL', 'ANSS', 'WTW', 'OXY', 'CNC', 'GIS', 'STZ', 'AVB', 'IRM', 'DD', 'KEYS', 'STT', 'VTR', 'RJF', 'BR', 'HUM', 'NUE', 'DTE', 'TSCO', 'FANG', 'HPQ', 'TPL', 'IP', 'GDDY', 'FITB', 'AWK', 'UAL', 'PPG', 'BRO', 'AEE', 'DOV', 'LEN', 'CDW', 'FTV', 'PPL', 'VLTO', 'CPAY', 'DRI', 'ATO', 'TYL', 'HSY', 'SBAC', 'CCL', 'SYF', 'IQV', 'EXE', 'CNP', 'KHC', 'ADM', 'EQR', 'HPE', 'HBAN', 'MTD', 'SW', 'TDY', 'CINF', 'CHD', 'SMCI', 'PODD', 'VRSN', 'STE', 'LYV', 'DVN', 'CBOE', 'ES', 'STX', 'K', 'EIX', 'TROW', 'NVR', 'WRB', 'DOW', 'WSM', 'FE', 'AMCR', 'NTRS', 'EXPE', 'HUBB', 'FSLR', 'PHM', 'PTC', 'GPN', 'WBD', 'CMS', 'WAT', 'RF', 'LH', 'NTAP', 'LDOS', 'DECK', 'DG', 'DGX', 'IFF', 'INVH', 'ULTA', 'ON', 'ZBH', 'LII', 'STLD', 'WY', 'LUV', 'MKC', 'MAA', 'HAL', 'JBL', 'CTRA', 'CFG', 'ESS', 'NI', 'BIIB', 'FDS', 'DLTR', 'TRMB', 'MOH', 'GPC', 'TPR', 'PKG', 'SNA', 'PFG', 'WDC', 'DPZ', 'KEY', 'CLX', 'FFIV', 'PNR', 'EXPD', 'COO', 'APTV', 'BALL', 'LNT', 'GEN', 'TSN', 'BAX', 'ROL', 'J', 'L', 'ZBRA', 'LYB', 'EL', 'WST', 'CF', 'OMC', 'EVRG', 'EG', 'LVS', 'AVY', 'BBY', 'IEX', 'KIM', 'MAS', 'BLDR', 'TER', 'TXT', 'ALGN', 'JKHY', 'HOLX', 'UDR', 'CPT', 'ALLE', 'PAYC', 'JNPR', 'FOXA', 'DOC', 'REG', 'JBHT', 'SJM', 'POOL', 'AKAM', 'SWKS', 'CHRW', 'SWK', 'RVTY', 'UHS', 'BG', 'ARE', 'NDSN', 'LKQ', 'HST', 'RL', 'TKO', 'NWSA', 'CAG', 'MOS', 'KMX', 'EPAM', 'VTRS', 'AIZ', 'PNW', 'GL', 'SOLV', 'INCY', 'BXP', 'TAP', 'EMN', 'DAY', 'IPG', 'ERIE', 'AES', 'HII', 'HSIC', 'WYNN', 'NCLH', 'HAS', 'HRL', 'MRNA', 'AOS', 'WBA', 'MKTX', 'MGM', 'GNRC', 'TECH', 'MTCH', 'LW', 'FRT', 'ALB', 'CRL', 'PARA', 'IVZ', 'BEN', 'CPB', 'APA', 'FOX', 'CZR', 'ENPH', 'BF.B']
 # Your 390 tickers would go here instead

# Create directory structure if it doesn't exist
output_dir = os.path.join("Datasets", "Cash Flow")
os.makedirs(output_dir, exist_ok=True)

# Process each ticker with error handling
success_count = 0
error_count = 0
error_tickers = []

for i, ticker_name in enumerate(tickers):
    try:
        # Fetch financial data
        ticker = yf.Ticker(ticker_name)
        cash_flow = ticker.cashflow
        
        # Export to CSV
        output_file = os.path.join(output_dir, f"{ticker_name}_cash_flow.csv")
        cash_flow.to_csv(output_file)
        
        success_count += 1
        
        # Add a small random delay between requests to avoid rate limiting
        time.sleep(random.uniform(0.5, 1.5))
        
    except Exception as e:
        print(f"Error processing {ticker_name}: {str(e)}")
        error_count += 1
        error_tickers.append(ticker_name)
        # Continue with the next ticker without stopping the entire process
        continue

print(f"Successfully fetched Cash Flow data for {success_count} Tickers")
if error_count > 0:
    print(f"Failed to fetch data for {error_count} tickers: {', '.join(error_tickers)}")
print(f"Data collection complete, files saved to 'Datasets/Cash Flow/' folder.")