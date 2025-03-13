# 🚀 cpc_py 🚀
`Crypto Price Command`
A visually enhanced terminal application for real-time cryptocurrency price tracking, K-line charts, and monitoring the total value of all virtual assets. 

It also supports tracking multiple user accounts, recording their crypto holdings and quantities for convenient real-time portfolio valuation. 

All data comes from the APIs of `Mexc SDK`. 

## ✅ Getting Started ✅
`cpc_py` requires Python 3.9+ 

```bash
pip install cpc_py
```

## 📌 Commands Overview 📌
| Command    | Requires `user` | Description |
|------------|-----------------|-------------|
| `symbols`  | ❌ No  | View available cryptocurrency symbols. |
| `price`    | ❌ No  | Check real-time cryptocurrency prices |
| `kline`    | ❌ No  | Display K-line (candlestick) charts |
| `user`     | ✅ Yes | Need to create a new user account first |
| `favorite` | ✅ Yes | Edit favorite list by using `option` command |
| `asset`    | ✅ Yes | Edit asset list by using `option` command|