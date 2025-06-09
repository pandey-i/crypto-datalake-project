# Crypto Data Lake Project

A real-time cryptocurrency price tracking and visualization system that collects data from CoinGecko, stores it in AWS S3, and visualizes it using Streamlit.

## Features

- Automated hourly data collection from CoinGecko API
- Data storage in AWS S3
- Real-time price visualization dashboard
- Historical price tracking
- Multiple cryptocurrency support

## Prerequisites

- Python 3.9+
- AWS Account with S3 access
- Snowflake Account
- CoinGecko API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-datalake-project.git
cd crypto-datalake-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

4. Set up Streamlit secrets:
Create a `.streamlit/secrets.toml` file with your Snowflake credentials:
```toml
[snowflake]
user = "your_username"
password = "your_password"
account = "your_account"
warehouse = "your_warehouse"
database = "your_database"
schema = "your_schema"
```

## Usage

1. Run the data collection pipeline:
```bash
python run_pipeline.py
```

2. Start the dashboard:
```bash
streamlit run dashboard/app.py
```

## Project Structure

```
crypto-datalake-project/
├── dashboard/
│   └── app.py              # Streamlit dashboard
├── Ingestion/
│   └── fetch_prices.py     # CoinGecko data collection
├── Upload_Raw_Data/
│   └── upload_to_s3.py     # S3 upload functionality
├── requirements.txt        # Python dependencies
└── run_pipeline.py        # Main pipeline script
```

## Automation

The data collection pipeline can be automated using Windows Task Scheduler:

1. Open Task Scheduler
2. Create a new Basic Task
3. Set the trigger to run hourly
4. Action: Start a program
5. Program/script: `python`
6. Add arguments: `run_pipeline.py`
7. Start in: `path_to_project`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 