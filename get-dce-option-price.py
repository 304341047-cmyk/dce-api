import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
from dceapi import Client
from dceapi.models import QuotesRequest, DayTradeParamRequest, SettleParamRequest


def to_record(obj):
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    return {}


def fetch_quotes_df(client, variety_id, trade_date, trade_type):
    quotes = client.market.get_day_quotes(
        QuotesRequest(
            variety_id=variety_id,
            trade_date=trade_date,
            trade_type=trade_type
        )
    )

    df_quotes = pd.DataFrame([
        {
            "contract_id": getattr(q, "contract_id", None),
            "close": getattr(q, "close", None),
            "settle_price": getattr(q, "clear_price", None),
            "volume": getattr(q, "volume", None),
            "open_interest": getattr(q, "open_interest", None),
        }
        for q in quotes
        if getattr(q, "contract_id", None)
    ])

    return df_quotes


def fetch_settle_df(client, variety_id, trade_date, trade_type, lang="zh"):
    settle_params = client.settle.get_settle_param(
        SettleParamRequest(
            variety_id=variety_id,
            trade_date=trade_date,
            trade_type=trade_type,
            lang=lang
        )
    )

    df_settle = pd.DataFrame([
        {
            "contract_id": getattr(s, "contract_id", None),
            "trade_date": trade_date,
            "margin_buy_rate": getattr(s, "spec_buy_rate", None),
            "margin_sell_rate": getattr(s, "spec_sell_rate", None),
            "open_fee": getattr(s, "open_fee", None),
            "offset_fee": getattr(s, "offset_fee", None),
            "intraday_open_fee": getattr(s, "short_open_fee", None),
            "intraday_offset_fee": getattr(s, "short_offset_fee", None),
        }
        for s in settle_params
        if getattr(s, "contract_id", None)
    ])

    return df_settle


def fetch_trade_df(client, variety_id, trade_type, lang="zh"):
    trade_params = client.trade.get_day_trade_param(
        DayTradeParamRequest(
            variety_id=variety_id,
            trade_type=trade_type,
            lang=lang
        )
    )

    records = []
    for t in trade_params:
        contract_id = getattr(t, "contract_id", None)
        if not contract_id:
            continue

        rec = to_record(t)
        records.append(rec)

    df_trade = pd.DataFrame(records)

    if df_trade.empty:
        return df_trade

    # 仅把 contract_id 和 trade_date 放前面，其余保持原样
    cols = list(df_trade.columns)
    ordered = []

    if "contract_id" in cols:
        ordered.append("contract_id")
    if "trade_date" in cols and "trade_date" not in ordered:
        ordered.append("trade_date")

    for c in cols:
        if c not in ordered:
            ordered.append(c)

    return df_trade[ordered]


def build_market_settle_df(client, variety_id, trade_date, trade_type, lang="zh"):
    df_quotes = fetch_quotes_df(client, variety_id, trade_date, trade_type)
    df_settle = fetch_settle_df(client, variety_id, trade_date, trade_type, lang=lang)

    df_market_settle = pd.merge(
        df_quotes,
        df_settle,
        on="contract_id",
        how="outer"
    )

    desired_cols = [
        "contract_id",
        "trade_date",
        "close",
        "settle_price",
        "volume",
        "open_interest",
        "margin_buy_rate",
        "margin_sell_rate",
        "open_fee",
        "offset_fee",
        "intraday_open_fee",
        "intraday_offset_fee",
    ]

    for col in desired_cols:
        if col not in df_market_settle.columns:
            df_market_settle[col] = None

    df_market_settle = df_market_settle[desired_cols]
    df_market_settle = df_market_settle.sort_values(by="contract_id").reset_index(drop=True)

    return df_market_settle


def main():
    client = Client.from_env()

    variety_id = "i"
    market_date = "20260409"
    today_date = datetime.today().strftime("%Y%m%d")
    lang = "zh"

    # 文件1：日行情 + 结算参数
    df_market_settle_futures = build_market_settle_df(
        client, variety_id, market_date, trade_type="1", lang=lang
    )
    df_market_settle_options = build_market_settle_df(
        client, variety_id, market_date, trade_type="2", lang=lang
    )

    market_settle_file = f"market_settle_snapshot_{market_date}.xlsx"
    with pd.ExcelWriter(market_settle_file, engine="openpyxl") as writer:
        df_market_settle_futures.to_excel(writer, sheet_name="Futures", index=False)
        df_market_settle_options.to_excel(writer, sheet_name="Options", index=False)

    # 文件2：交易参数
    df_trade_futures = fetch_trade_df(
        client, variety_id, trade_type="1", lang=lang
    )
    df_trade_options = fetch_trade_df(
        client, variety_id, trade_type="2", lang=lang
    )

    trade_file = f"trade_params_snapshot_{today_date}.xlsx"
    with pd.ExcelWriter(trade_file, engine="openpyxl") as writer:
        df_trade_futures.to_excel(writer, sheet_name="Futures", index=False)
        df_trade_options.to_excel(writer, sheet_name="Options", index=False)

    print(f"Saved: {market_settle_file}")
    print(f"Saved: {trade_file}")


if __name__ == "__main__":
    main()