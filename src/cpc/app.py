import argparse
from cpc.handlers import (
    SYMBOL,
    PRICE,
    KLINE,
    USER,
    FAVORITE,
    ASSET
)


def main():
    parser = argparse.ArgumentParser(usage="cpc [COMMAND] [OPTIONS]",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="examples: \n  cpc price BTCUSDT ETHUSDT\n  cpc symbols XRP")

    subparsers = parser.add_subparsers(dest="command",
                                       metavar="[Commands]",
                                       title="available commands",
                                       help="[Description]")

    # symbols
    parser_symbols = subparsers.add_parser("symbols",
                                           usage="cpc symbols [query]",
                                           help="List or filter symbols",
                                           epilog="examples: cpc symbols btc or cpc symbols ETHusDt")
    parser_symbols.add_argument("query",
                                nargs="?",
                                default=None,
                                help="Optional symbol filter")

    # price
    parser_price = subparsers.add_parser("price",
                                         usage="cpc price [symbol list]",
                                         help="Search price of symbol list",
                                         epilog="examples: cpc price btcusdt ethusdc xrpusdc")
    parser_price.add_argument("symbols",
                              nargs="+", help="Symbols to get price for")

    # kline
    parser_kline = subparsers.add_parser("kline",
                                         usage="cpc kline [symbol] [--interval] [--limit]",
                                         help="Get kline of a symbol",
                                         epilog="examples: cpc kline btcusdt --interval 4h --limit 30")
    parser_kline.add_argument("symbol",
                              help="Symbol to get kline for")
    parser_kline.add_argument("--interval",
                              nargs="?",
                              default="1d",
                              help="Interval of kline (e.g., 1m, 5m, 15m, 30m, 60m, 4h, 8h, 1d, 1W, 1M)")
    parser_kline.add_argument("--limit",
                              nargs="?",
                              default=30,
                              help="Amount of kline")

    # users, user, create_user, switch_user, update_user, remove_user
    subparsers.add_parser("users", help="Get all user")
    subparsers.add_parser("user", help="Get detail of targeted user")

    parser_create_user = subparsers.add_parser("create_user",
                                               usage="cpc create_user [name]",
                                               help="Create a new user",
                                               epilog="examples: cpc create_user Binance Wallet")
    parser_create_user.add_argument("name",
                                    nargs="+",
                                    help="Name of the new user")

    parser_switch_user = subparsers.add_parser("switch_user",
                                               usage="cpc switch_user [user_id]",
                                               help="Target another user",
                                               epilog="examples: cpc switch_user 2")
    parser_switch_user.add_argument("user_id",
                                    nargs="?",
                                    help="Id of the user to be targeted")

    parser_update_user = subparsers.add_parser("update_user",
                                               usage="cpc update_user [user_id] [name]",
                                               help="Update user's name",
                                               epilog="examples: cpc update_user 2 OKX Wallet")
    parser_update_user.add_argument("user_id",
                                    help="Id of the user to be updated")
    parser_update_user.add_argument("name",
                                    nargs="+",
                                    help="Name of the user to be updated")

    parser_remove_user = subparsers.add_parser("remove_user",
                                               usage="cpc remove_user [user_id]",
                                               help="Remove user",
                                               epilog="examples: cpc remove_user 2")
    parser_remove_user.add_argument("user_id",
                                    help="Id of the user to be removed")

    # favortie, add_favorite, remove_favorite
    subparsers.add_parser("favorite",
                          help="Get price detail of favortite list")
    parser_add_favorite = subparsers.add_parser("add_favorite",
                                                usage="cpc add_favorite [symbol list]",
                                                help="Add favorties into favorite list",
                                                epilog="examples: cpc add_favorite btcusdt ethusdt xrpusdt")
    parser_add_favorite.add_argument("favorite_list",
                                     nargs="+",
                                     default=None,
                                     help="Favorite list to be added")
    parser_remove_favorite = subparsers.add_parser("remove_favorite",
                                                   usage="cpc add_favorite [symbol list]",
                                                   help="Remove favorties from favorite list",
                                                   epilog="examples: cpc remove_favorite btcusdt ethusdt xrpusdt")
    parser_remove_favorite.add_argument("favorite_list",
                                        nargs="+",
                                        default=None,
                                        help="Favorite list to be removed")

    # asset, add_asset, update_asset, remove_asset
    parser_asset = subparsers.add_parser("asset",
                                         usage="cpc asset [--sort] [--reverse]",
                                         help="Get asset position of asset list",
                                         epilog="examples: cpc asset or cpc asset --sort amount --reverse true")
    parser_asset.add_argument("--sort",
                              nargs="?",
                              choices=["value", "amount", "symbol"],
                              default="value",
                              help="Method of sorted")
    parser_asset.add_argument("--reverse",
                              nargs="?",
                              choices=["True", "true", "False", "false"],
                              default="True",
                              help="DESC or ASC")
    parser_add_asset = subparsers.add_parser("add_asset",
                                             help="Add asset into asset list",
                                             epilog="examples: cpc add_asset btcusdt 0.5 ethusdt 2.5")
    parser_add_asset.add_argument("asset_list",
                                  nargs="+",
                                  default=None,
                                  help="Asset list to be added")
    parser_update_asset = subparsers.add_parser("update_asset",
                                                help="Update the asset which in the asset list",
                                                epilog="examples: cpc update_asset btcusdt 1.5 ethusdt 5.5")
    parser_update_asset.add_argument("asset_list",
                                     nargs="+",
                                     default=None,
                                     help="Asset list to be updated")
    parser_remove_asset = subparsers.add_parser("remove_asset",
                                                help="Remove the asset which in the asset list",
                                                epilog="examples: cpc remove_asset btcusdt ethusdt")
    parser_remove_asset.add_argument("asset_list",
                                     nargs="+",
                                     default=None,
                                     help="Asset list to be removed")

    args = parser.parse_args()
    match args.command:
        case "symbols":
            if args.query:
                SYMBOL.filter_symbols(args.query)
            else:
                SYMBOL.filter_symbols()

        case "price":
            if args.symbols:
                PRICE.get_price_detail(args.symbols)

        case "kline":
            if args.symbol:
                KLINE.get_kline(
                    args.symbol, interval=args.interval, limit=args.limit)

        case "user":
            USER.get_user(print_table=True)

        case "users":
            USER.get_users()

        case "create_user":
            if args.name:
                USER.create_user(args.name)

        case "switch_user":
            if args.user_id:
                USER.switch_user(args.user_id)

        case "update_user":
            if args.user_id and args.name:
                USER.update_user(args.user_id, args.name)

        case "remove_user":
            if args.user_id:
                USER.remove_user(args.user_id)

        case "favorite":
            PRICE.get_price_detail(USER.get_user()["favorite"])

        case "add_favorite":
            if args.favorite_list:
                FAVORITE.add_favorite(args.favorite_list)

        case "remove_favorite":
            if args.favorite_list:
                FAVORITE.remove_favorite(args.favorite_list)

        case "asset":
            USER.get_position_ratio(
                sort=args.sort, reverse=args.reverse)

        case "add_asset":
            if args.asset_list:
                ASSET.add_asset(args.asset_list)

        case "update_asset":
            if args.asset_list:
                ASSET.update_asset(args.asset_list)

        case "remove_asset":
            if args.asset_list:
                ASSET.remove_asset(args.asset_list)


if __name__ == "__main__":
    main()
