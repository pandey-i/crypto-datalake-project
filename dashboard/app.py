import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Crypto Price Dashboard",
    page_icon="🪙",
    layout="wide"
)

# Title
st.title("🪙 Real-Time Crypto Prices Dashboard")

# Snowflake connection
@st.cache_resource
def init_connection():
    try:
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        return None

# Query function with caching
@st.cache_data(ttl=3600)
def load_data(hours=24):
    try:
        query = f"""
        SELECT 
            COIN as coin,
            PRICE_USD as price_usd,
            TIMESTAMP as timestamp
        FROM crypto_prices
        WHERE timestamp > DATEADD(hour, -{hours}, CURRENT_TIMESTAMP())
        ORDER BY timestamp DESC
        """
        
        # Use cursor to fetch data
        conn = init_connection()
        if conn is None:
            return pd.DataFrame(columns=['coin', 'price_usd', 'timestamp'])
            
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Get column names from cursor description
        columns = [col[0].lower() for col in cursor.description]
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        # Debug information
        st.sidebar.write("Available columns:", df.columns.tolist())
        st.sidebar.write("Sample data:", df.head())
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(columns=['coin', 'price_usd', 'timestamp'])

# Sidebar controls
st.sidebar.header("Controls")

# Time range selector
time_ranges = {
    "Last 24 Hours": 24,
    "Last 48 Hours": 48,
    "Last 72 Hours": 72,
    "Last Week": 168
}
selected_range = st.sidebar.selectbox(
    "Select Time Range",
    list(time_ranges.keys())
)

# Load data
df = load_data(time_ranges[selected_range])

# Check if we have any data
if df.empty:
    st.warning("No data available. Please check your database connection and data ingestion pipeline.")
    st.stop()

# Check if required columns exist
required_columns = ["coin", "price_usd", "timestamp"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns in database: {', '.join(missing_columns)}")
    st.stop()

# Coin selector
coins = sorted(df["coin"].unique())
selected_coins = st.sidebar.multiselect(
    "Select Coins",
    coins,
    default=coins[:5] if len(coins) > 0 else []  # Default to first 5 coins if available
)

# Main content
if not selected_coins:
    st.warning("Please select at least one coin from the sidebar.")
else:
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Price Charts", "Data Table"])
    
    with tab1:
        # Price charts
        for coin in selected_coins:
            filtered_df = df[df["coin"] == coin]
            
            fig = px.line(
                filtered_df,
                x="timestamp",
                y="price_usd",
                title=f"{coin} Price Over Time",
                labels={"price_usd": "Price (USD)", "timestamp": "Time"}
            )
            
            # Add hover data
            fig.update_traces(
                hovertemplate="<br>".join([
                    "Time: %{x}",
                    "Price: $%{y:,.2f}",
                    "<extra></extra>"
                ])
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Data table
        st.subheader("Latest Prices")
        
        # Filter for selected coins
        filtered_df = df[df["coin"].isin(selected_coins)]
        
        # Pivot the data for better table view
        pivot_df = filtered_df.pivot(
            index="timestamp",
            columns="coin",
            values="price_usd"
        ).reset_index()
        
        # Format the timestamp
        pivot_df["timestamp"] = pivot_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
        
        # Display the table
        st.dataframe(
            pivot_df,
            use_container_width=True,
            hide_index=True
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Data last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")) 