import httpx
import asyncio
import logging
import pandas as pd
from aiolimiter import AsyncLimiter
from datetime import datetime
from typing import Union, List, Dict
import pyarrow as pa
import pyarrow.parquet as pq
import boto3
from io import BytesIO
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CoinGeckoAPI:
    def __init__(self, api_key: str, base_url: str = "https://pro-api.coingecko.com/api/v3", rate_limit: int = 500):
        self.api_key = api_key
        self.base_url = base_url
        self.limiter = AsyncLimiter(rate_limit, 60)

    async def fetch(self, endpoint: str, params: dict = None, retries: int = 3) -> dict:
        """General method to perform an API GET request with retries."""
        async with httpx.AsyncClient() as client:
            headers = {
                "accept": "application/json",
                "x-cg-pro-api-key": self.api_key,
            }

            for attempt in range(retries):
                try:
                    await self.limiter.acquire()
                    response = await client.get(f"{self.base_url}/{endpoint}", params=params, headers=headers, timeout=10)
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429 and attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        logging.error(f"HTTP error: {e.response.status_code}")
                        raise
                except Exception as e:
                    logging.error(f"Request error: {e}")
                    raise

    async def fetch_all_pages(self, endpoint: str, params: dict, max_pages: int) -> list:
        """Fetch all pages of data asynchronously."""
        tasks = [self.fetch(endpoint, {**params, "page": page}) for page in range(1, max_pages + 1)]
        results = await asyncio.gather(*tasks)
        return [item for sublist in results for item in sublist if item]


class CoinGeckoDataProcessor:
    """Handles processing of data returned by the CoinGecko API."""

    @staticmethod
    def merge_timeseries_data(data: dict, coingecko_id: str) -> pd.DataFrame:
        """Clean and merge timeseries data."""
        prices = pd.DataFrame(data['prices'], columns=['date', 'price'])
        market_cap = pd.DataFrame(data['market_caps'], columns=['date', 'market_cap'])
        volume = pd.DataFrame(data['total_volumes'], columns=['date', 'volume'])
        df = prices.merge(market_cap, on='date').merge(volume, on='date')
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df['coingecko_id'] = coingecko_id
        return df

    @staticmethod
    def save_to_parquet(df: pd.DataFrame, file_path: str):
        """Save DataFrame to a Parquet file."""
        df.to_parquet(file_path, index=False)


class CoinGecko:
    def __init__(self, api_key: str, rate_limit: int = 500):
        self.api = CoinGeckoAPI(api_key, rate_limit=rate_limit)

    async def _async_get_categories(self) -> pd.DataFrame:
        """Fetches the list of all categories from the CoinGecko API and returns as a DataFrame."""
        categories = await self.api.fetch("coins/categories/list")
        return pd.DataFrame(categories)

    async def _async_get_coins(self, coins: int, category: str = None) -> pd.DataFrame:
        """Gets a list of assets from CoinGecko API asynchronously."""
        per_page = 250
        pages = coins // per_page + (0 if coins % per_page == 0 else 1)

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": per_page,
            "sparkline": False,
            "locale": "en",
            "x_cg_pro_api_key": self.api.api_key
        }
        if category:
            params["category"] = category

        data = await self.api.fetch_all_pages("coins/markets", params, pages)
        df = pd.DataFrame(data)
        df.drop(columns=['roi'], inplace=True)
        df.rename(columns={"id": "coingecko_id"}, inplace=True)
        return df

    async def _async_get_timeseries(self, coingecko_ids: list) -> pd.DataFrame:
        """Fetch and process timeseries data for multiple assets."""
        tasks = [self.api.fetch(f"coins/{id}/market_chart", {
            "vs_currency": "usd",
            "days": "max",
            "interval": "daily",
            "x_cg_pro_api_key": self.api.api_key
        }) for id in coingecko_ids]

        results = await asyncio.gather(*tasks)
        df_list = [CoinGeckoDataProcessor.merge_timeseries_data(data, id) for data, id in zip(results, coingecko_ids)]
        return pd.concat(df_list, ignore_index=True)

    def get_categories(self) -> pd.DataFrame:
        """Synchronous method to fetch and return all categories as a DataFrame."""
        return asyncio.run(self._async_get_categories())

    def get_coins(self, coins: int, category: str = None) -> pd.DataFrame:
        """Synchronous method to fetch and return coins as a DataFrame."""
        return asyncio.run(self._async_get_coins(coins, category))

    def get_timeseries(self, coingecko_ids: list) -> pd.DataFrame:
        """Synchronous method to fetch and return timeseries data as a DataFrame."""
        return asyncio.run(self._async_get_timeseries(coingecko_ids))

    def export_data(self, coins: Union[int, List[str], str], export_format: str = 'df') -> pd.DataFrame:
        """Main method to fetch and export CoinGecko data."""
        if isinstance(coins, int):
            coins_df = self.get_coins(coins)
            coins = coins_df["coingecko_id"].tolist()
        elif isinstance(coins, str):
            coins_df = self.get_all_active_coins()
            coins = coins_df["coingecko_id"].tolist()

        historical_data_df = self.get_timeseries(coins)

        if export_format == 'df':
            return historical_data_df
        elif export_format == 'parquet':
            today = datetime.now().strftime("%Y-%m-%d")
            CoinGeckoDataProcessor.save_to_parquet(historical_data_df, f"data/historical_data_{today}.parquet")
        else:
            raise ValueError("Invalid export format. Choose 'df' or 'parquet'.")

    def get_total_marketcap(self) -> pd.DataFrame:
        """Fetches the total market cap data from the CoinGecko API and returns it as a DataFrame."""
        url = f"{self.api.base_url}/global/market_cap_chart?days=max"
        headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": self.api.api_key
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()

        # Process the market cap data
        market_cap_data = pd.DataFrame(data['market_cap'], columns=['date', 'market_cap'])
        market_cap_data['date'] = pd.to_datetime(market_cap_data['date'], unit='ms')
        
        return market_cap_data
    
    def get_all_active_coins(self) -> pd.DataFrame:
        """Fetches the list of all active coins from the CoinGecko API and returns it as a DataFrame."""
        url = "https://pro-api.coingecko.com/api/v3/coins/list?include_platform=false&status=active"

        headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": "CG-6rSA4HVyKdSVzEno5Sp7tJ2W"
        }

        r = requests.get(url, headers=headers).json()
        df = pd.DataFrame(r)
        df.rename(columns={"id": "coingecko_id"}, inplace=True)
        return df


    def upload_to_s3(
        self,
        df: pd.DataFrame,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket_name: str,
        folder_name: str = None,
        file_name: str = None,
    ):
        """Uploads a DataFrame to S3 as a Parquet file."""
        table = pa.Table.from_pandas(df)
        buffer = BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0)

        # Set up S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        # Construct S3 key
        s3_key = f"{folder_name}/" if folder_name else ""
        s3_key += file_name if file_name else "data.parquet"

        # Upload to S3
        s3_client.upload_fileobj(buffer, bucket_name, s3_key)
        print(f"File uploaded successfully to {bucket_name}/{s3_key}")


if __name__ == "__main__":
    cg = CoinGecko(api_key="CG-api-key")

    # Fetch and print the categories DataFrame
    categories_df = cg.get_categories()
    print(categories_df)
    
    first_value = categories_df['category_id'].iloc[0]

    # Fetch coins within the first category
    coins_df = cg.get_coins(100, category=first_value)
    print(coins_df)

    print('uploading to s3')
    # Export data to S3
    cg.upload_to_s3(
        df=coins_df,
        aws_access_key_id="access-key",
        aws_secret_access_key="secret-key",
        bucket_name="bucket-name",
        folder_name="folder-name",
        file_name=f"filename_{datetime.now().strftime("%Y-%m-%d")}.parquet",
    )