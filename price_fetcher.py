import httpx
from typing import List, Dict
from settings import PRICE_API_URL_TEMPLATE

async def get_token_prices(token_addresses: List[str]) -> Dict[str, float]:
    """
    Fetches prices for a list of token addresses from the API.
    Returns a dictionary mapping token address to its price.
    """
    if not token_addresses:
        return {}

    tokens_str = ",".join(token_addresses)
    url = PRICE_API_URL_TEMPLATE.format(tokens=tokens_str)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            
            # The API returns a dictionary like {"prices":{"TOKEN_ADDR":0.123}}
            # We just need to access the nested dictionary.
            prices = data.get('prices', {})
            return prices
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (e.g., API down, invalid request)
            print(f"HTTP error occurred: {e}")
            return {}
        except Exception as e:
            # Handle other exceptions (e.g., network issues, invalid JSON)
            print(f"An error occurred: {e}")
            return {}
