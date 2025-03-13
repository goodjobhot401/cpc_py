INIT_USER_DATA = {
    "name": "Default User",
    "favorite": [
        "BTCUSDT",
        "ETHUSDT"
    ],
    "asset": [
        {
            "symbol": "BTCUSDT",
            "amount": 0.5
        },
        {
            "symbol": "ETHUSDT",
            "amount": 50.0
        }
    ]
}

PRICE_DETAIL_ROW_MAP = {
    "Latest Price": ("lastPrice", "bold yellow"),
    "Price Change(24H)": ("priceChange", ""),
    "Change(%)": ("priceChangePercent", ""),
    "Highest Bid": ("bidPrice", ""),
    "Bid Quantity": ("bidQty", ""),
    "Lowest Ask": ("askPrice", ""),
    "Ask Quantity": ("askQty", ""),
    "Opening Price": ("openPrice", ""),
    "24H High": ("highPrice", ""),
    "24H Low": ("lowPrice", ""),
    "24H Volume": ("volume", ""),
    "24H Turnover": ("quoteVolume", "")
}

VALID_INTERVAL = ["1m", "5m", "15m", "30m",
                  "60m", "4h", "8h", "1d", "1W", "1M"]
