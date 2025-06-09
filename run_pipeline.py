import os
import sys
from datetime import datetime
from Ingestion.fetch_prices import get_all_coin_ids, fetch_price_data
from Upload_Raw_Data.upload_to_s3 import upload_to_s3

def run_pipeline():
    try:
        # Step 1: Fetch crypto prices
        print("Step 1: Fetching crypto prices...")
        coin_ids = get_all_coin_ids()
        print(f"Found {len(coin_ids)} supported crypto coin ids.")
        
        price_data = fetch_price_data(coin_ids)
        print(f"Successfully fetched price data for {len(price_data)} coins.")
        
        # Step 2: Save to CSV
        print("\nStep 2: Saving to CSV...")
        timestamp_str = datetime.utcnow().strftime('%Y_%m_%d_%H')
        filename = f"crypto_prices_{timestamp_str}.csv"
        price_data.to_csv(filename, index=False)
        print(f"📁 Price data saved to {filename}")
        
        # Step 3: Upload to S3
        print("\nStep 3: Uploading to S3...")
        bucket_name = "crypto-datalake-01"
        s3_prefix = 'hourly/'
        s3_key = f"{s3_prefix}{filename}"
        
        if upload_to_s3(filename, bucket_name, s3_key):
            print(f"✅ Successfully uploaded to {bucket_name}/{s3_key}")
            
            # Clean up local file
            os.remove(filename)
            print(f"🧹 Cleaned up local file: {filename}")
        else:
            print("❌ Failed to upload to S3")
            sys.exit(1)
            
        print("\n✨ Pipeline completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in pipeline: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline() 