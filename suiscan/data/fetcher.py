"""
Data fetcher module for Sui Explorer.

This module provides functions to fetch recent transactions and wallet balances
from Google BigQuery's public Sui dataset (bigquery-public-data.crypto_sui_mainnet_us).
Results are returned as Polars DataFrames for efficient processing.
"""

import os
from datetime import datetime, timedelta
from typing import Optional
import polars as pl
from google.cloud import bigquery


class SuiDataFetcher:
    """Fetcher class for Sui blockchain data from BigQuery."""
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize the SuiDataFetcher.
        
        Args:
            project_id: Google Cloud project ID. If None, uses default from credentials.
        """
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = "bigquery-public-data.crypto_sui_mainnet_us"
        
    def get_recent_transactions(self, days: int = 7, limit: int = 100) -> pl.DataFrame:
        """
        Fetch recent transactions from the Sui network.
        
        Args:
            days: Number of days back to fetch transactions (default: 7)
            limit: Maximum number of transactions to fetch (default: 100)
            
        Returns:
            Polars DataFrame with transaction data
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = int(cutoff_date.timestamp() * 1000)  # Convert to milliseconds
        
        query = f"""
        SELECT 
            transaction_digest,
            timestamp_ms,
            sender,
            gas_used,
            gas_price,
            success,
            effects_status,
            checkpoint_sequence_number
        FROM `{self.dataset_id}.transactions`
        WHERE timestamp_ms >= {cutoff_timestamp}
        ORDER BY timestamp_ms DESC
        LIMIT {limit}
        """
        
        print(f"Fetching recent transactions (last {days} days, limit {limit})...")
        query_job = self.client.query(query)
        
        # Convert to Arrow table first, then to Polars DataFrame
        arrow_table = query_job.to_arrow()
        df = pl.from_arrow(arrow_table)
        
        # Add readable timestamp column
        df = df.with_columns([
            pl.from_epoch(pl.col("timestamp_ms"), time_unit="ms").alias("timestamp")
        ])
        
        print(f"Fetched {len(df)} transactions")
        return df
    
    def get_wallet_balances(self, addresses: Optional[list] = None, limit: int = 50) -> pl.DataFrame:
        """
        Fetch wallet balances for specific addresses or top wallets.
        
        Args:
            addresses: List of wallet addresses to query. If None, fetches top wallets.
            limit: Maximum number of wallets to fetch (default: 50)
            
        Returns:
            Polars DataFrame with wallet balance data
        """
        if addresses:
            # Query specific addresses
            addresses_str = "', '".join(addresses)
            where_clause = f"WHERE owner IN ('{addresses_str}')"
        else:
            # Get top wallets by balance
            where_clause = "WHERE coin_type = '0x2::sui::SUI'"
        
        query = f"""
        SELECT 
            owner,
            coin_type,
            balance,
            object_id
        FROM `{self.dataset_id}.objects`
        {where_clause}
        ORDER BY CAST(balance AS INT64) DESC
        LIMIT {limit}
        """
        
        if addresses:
            print(f"Fetching balances for {len(addresses)} specific addresses...")
        else:
            print(f"Fetching top {limit} wallet balances...")
            
        query_job = self.client.query(query)
        
        # Convert to Arrow table first, then to Polars DataFrame
        arrow_table = query_job.to_arrow()
        df = pl.from_arrow(arrow_table)
        
        # Convert balance to numeric and add SUI amount (1 SUI = 1e9 units)
        df = df.with_columns([
            pl.col("balance").cast(pl.Int64).alias("balance_raw"),
            (pl.col("balance").cast(pl.Int64) / 1_000_000_000).alias("balance_sui")
        ])
        
        print(f"Fetched {len(df)} wallet balances")
        return df
    
    def get_transaction_summary(self, days: int = 7) -> pl.DataFrame:
        """
        Get a summary of transaction activity over the specified period.
        
        Args:
            days: Number of days back to analyze (default: 7)
            
        Returns:
            Polars DataFrame with transaction summary statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = int(cutoff_date.timestamp() * 1000)
        
        query = f"""
        SELECT 
            DATE(TIMESTAMP_MILLIS(timestamp_ms)) as date,
            COUNT(*) as transaction_count,
            COUNT(DISTINCT sender) as unique_senders,
            AVG(CAST(gas_used AS INT64)) as avg_gas_used,
            SUM(CASE WHEN success = true THEN 1 ELSE 0 END) as successful_txns,
            SUM(CASE WHEN success = false THEN 1 ELSE 0 END) as failed_txns
        FROM `{self.dataset_id}.transactions`
        WHERE timestamp_ms >= {cutoff_timestamp}
        GROUP BY DATE(TIMESTAMP_MILLIS(timestamp_ms))
        ORDER BY date DESC
        """
        
        print(f"Fetching transaction summary for last {days} days...")
        query_job = self.client.query(query)
        
        arrow_table = query_job.to_arrow()
        df = pl.from_arrow(arrow_table)
        
        # Add success rate calculation
        df = df.with_columns([
            (pl.col("successful_txns") / pl.col("transaction_count") * 100).alias("success_rate_pct")
        ])
        
        print(f"Generated summary for {len(df)} days")
        return df


def create_fetcher(project_id: Optional[str] = None) -> SuiDataFetcher:
    """
    Factory function to create a SuiDataFetcher instance.
    
    Args:
        project_id: Google Cloud project ID. If None, uses default from credentials.
        
    Returns:
        Configured SuiDataFetcher instance
    """
    return SuiDataFetcher(project_id=project_id) 