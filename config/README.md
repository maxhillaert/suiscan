# BigQuery Configuration

This directory contains configuration files for accessing Google BigQuery.

## Setup Instructions

1. **Create a Google Cloud Project** (if you don't have one):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable BigQuery API**:
   - In your Google Cloud Console, go to "APIs & Services" > "Library"
   - Search for "BigQuery API" and enable it

3. **Create Service Account**:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name (e.g., "sui-explorer-bigquery")
   - Grant it the "BigQuery User" role
   - Click "Done"

4. **Download Credentials**:
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON" format
   - Download the file and rename it to `bigquery_credentials.json`
   - Place it in this `config/` directory

5. **Set Environment Variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="config/bigquery_credentials.json"
   ```

## File Structure

```
config/
├── README.md                    # This file
└── bigquery_credentials.json    # Your service account key (create this)
```

## Security Notes

- ⚠️ **Never commit `bigquery_credentials.json` to version control**
- The `.gitignore` file is configured to exclude this file
- Keep your credentials secure and rotate them periodically

## Testing Connection

After setup, you can test your connection by running the main script:

```bash
cd src
python main.py
```

The script will automatically check if credentials are properly configured. 