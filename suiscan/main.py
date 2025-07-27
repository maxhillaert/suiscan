"""
Sui Explorer - Main Script (Milestone 1)

This script demonstrates fetching and displaying Sui blockchain data from BigQuery.
Run this in VSCode's interactive mode using Ctrl+Enter on each cell.

Prerequisites:
1. Set up BigQuery credentials: config/bigquery_credentials.json
2. Set environment variable: GOOGLE_APPLICATION_CREDENTIALS=config/bigquery_credentials.json
3. Install dependencies: google-cloud-bigquery, polars, pyarrow
"""
# %%
import os
from pathlib import Path
import polars as pl
from suiscan.data.fetcher import create_fetcher

# %%
# Configuration and Setup
print("🚀 Sui Explorer - Milestone 1")
print("=" * 50)

# Check if credentials are set up
script_dir = Path(__file__).parent.parent  # Go up from suiscan/main.py to root
credentials_path = script_dir / "config" / "bigquery_credentials.json"

if not credentials_path.exists():
    print("⚠️  Warning: BigQuery credentials not found!")
    print("📁 Please place your service account key at: config/bigquery_credentials.json")
    print("🔧 And set: export GOOGLE_APPLICATION_CREDENTIALS='config/bigquery_credentials.json'")
else:
    print("✅ BigQuery credentials found")

# Set environment variable if credentials file exists
if credentials_path.exists():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path.absolute())

print("\n🔗 Connecting to Sui BigQuery dataset...")

# %%
# Initialize the data fetcher
try:
    fetcher = create_fetcher()
    print("✅ Successfully connected to BigQuery!")
    print(f"📊 Dataset: {fetcher.dataset_id}")
except Exception as e:
    print(f"❌ Failed to connect to BigQuery: {e}")
    print("🔧 Please check your credentials and internet connection")

# %%
# Fetch recent transactions
print("\n📈 Fetching Recent Transactions")
print("-" * 30)

try:
    # Get last 7 days of transactions (limited to 20 for quick display)
    recent_txns = fetcher.get_recent_transactions(days=7, limit=20)
    
    print("\n📋 Recent Transactions:")
    print(recent_txns.select([
        "transaction_digest",
        "timestamp", 
        "sender",
        "gas_used",
        "success",
        "effects_status"
    ]))
    
    print(f"\n📊 Transaction Statistics:")
    print(f"   Total fetched: {len(recent_txns)}")
    print(f"   Successful: {recent_txns.filter(pl.col('success') == True).shape[0]}")
    print(f"   Failed: {recent_txns.filter(pl.col('success') == False).shape[0]}")
    
except Exception as e:
    print(f"❌ Error fetching transactions: {e}")

# %%
# Fetch wallet balances
print("\n💰 Fetching Top Wallet Balances")
print("-" * 32)

try:
    # Get top 10 wallets by SUI balance
    top_wallets = fetcher.get_wallet_balances(limit=10)
    
    print("\n💎 Top Wallets by SUI Balance:")
    print(top_wallets.select([
        "owner",
        "balance_sui",
        "coin_type"
    ]).head(10))
    
    total_sui = top_wallets["balance_sui"].sum()
    print(f"\n📊 Top 10 Wallets Total: {total_sui:,.2f} SUI")
    
except Exception as e:
    print(f"❌ Error fetching wallet balances: {e}")

# %%
# Get transaction summary
print("\n📊 Transaction Activity Summary")
print("-" * 33)

try:
    # Get 7-day activity summary
    summary = fetcher.get_transaction_summary(days=7)
    
    print("\n📈 Daily Transaction Summary:")
    print(summary.select([
        "date",
        "transaction_count",
        "unique_senders", 
        "successful_txns",
        "failed_txns",
        "success_rate_pct"
    ]))
    
    # Calculate totals
    total_txns = summary["transaction_count"].sum()
    avg_daily_txns = summary["transaction_count"].mean()
    overall_success_rate = (summary["successful_txns"].sum() / total_txns * 100)
    
    print(f"\n📊 Summary Statistics:")
    print(f"   Total transactions (7 days): {total_txns:,}")
    print(f"   Average daily transactions: {avg_daily_txns:,.0f}")
    print(f"   Overall success rate: {overall_success_rate:.2f}%")
    
except Exception as e:
    print(f"❌ Error fetching transaction summary: {e}")

# %%
# Custom query example
print("\n🔍 Custom Analysis Example")
print("-" * 27)

try:
    # Example: Analyze gas usage patterns
    gas_analysis = recent_txns.select([
        pl.col("gas_used").cast(pl.Int64).alias("gas_used_int"),
        "success"
    ]).with_columns([
        pl.when(pl.col("gas_used_int") < 1000000)
        .then(pl.lit("Low"))
        .when(pl.col("gas_used_int") < 5000000)
        .then(pl.lit("Medium"))
        .otherwise(pl.lit("High"))
        .alias("gas_category")
    ])
    
    gas_summary = gas_analysis.group_by("gas_category").agg([
        pl.count().alias("count"),
        pl.col("gas_used_int").mean().alias("avg_gas"),
        pl.col("success").mean().alias("success_rate")
    ])
    
    print("\n⛽ Gas Usage Analysis:")
    print(gas_summary)
    
except Exception as e:
    print(f"❌ Error in custom analysis: {e}")

# %%
# Interactive exploration prompt
print("\n🔧 Ready for Interactive Exploration!")
print("=" * 42)
print("""
💡 Try these commands in the next cells:

# Get specific wallet balance
specific_addresses = ["0x123..."]  # Replace with real address
balances = fetcher.get_wallet_balances(addresses=specific_addresses)

# Custom time range
recent_hour = fetcher.get_recent_transactions(days=0.04, limit=50)  # ~1 hour

# Explore the data
print(recent_txns.columns)
print(recent_txns.dtypes)
print(recent_txns.describe())

# Filter and analyze
high_gas_txns = recent_txns.filter(pl.col("gas_used").cast(pl.Int64) > 1000000)
failed_txns = recent_txns.filter(pl.col("success") == False)
""")

print("✨ Happy exploring! Run cells above or create your own queries.")

# %% 