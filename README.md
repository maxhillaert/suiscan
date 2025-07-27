# 🚀 Sui Explorer (Milestone 1)

A lightweight blockchain explorer tool for the Sui network that fetches and analyzes data from Google BigQuery's public Sui dataset.

## 🎯 Features (Milestone 1)

- **📊 Data Fetching**: Query recent transactions and wallet balances from BigQuery
- **⚡ Fast Processing**: Uses Polars DataFrames with Arrow for efficient data handling
- **🔧 Interactive Development**: Designed for VSCode's interactive mode with `#%%` cells
- **📈 Analytics**: Basic transaction summaries and gas usage analysis
- **🛡️ Modular Design**: Clean separation between data fetching and presentation

## 🏗️ Project Structure

```
sui-explorer/
├── src/
│   ├── main.py              # Main interactive script
│   └── data/
│       ├── __init__.py      # Package init
│       └── fetcher.py       # BigQuery data fetcher
├── config/
│   ├── README.md            # Configuration instructions
│   └── bigquery_credentials.json  # Your BigQuery service account key
├── pyproject.toml           # Project dependencies
├── .gitignore              # Git ignore patterns
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install UV (Package Manager)

First, install UV if you don't have it:

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: pip install uv
pip install uv
```

### 2. Set Up the Project

```bash
# Clone or create the project directory
cd sui-explorer

# Create virtual environment
uv venv .venv

# Activate virtual environment
# Windows (Git Bash)
source .venv/Scripts/activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
uv pip install google-cloud-bigquery polars pyarrow jupyter ipykernel
```

### 3. Configure BigQuery Access

1. **Set up Google Cloud credentials** (see detailed instructions in `config/README.md`):
   - Create a Google Cloud project
   - Enable BigQuery API
   - Create a service account with BigQuery User role
   - Download the JSON key file
   - Place it at `config/bigquery_credentials.json`

2. **Set environment variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="config/bigquery_credentials.json"
   ```

### 4. Run the Explorer

```bash
cd src
python main.py
```

## 💻 VSCode Interactive Mode

For the best experience, use VSCode's interactive mode:

1. **Install VSCode Extensions**:
   - Python
   - Jupyter

2. **Open the project** in VSCode

3. **Select Python interpreter** from your `.venv`

4. **Open `src/main.py`**

5. **Run cells interactively**:
   - Use `Ctrl+Enter` to run individual cells
   - Each `# %%` marks a new cell
   - Results appear in the interactive window

## 📊 What You Can Explore

### Recent Transactions
```python
# Fetch last 7 days of transactions
recent_txns = fetcher.get_recent_transactions(days=7, limit=100)
print(recent_txns)
```

### Wallet Balances  
```python
# Get top wallets by SUI balance
top_wallets = fetcher.get_wallet_balances(limit=50)
print(top_wallets)

# Query specific addresses
specific_balances = fetcher.get_wallet_balances(
    addresses=["0x123...", "0x456..."]
)
```

### Transaction Analytics
```python
# Daily activity summary
summary = fetcher.get_transaction_summary(days=7)
print(summary)

# Custom analysis with Polars
high_gas = recent_txns.filter(pl.col("gas_used").cast(pl.Int64) > 1000000)
```

## 🔧 Dependencies

- **google-cloud-bigquery**: BigQuery client for data fetching
- **polars**: Fast DataFrame processing (Rust-backed)
- **pyarrow**: Arrow format support for BigQuery → Polars conversion
- **jupyter** (optional): For enhanced interactive experience

## 📚 BigQuery Dataset

This project uses Google's public Sui dataset:
- **Dataset**: `bigquery-public-data.crypto_sui_mainnet_us`
- **Tables**: `transactions`, `objects`, and more
- **Free tier**: Up to 1TB queries per month

## 🛠️ Development Tips

1. **Start small**: Use `limit` parameters to avoid large queries during development
2. **Use time filters**: Recent data (last 7 days) loads faster
3. **Leverage Polars**: Fast filtering, grouping, and aggregation operations
4. **Interactive development**: Test queries in individual cells
5. **Check credentials**: The script will warn if BigQuery credentials are missing

## 🔜 Future Milestones

- **Milestone 2**: CLI interface with rich formatting
- **Milestone 3**: Web dashboard with real-time updates  
- **Milestone 4**: Advanced analytics and GPU acceleration
- **Milestone 5**: Custom indexing and caching

## 🤝 Contributing

This is the initial milestone focusing on basic data fetching and exploration. Future contributions will expand the analytics capabilities and user interface.

## 📄 License

MIT License - see LICENSE file for details.

---

**Happy exploring the Sui blockchain! 🌊** 