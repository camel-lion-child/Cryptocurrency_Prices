
import requests

FLIPSIDE_API_KEY = "1989b34e-ab83-4cab-b260-71278c9095ac"
FLIPSIDE_API_URL = "https://api.flipsidecrypto.com/queries"

query = {
    "sql": """
    SELECT 
        symbol, 
        price_usd, 
        market_cap, 
        volume_24h
    FROM flipside.crypto_prices
    ORDER BY market_cap DESC
    LIMIT 50
    """,
}

headers = {"x-api-key": FLIPSIDE_API_KEY}
response = requests.post(FLIPSIDE_API_URL, json=query, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Lỗi: {response.status_code} - {response.text}")
