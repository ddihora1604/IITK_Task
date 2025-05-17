# Financial Data Analysis and ESG Metrics Project

## Overview
This project is a comprehensive financial data analysis system that collects, processes, and analyzes data from approximately 500 tickers in the S&P Global Index. It provides detailed financial information, ESG metrics, and various financial statements for comprehensive market analysis.

## Key Features

### 1. Historical Data Analysis
- Historical price data collection and analysis
- Time-series data processing
- Market trend analysis capabilities

### 2. ESG (Environmental, Social, Governance) Data
- Comprehensive ESG metrics collection
- Environmental impact analysis
- Social responsibility metrics
- Corporate governance evaluation

### 3. Company Information
- Detailed company summaries
- Key business metrics
- Company overview and description

### 4. Financial Statements
- Income Statement analysis
- Balance Sheet data
- Cash Flow statement analysis
- Key financial ratios and metrics

### 5. Statistical Analysis
- Key statistics and metrics
- Market performance indicators
- Financial health indicators

## Technical Architecture

### Core Components
1. **Data Collection Module**
   - `historical_data.py`: Historical price data collection
   - `esg_data.py`: ESG metrics collection
   - `company_summary.py`: Company information gathering
   - `statistical_data.py`: Statistical data processing

2. **Financial Analysis Module**
   - `income_statement.py`: Income statement analysis
   - `balance_sheet.py`: Balance sheet analysis
   - `cash_flows.py`: Cash flow analysis
   - `stocks.py`: Stock-specific data processing

3. **Bot Management**
   - `bot.py`: Handles web scraping and API interactions

## Data Collection and Processing

### Data Sources
- Primary Data Source: Yahoo Finance
- Secondary Data Source: Web scraping for additional metrics
- S&P Global Index tickers (approximately 500 companies)

### Rate Limiting and Bot Handling
- Custom user-agent headers implementation
- Rate limiting management
- Bot detection avoidance techniques
- Request throttling and delay implementation

### Data Storage
- Processed data stored in the `Data/` directory
- Raw datasets maintained in `Datasets/` directory
- ESG-specific data in `files4esg/` directory

## Data Pipeline
1. Data Collection
   - Fetch data from Yahoo Finance
   - Web scraping for additional metrics
   - ESG data collection

2. Data Processing
   - Clean and validate data
   - Transform into required formats
   - Calculate derived metrics

3. Data Storage
   - Store processed data
   - Maintain data versioning
   - Ensure data integrity

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project
1. Ensure all dependencies are installed
2. Run the main data collection script:
   ```bash
   python historical_data.py
   ```

## Project Structure
```
├── Data/                  # Processed data storage
├── Datasets/             # Raw datasets
├── files4esg/           # ESG-specific data files
├── balance_sheet.py     # Balance sheet analysis
├── cash_flows.py        # Cash flow analysis
├── company_summary.py   # Company information
├── esg_data.py         # ESG metrics collection
├── historical_data.py   # Historical data processing
├── income_statement.py  # Income statement analysis
├── statistical_data.py  # Statistical analysis
├── stocks.py           # Stock data processing
├── bot.py             # Web scraping and API handling
└── requirements.txt    # Project dependencies
```

## Acknowledgments
- Yahoo Finance for market data
- S&P Global for index data
- Contributors and maintainers of the project 