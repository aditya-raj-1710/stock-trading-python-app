import os
from dotenv import load_dotenv
import requests
import time
import csv
import logging
import snowflake.connector
from datetime import datetime
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ticker_fetch.log'),
        logging.StreamHandler()
    ]
)

load_dotenv()

# API Configuration
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Snowflake Configuration
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "ny85162")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "STOCK_DATA")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
SNOWFLAKE_TABLE = os.getenv("SNOWFLAKE_TABLE", "TICKERS")

# API Configuration
LIMIT = 1000
TIME_DELAY = 20

def get_snowflake_connection():
    """Create and return a Snowflake database connection."""
    try:
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        logging.info(f"Successfully connected to Snowflake: {SNOWFLAKE_ACCOUNT}")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to Snowflake: {str(e)}")
        raise


def create_tickers_table(conn):
    """Create the tickers table if it doesn't exist."""
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {SNOWFLAKE_TABLE} (
        ticker VARCHAR(50),
        name VARCHAR(500),
        market VARCHAR(50),
        locale VARCHAR(10),
        primary_exchange VARCHAR(50),
        type VARCHAR(10),
        active BOOLEAN,
        currency_name VARCHAR(10),
        cik VARCHAR(20),
        composite_figi VARCHAR(50),
        share_class_figi VARCHAR(50),
        last_updated_utc TIMESTAMP_TZ,
        data_loaded_at TIMESTAMP_TZ DEFAULT CURRENT_TIMESTAMP(),
        batch_id VARCHAR(100)
    )
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        logging.info(f"Table {SNOWFLAKE_TABLE} created or verified successfully")
        cursor.close()
    except Exception as e:
        logging.error(f"Failed to create table {SNOWFLAKE_TABLE}: {str(e)}")
        raise


def insert_data_to_snowflake(tickers: List[Dict[str, Any]], batch_id: str) -> int:
    """Insert ticker data into Snowflake."""
    if not SNOWFLAKE_USER or not SNOWFLAKE_PASSWORD:
        logging.warning("Snowflake credentials not provided, skipping database insertion")
        return 0
    
    try:
        conn = get_snowflake_connection()
        create_tickers_table(conn)
        
        # Prepare data for insertion
        insert_sql = f"""
        INSERT INTO {SNOWFLAKE_TABLE} (
            ticker, name, market, locale, primary_exchange, type, 
            active, currency_name, cik, composite_figi, share_class_figi, 
            last_updated_utc, data_loaded_at, batch_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor = conn.cursor()
        
        # Insert data in batches
        batch_size = 1000
        total_inserted = 0
        current_time = datetime.now()
        
        for i in range(0, len(tickers), batch_size):
            batch_tickers = tickers[i:i + batch_size]
            
            batch_data = []
            for ticker in batch_tickers:
                batch_data.append((
                    ticker.get('ticker', ''),
                    ticker.get('name', ''),
                    ticker.get('market', ''),
                    ticker.get('locale', ''),
                    ticker.get('primary_exchange', ''),
                    ticker.get('type', ''),
                    ticker.get('active', False),
                    ticker.get('currency_name', ''),
                    ticker.get('cik', ''),
                    ticker.get('composite_figi', ''),
                    ticker.get('share_class_figi', ''),
                    ticker.get('last_updated_utc', None),
                    current_time,
                    batch_id
                ))
            
            cursor.executemany(insert_sql, batch_data)
            total_inserted += len(batch_data)
            logging.info(f"Inserted batch {i//batch_size + 1}: {len(batch_data)} records")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logging.info(f"Successfully inserted {total_inserted} ticker records to Snowflake")
        return total_inserted
        
    except Exception as e:
        logging.error(f"Failed to insert data to Snowflake: {str(e)}")
        raise


def get_tickers():
    """Fetch stock ticker data from Polygon.io API and save to CSV and Snowflake."""
    
    # Validate API key
    if not POLYGON_API_KEY:
        logging.error("POLYGON_API_KEY not found in environment variables")
        raise ValueError("API key is required but not provided")
    
    # Generate batch ID for tracking
    batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    logging.info("Starting ticker data collection from Polygon.io API")
    logging.info(f"Configuration: LIMIT={LIMIT}, TIME_DELAY={TIME_DELAY}s")
    logging.info(f"Batch ID: {batch_id}")
    
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    
    tickers = []
    page_count = 0
    total_tickers = 0

    is_data_present = True

    try:
        while is_data_present:
            page_count += 1
            logging.info(f"Fetching page {page_count} from Polygon.io API")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for API errors
            if 'status' in data and data['status'] != 'OK':
                logging.error(f"API returned error status: {data.get('status', 'Unknown')}")
                if 'message' in data:
                    logging.error(f"Error message: {data['message']}")
                raise requests.RequestException(f"API error: {data.get('message', 'Unknown error')}")
            
            # Process results
            if 'results' not in data:
                logging.warning("No 'results' field found in API response")
                break
                
            page_tickers = data['results']
            tickers.extend(page_tickers)
            total_tickers += len(page_tickers)
            
            logging.info(f"Page {page_count}: Retrieved {len(page_tickers)} tickers (Total: {total_tickers})")
            
            # Check for next page
            if 'next_url' in data:
                url = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
                logging.debug(f"Waiting {TIME_DELAY} seconds before next request (rate limiting)")
                time.sleep(TIME_DELAY)
            else:
                is_data_present = False
                logging.info("No more pages available")

    except requests.RequestException as e:
        logging.error(f"Network/API error occurred: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise

    logging.info(f"Data collection completed. Total tickers retrieved: {len(tickers)}")

    # Define CSV schema using example ticker structure
    example_ticker = {
        'ticker': 'ZWS', 
        'name': 'Zurn Elkay Water Solutions Corporation', 
        'market': 'stocks', 
        'locale': 'us', 
        'primary_exchange': 'XNYS', 
        'type': 'CS', 
        'active': True, 
        'currency_name': 'usd', 
        'cik': '0001439288', 
        'composite_figi': 'BBG000H8R0N8', 
        'share_class_figi': 'BBG001T36GB5', 
        'last_updated_utc': '2025-09-11T06:11:10.586204443Z'
    }

    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Write tickers to CSV with example_ticker schema
    fieldnames = list(example_ticker.keys())
    output_csv = 'output/tickers.csv'
    
    logging.info(f"Writing {len(tickers)} tickers to CSV file: {output_csv}")
    
    try:
        with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for t in tickers:                       
                row = {key: t.get(key, '') for key in fieldnames}
                writer.writerow(row)
        
        logging.info(f"Successfully wrote {len(tickers)} rows to {output_csv}")
        
        # Log file size for monitoring
        file_size = os.path.getsize(output_csv)
        logging.info(f"Output file size: {file_size:,} bytes")
        
    except Exception as e:
        logging.error(f"Failed to write CSV file: {str(e)}")
        raise
    
    # Insert data to Snowflake
    snowflake_records = 0
    try:
        snowflake_records = insert_data_to_snowflake(tickers, batch_id)
        logging.info(f"Snowflake insertion completed: {snowflake_records} records")
    except Exception as e:
        logging.error(f"Snowflake insertion failed: {str(e)}")
        # Continue execution even if Snowflake fails
    
    logging.info("Ticker data collection and export completed successfully")
    return len(tickers), snowflake_records


if __name__ == "__main__":
    try:
        logging.info("=" * 60)
        logging.info("Stock Ticker Data Collection Started")
        logging.info(f"Timestamp: {datetime.now()}")
        logging.info("=" * 60)
        
        csv_count, snowflake_count = get_tickers()
        
        logging.info("=" * 60)
        logging.info(f"Process completed successfully!")
        logging.info(f"CSV records: {csv_count}")
        logging.info(f"Snowflake records: {snowflake_count}")
        logging.info(f"Completion time: {datetime.now()}")
        logging.info("=" * 60)
        
    except Exception as e:
        logging.error("=" * 60)
        logging.error(f"Process failed with error: {str(e)}")
        logging.error(f"Failure time: {datetime.now()}")
        logging.error("=" * 60)
        raise