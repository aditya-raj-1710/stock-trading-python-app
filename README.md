# Stock Ticker Data Fetcher

A Python application that fetches stock ticker data from the Polygon.io API and exports it to a CSV file. This tool retrieves comprehensive information about active US stock tickers including company names, market details, and financial identifiers. The application supports both one-time data fetching and automated scheduled updates.

## Project Structure

- `script.py` - Main ticker fetching script (can be run standalone or imported)
- `schedule_ticker_script.py` - Automated scheduler that runs the ticker fetcher every minute
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (API keys) - **not tracked in git**
- `tickers.csv` - Output file containing fetched ticker data
- `README.md` - This documentation file

## Setup Instructions

### Prerequisites
- Python 3.8 or higher installed on your system
- pip (Python package installer)
- Polygon.io API key (free tier available at [polygon.io](https://polygon.io))

### Virtual Environment Setup

#### 1. Create a Virtual Environment
```bash
# Navigate to the project directory
cd /path/to/stock-trading-python-app

# Create a virtual environment named 'pythonenv'
python3 -m venv pythonenv
```

#### 2. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source pythonenv/bin/activate
```

**On Windows:**
```bash
# Command Prompt
pythonenv\Scripts\activate

# PowerShell
pythonenv\Scripts\Activate.ps1
```

#### 3. Install Dependencies
```bash
# Make sure you're in the activated virtual environment
pip install -r requirements.txt
```

#### 4. Configure API Key
```bash
# Create a .env file in the project root
touch .env

# Add your Polygon.io API key to the .env file
echo "POLYGON_API_KEY=your_api_key_here" >> .env
```

#### 5. Verify Installation
```bash
# Check if packages are installed correctly
pip list
```

## Usage

The application provides two modes of operation:

### Option 1: One-Time Data Fetch

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source pythonenv/bin/activate
   ```

2. **Run the script once**:
   ```bash
   python script.py
   ```

### Option 2: Automated Scheduled Updates

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source pythonenv/bin/activate
   ```

2. **Run the scheduled script**:
   ```bash
   python schedule_ticker_script.py
   ```

### What the Application Does

- **One-time mode** (`script.py`): Fetches stock ticker data once and exits
- **Scheduled mode** (`schedule_ticker_script.py`): Continuously fetches ticker data every minute
- Fetches stock ticker data from Polygon.io API
- Displays progress information in the console
- Saves all ticker data to `tickers.csv` in the project root
- Includes a 20-second delay between API calls to respect rate limits

### Output

The script generates a CSV file (`tickers.csv`) containing:
- Ticker symbol
- Company name
- Market information
- Exchange details
- Financial identifiers (CIK, FIGI codes)
- Currency and locale information
- Last updated timestamp

### Deactivating the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```

### Important Notes

- Always activate the virtual environment before working on the project
- The virtual environment folder (`pythonenv/`) and `.env` file are already included in `.gitignore`
- Never commit the virtual environment folder or `.env` file to version control
- The script includes rate limiting (20-second delays) to respect Polygon.io API limits
- The free Polygon.io tier has rate limits; consider upgrading for higher throughput
- **Scheduled mode**: The `schedule_ticker_script.py` will run continuously until manually stopped (Ctrl+C)
- **Scheduled mode**: Runs every minute, which may exceed API rate limits on free tier
- If you need to recreate the environment, delete the `pythonenv/` folder and follow the setup steps again

### Troubleshooting

If you encounter issues:
1. Make sure Python 3.8+ is installed: `python3 --version`
2. Ensure pip is up to date: `pip install --upgrade pip`
3. If activation fails, try using the full path: `source ./pythonenv/bin/activate`
4. Verify your API key is correctly set in the `.env` file
5. Check your internet connection and Polygon.io API status
6. Ensure you have sufficient disk space for the CSV output file
7. If you get rate limit errors, the script already includes delays, but you may need to wait longer between runs
8. **For scheduled mode**: If you get frequent rate limit errors, consider modifying the schedule interval in `schedule_ticker_script.py`
9. **To stop scheduled mode**: Use Ctrl+C to terminate the scheduled script