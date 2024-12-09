from app.cmc.client import cmc_client
from langchain_core.tools import tool
from typing import Optional

from app.graph.state import OverallState, CategoryAnalysisOutputState


@tool
def get_categories_with_changes() -> CategoryAnalysisOutputState:
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
    if not categories or categories['status']['error_code']:
        return {"categories": []}

    # Extract only what we need to reduce token usage
    concise_categories = [
                             {
                                 "name": cat["name"],
                                 "id": cat["id"],
                                 "market_cap": cat["market_cap"],
                                 "market_cap_change": cat["market_cap_change"],
                                 "volume": cat["volume"],
                                 "volume_change": cat["volume_change"],
                             }
                             for cat in categories["data"]
                         ]
    return {"categories": concise_categories}
