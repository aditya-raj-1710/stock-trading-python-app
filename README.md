# Stock Ticker Data Fetcher

A Python application that fetches stock ticker data from the Polygon.io API and exports it to a CSV file. This tool retrieves comprehensive information about active US stock tickers including company names, market details, and financial identifiers.

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

### Running the Application

1. **Activate the virtual environment** (if not already activated):
   ```bash
   source pythonenv/bin/activate
   ```

2. **Run the script**:
   ```bash
   python script.py
   ```

3. **The application will**:
   - Fetch stock ticker data from Polygon.io API
   - Display progress information in the console
   - Save all ticker data to `tickers.csv` in the project root
   - Include a 65-second delay between API calls to respect rate limits

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
- The script includes rate limiting (65-second delays) to respect Polygon.io API limits
- The free Polygon.io tier has rate limits; consider upgrading for higher throughput
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