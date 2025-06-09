-- Create or replace the file format
CREATE OR REPLACE FILE FORMAT crypto_prices_format
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create or replace the stage
CREATE OR REPLACE STAGE crypto_prices_stage
    URL = 's3://crypto-datalake-01/hourly/'
    CREDENTIALS = (AWS_KEY_ID = '${AWS_KEY_ID}' AWS_SECRET_KEY = '${AWS_SECRET_KEY}')
    FILE_FORMAT = crypto_prices_format;

-- Create or replace the task
CREATE OR REPLACE TASK load_crypto_prices
    WAREHOUSE = COMPUTE_WH
    SCHEDULE = '1 HOUR'
AS
    COPY INTO crypto_prices (price_usd, coin, timestamp)
    FROM @crypto_prices_stage
    PATTERN = 'crypto_prices_.*\.csv'
    ON_ERROR = CONTINUE;

-- Enable the task
ALTER TASK load_crypto_prices RESUME; 