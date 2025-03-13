# 🚀 cpc_py 🚀
`Crypto Price Command`
A visually enhanced terminal application for real-time cryptocurrency price tracking, K-line charts, and monitoring the total value of all virtual assets. 

It also supports tracking multiple user accounts, recording their crypto holdings and quantities for convenient real-time portfolio valuation. 

All data comes from the APIs of `Mexc SDK`. 

![Demo Screenshot](/doc/images/price_example3.png)
<br>

## ✅ Getting Started ✅
`cpc_py` requires Python 3.9+ 

```bash
pip install cpc_py
```
<br>

## 📌 Commands Overview 📌
Commands like `users`, `user`, `favorite`, and `asset` require user-provided data before they can be used. 
| Command    | Requires `user` | Description |
|------------|-----------------|-------------|
| `symbols`  | ❌ No  | View available crypto currency symbols. |
| `price`    | ❌ No  | Check real-time crypto currency prices |
| `kline`    | ❌ No  | Display K-line (candlestick) charts |
| `users`    | ✅ Yes | Display the user list, default value is inserted on first use |
| `user`     | ✅ Yes | A user must be created first, but a default value is inserted on first use |
| `favorite` | ✅ Yes | Edit favorite list by using `option` command |
| `asset`    | ✅ Yes | Edit asset list by using `option` command|
<br>

## 🔍 Documents 🔍
- **`cpc symbols [--option]`**  
  - **Description**: 

    Use the `symbols` command to search for valid cryptocurrency symbols.  
  - **Usage**:
    ```bash
    cpc symbols [--option]
    ```
  - **Behavior**:
    - If no `option` is provided, the command will return all available symbols sorted in `A-Z` order.
    - If an `option` is provided, it will return similar available symbols based on the input.
    - Example
    
            cpc symbols

        ![Demo Screenshot](/doc/images/symbols_example2.png)

            cpc symbols xr

        ![Demo Screenshot](/doc/images/symbols_example3.png)

- **`cpc price [symbol list]`**  
  - **Description**: 

    Use the `price` command to search real-time price.  
  - **Usage**:
    ```bash
    cpc price [symbol list]
    ```
  - **Behavior**:
    - Example
    
            cpc price btcusdt ethusdt solusdt
        
        ![Demo Screenshot](/doc/images/price_example3.png)


- **`cpc kline [symbol] [--interval] [--limit]`**  
  - **Description**: 

    Use the `kline` command to display K-line charts.  
  - **Usage**:
    ```bash
    cpc kline [symbol] [--interval] [--limit]
    ```
  - **Behavior**:
    - `interval` only accepts the following values 
        - `['1m', '5m', '15m', '30m', '60m', '4h', '8h', '1d', '1W', '1M']`
    - Example

            cpc kline btcusdt --interval 1W
            
    
        ![Demo Screenshot](/doc/images/kline_example1.png)


- **`cpc users`**  
  - **Description**: 

    Use the `users` command to display user list and show which user is targeted.
  - **Usage**:
    ```bash
    cpc users
    ```
  - **Behavior**:
    - Example
    
            cpc users


        ![Demo Screenshot](/doc/images/users_example1.png)

  - **Extension**:
    - `cpc switch_user [user_id]`
        
        Use the `switch_user` command to switch the target.

      - example

            cpc switch_user 3
            


- **`cpc user`**
  - **Description**: 

    Use the `user` command to display the detail infomation of the targeted user.
  - **Usage**:
    ```bash
    cpc user
    ```
  - **Behavior**:
    - Example
    
            cpc user

        ![Demo Screenshot](/doc/images/binance%20wallet/user_example1.png)

  - **Extension**:
    - `cpc create_user [name]`

        Use the `create_user` command to create a new user, and that will be targeted immediately.

      - example

            cpc create_user Tom's Bitget account
            

    - `cpc update_user [user_id] [name]`

        Use the `update_user` command to update user's name by user_id.

      - example

            cpc update_user 2 Binance wallet
            

    - `cpc remove_user [user_id]`

        Use the `remove_user` command to remove user by user_id.

      - example

            cpc remove_user 2

- **`cpc favorite`**
  - **Description**: 

    Use the `favorite` command to fetch price details for all crypto currencies in the targeted user's favorite list.
  - **Usage**:
    ```bash
    cpc favorite
    ```
  - **Behavior**:
    - Example

            cpc favorite
    
        ![Demo Screenshot](/doc/images/binance%20wallet/favorite_example1.png)

  - **Extension**:
    - `cpc add_favorite [symbol list]`

        Use the `add_favorite` command to add new symbols to the favorite list.

      - example

            cpc add_favorite btcusdt ethusdt
            

    - `cpc remove_favorite [symbol list]`

        Use the `remove_favorite` command to remove symbols from the targeted user's favorite list.

      - example

            cpc remove_favorite btcusdt ethusdt
            


- **`cpc asset`**
  - **Description**: 

    Use the `asset` command to calculate market value for all crypto currencies in the targeted user's asset list.
  - **Usage**:
    ```bash
    cpc asset
    ```
  - **Behavior**:
    - Example

            cpc asset
    
        ![Demo Screenshot](/doc/images/binance%20wallet/asset_example1.png)

  - **Extension**:
    - `cpc add_asset [asset list]`

        Use the `add_asset` command to add new symbols to the asset list.
        
        - example

                cpc add_asset btcusdt 0.001 ethusdt 0.25
            


    - `cpc update_asset` [asset list]

        User the `update_asset` command to update amount of the asset.

        - example

                cpc update_asset btcusdt 0.002 ethusdt 0.35
            

    - `cpc remove_asset [asset list]`

        Use the `remove_asset` command to remove symbols from the targeted user's asset list.

        - example

                cpc remove_asset btcusdt ethusdt