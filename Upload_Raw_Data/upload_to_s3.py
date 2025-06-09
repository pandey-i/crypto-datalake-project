import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
import os

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket
    file_name: Name of the file to upload
    bucket: Bucket to upload to
    object_name: S3 object name. If not specified then file_name is used
    """
    # If S3 object_name is not specified, use just the filename without the path
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Verify file exists
    if not os.path.exists(file_name):
        print(f"Error: File {file_name} does not exist")
        return False

    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(file_name, bucket, object_name)
        print(f"Successfully uploaded {file_name} to {bucket}/{object_name}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
        return False
    except NoCredentialsError:
        print("AWS credentials not available. Please configure your AWS credentials.")
        return False
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

# Example usage
if __name__ == "__main__":
    filename = "crypto_prices_2025_06_09_10.csv"
    file_path = "C:/Users/Aman/Desktop/crypto-datalake-project/crypto_prices_2025_06_09_10.csv"
    bucket_name = "crypto-datalake-01"
    s3_prefix = 'hourly/' # folder inside the bucket
    s3_key = f"{s3_prefix}{filename}"
    upload_to_s3(file_path, bucket_name)
    