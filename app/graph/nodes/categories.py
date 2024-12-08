from app.cmc.client import cmc_client
from langchain_core.tools import tool
from typing import Optional


@tool
def get_categories_with_changes() -> Optional[list[dict]]:
    """
    Get the list of crypto market categories with market data.

    :return:
    - Category Name
    - Market cap
    - Market cap change (24h)
    - Volume
    - Volume Change (24h)
    """
    categories = cmc_client.get_categories()
    if not categories:
        return

    # if API returned error -> return
    if categories['status']['error_code']:
        return

    output = []
    # Extract only what we need to reduce token usage
    for category in categories['data']:
        concise_category = dict()
        concise_category['name'] = category['name']
        concise_category['id'] = category['id']
        concise_category['market_cap'] = category['market_cap']
        concise_category['market_cap_change'] = category['market_cap_change']
        concise_category['volume'] = category['volume']
        concise_category['volume_change'] = category['volume_change']

        output.append(concise_category)
    return output
