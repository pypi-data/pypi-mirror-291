
# CoinGecko API Wrapper

This project provides a Python wrapper for the CoinGecko API, enabling users to fetch cryptocurrency data, process it into pandas DataFrames, and upload it to AWS S3 as Parquet files. The wrapper abstracts away the complexity of asynchronous API calls and provides an easy-to-use interface for interacting with the CoinGecko API.

## Table of Contents

- [Installation](#installation)
- [Class Structure](#class-structure)
  - [CoinGeckoAPI](#coingeckoapi)
  - [CoinGeckoDataProcessor](#coingeckodataprocessor)
  - [CoinGecko](#coingecko)
- [Usage](#usage)
  - [Fetching Categories](#fetching-categories)
  - [Fetching Coins](#fetching-coins)
  - [Fetching Timeseries Data](#fetching-timeseries-data)
  - [Exporting Data to Parquet](#exporting-data-to-parquet)
  - [Uploading Data to S3](#uploading-data-to-s3)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

   \`\`\`bash
   git clone https://github.com/yourusername/coingecko-api-wrapper.git
   cd coingecko-api-wrapper
   \`\`\`

2. **Set up a virtual environment:**

   \`\`\`bash
   python3 -m venv venv
   source venv/bin/activate
   \`\`\`

3. **Install the required dependencies:**

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Class Structure

### CoinGeckoAPI

The \`CoinGeckoAPI\` class is responsible for interacting directly with the CoinGecko API. It handles:

- Making asynchronous GET requests to the API.
- Managing rate limits using \`AsyncLimiter\`.
- Fetching data from paginated endpoints.

#### Methods:

- \`fetch(endpoint: str, params: dict = None, retries: int = 3) -> dict\`: Performs a GET request to the specified endpoint.
- \`fetch_all_pages(endpoint: str, params: dict, max_pages: int) -> list\`: Fetches all pages of data asynchronously.

### CoinGeckoDataProcessor

The \`CoinGeckoDataProcessor\` class processes raw data fetched from the CoinGecko API. It handles:

- Merging timeseries data into a pandas DataFrame.
- Saving DataFrames to Parquet files.

#### Methods:

- \`merge_timeseries_data(data: dict, coingecko_id: str) -> pd.DataFrame\`: Cleans and merges timeseries data.
- \`save_to_parquet(df: pd.DataFrame, file_path: str)\`: Saves a DataFrame to a Parquet file.

### CoinGecko

The \`CoinGecko\` class is the main interface for users. It abstracts away the complexities of asynchronous calls and provides simple, synchronous methods to fetch data, process it, and upload it to S3.

#### Methods:

- \`get_categories() -> pd.DataFrame\`: Fetches all categories from the CoinGecko API.
- \`get_coins(coins: int, category: str = None) -> pd.DataFrame\`: Fetches a list of assets based on market cap.
- \`get_timeseries(coingecko_ids: list) -> pd.DataFrame\`: Fetches and processes timeseries data.
- \`export_data(coins: Union[int, List[str]], export_format: str = 'df') -> pd.DataFrame\`: Fetches and exports data as a DataFrame or saves it as a Parquet file.
- \`upload_to_s3(df: pd.DataFrame, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str, folder_name: str = None, file_name: str = None)\`: Uploads a DataFrame to AWS S3 as a Parquet file.

## Usage

### Fetching Categories

\`\`\`python
from coingecko import CoinGecko

cg = CoinGecko(api_key="your-api-key")

# Fetch and print the categories DataFrame
categories_df = cg.get_categories()
print(categories_df)
\`\`\`

### Fetching Coins

\`\`\`python
from coingecko import CoinGecko

cg = CoinGecko(api_key="your-api-key")

# Fetch top 100 coins by market cap
coins_df = cg.get_coins(100)
print(coins_df)
\`\`\`

### Fetching Timeseries Data

\`\`\`python
from coingecko import CoinGecko

cg = CoinGecko(api_key="your-api-key")

# Fetch timeseries data for a list of coin IDs
timeseries_df = cg.get_timeseries(['bitcoin', 'ethereum'])
print(timeseries_df)
\`\`\`

### Exporting Data to Parquet

\`\`\`python
from coingecko import CoinGecko

cg = CoinGecko(api_key="your-api-key")

# Export data to a Parquet file
cg.export_data(coins=100, export_format='parquet')
\`\`\`

### Uploading Data to S3

\`\`\`python
from coingecko import CoinGecko

cg = CoinGecko(api_key="your-api-key")

# Fetch and upload coins data to S3
coins_df = cg.get_coins(100)
cg.upload_to_s3(
    df=coins_df,
    aws_access_key_id="your-aws-access-key-id",
    aws_secret_access_key="your-aws-secret-access-key",
    bucket_name="your-s3-bucket-name",
    folder_name="your-folder-name",
    file_name="your-file-name.parquet"
)
\`\`\`
