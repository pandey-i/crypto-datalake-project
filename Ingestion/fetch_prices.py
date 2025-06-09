import requests
import pandas as pd
from datetime import datetime, timedelta
import time

def get_all_coin_ids():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        coins = response.json()
        return [coin['id'] for coin in coins]
    else:
        raise Exception(f"Failed to fetch coin list: {response.status_code} - {response.text}")
    
def fetch_price_data(coin_ids):
    all_data = []
    chunk_size = 250
    
    for i in range(0, len(coin_ids), chunk_size):
        chunk = coin_ids[i:i+chunk_size]
        ids_str = ','.join(chunk)
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': ids_str,
            'vs_currencies': 'usd'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                chunk_df = pd.DataFrame(data).T
                chunk_df.columns = ['price_usd']
                chunk_df['coin'] = chunk_df.index
                chunk_df['timestamp'] = datetime.utcnow()
                all_data.append(chunk_df.reset_index(drop=True))
                print(f"Successfully processed {len(data)} coins in current chunk")
            else:
                print(f"No data found for chunk {chunk}")
        else:
            print(f"Failed to fetch chunk: {response.status_code} - {response.text}")
        time.sleep(1)  # Rate limiting
    
    if not all_data:
        raise Exception("No data was collected")
    
    full_df = pd.concat(all_data, ignore_index=True)
    return full_df

if __name__ == "__main__":
    try:
        print("Fetching list of all supported crypto coin ids...")
        coin_ids = get_all_coin_ids()
        print(f"Found {len(coin_ids)} supported crypto coin ids.")
        
        print("Fetching price data for all coins...")
        price_data = fetch_price_data(coin_ids)
        print(f"Successfully fetched price data for {len(price_data)} coins.")
        
        print("Saving price data to CSV file...")
        timestamp_str = datetime.utcnow().strftime('%Y_%m_%d_%H')
        filename = f"crypto_prices_{timestamp_str}.csv"
        price_data.to_csv(filename, index=False)
        print(f"📁 Price data saved to {filename}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    
        
        
            
