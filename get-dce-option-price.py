import csv
from dceapi import Client
from dceapi.models import QuotesRequest

def main():
    client = Client.from_env()

    req = QuotesRequest(
        variety_id="i",          # 可以改成你要的品种
        trade_date="20260408",   # 可以改成今天
        trade_type="2"           # 期权
    )

    quotes = client.market.get_day_quotes(req)

    with open("option_quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        # 表头
        writer.writerow([
            "contract_id",
            "close",
            "clear_price",
            "volume",
            "open_interest"
        ])

        for q in quotes:
            writer.writerow([
                getattr(q, "contract_id", ""),
                getattr(q, "close", ""),
                getattr(q, "clear_price", ""),
                getattr(q, "volume", ""),
                getattr(q, "open_interest", "")
            ])

    print(f"Saved {len(quotes)} rows")

if __name__ == "__main__":
    main()