import argparse
import requests
import json
import os
import logging
import sys
from datetime import datetime

# --- MODIFIED: Use the script's directory as the project root ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# --- MODIFIED: The API server will be reachable via its service name in Docker ---
API_BASE_URL = "http://api_server/"
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
LOG_FILE = os.path.join(PROJECT_ROOT, 'error.log')


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_FILE,
    filemode='a'
)

console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def get_exchange_rate(api_key, from_currency, to_currency, date_str):
    """
    Fetches the exchange rate from the API.

    Args:
        api_key (str): The API key for authentication.
        from_currency (str): The currency to convert from (e.g., USD).
        to_currency (str): The currency to convert to (e.g., EUR).
        date_str (str): The date for the exchange rate in YYYY-MM-DD format.

    Returns:
        dict: The exchange rate data if successful, None otherwise.
    """
    params = {
        'from': from_currency,
        'to': to_currency,
        'date': date_str
    }
    # In docker-compose, the API service is on port 80
    url = f"{API_BASE_URL}?from={from_currency}&to={to_currency}&date={date_str}"
    
    payload = {
        'key': api_key
    }
    try:
        # The request now uses the full URL in the post method
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        if data.get("error"):
            error_msg = f"API Error: {data['error']}"
            logging.error(error_msg)
            return None
        
        return data.get("data")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response from API. Response text: " + response.text)
        return None

def save_data_to_json(data, from_currency, to_currency, date_str):
    """
    Saves the exchange rate data to a JSON file in the 'data' directory.

    Args:
        data (dict): The data to save.
        from_currency (str): The currency converted from.
        to_currency (str): The currency converted to.
        date_str (str): The date of the exchange rate.
    """
    try:
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Created directory: {DATA_DIR}")
            
        filename = f"{from_currency.upper()}_{to_currency.upper()}_{date_str}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved data to {filepath}")

    except OSError as e:
        logging.error(f"Failed to save data file: {e}")

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(description="Get currency exchange rates from a web API.")
    parser.add_argument("from_currency", type=str, help="The currency to convert from (e.g., USD).")
    parser.add_argument("to_currency", type=str, help="The currency to convert to (e.g., EUR).")
    parser.add_argument("date", type=str, help="The date for the exchange rate in YYYY-MM-DD format.")
    
    args = parser.parse_args()
    
    # Validate date format before making an API call
    try:
        datetime.strptime(args.date, '%Y-%m-%d')
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        sys.exit(1)

    api_key = os.getenv("API_KEY")
    if not api_key:
        logging.error("API_KEY environment variable not set. Please set it before running the script.")
        sys.exit(1)

    exchange_data = get_exchange_rate(api_key, args.from_currency, args.to_currency, args.date)
    
    if exchange_data:
        save_data_to_json(exchange_data, args.from_currency, args.to_currency, args.date)
    else:
        # Exit with a non-zero status code to indicate failure
        sys.exit(1)

if __name__ == "__main__":
    main()