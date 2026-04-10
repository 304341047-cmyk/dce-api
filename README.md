# DCE Market Data Downloader

## 📌 Project Overview

This project retrieves daily market data and trading parameters from the Dalian Commodity Exchange (DCE) using the `dceapi` Python SDK. 

---

## ✨ Features

* 📊 Downloads daily **futures and options market data**

---

## 📂 Output Files

### 1. Market and Settlement Data

**`market_settle_snapshot_YYYYMMDD.xlsx`**

| Sheet Name | Description                                   |
| ---------- | --------------------------------------------- |
| Futures    | Futures market data and settlement parameters |
| Options    | Options market data and settlement parameters |

---

### 2. Trading Parameters

**`trade_params_snapshot_YYYYMMDD.xlsx`**

| Sheet Name | Description                      |
| ---------- | -------------------------------- |
| Futures    | Daily futures trading parameters |
| Options    | Daily options trading parameters |


---

## 🛠️ Technologies Used

* **Python 3**
* **Pandas** – Data processing and export
* **dceapi** – DCE API SDK
* **python-dotenv** – Secure credential management
* **OpenPyXL** – Excel file generation

---

## 📦 Installation

Install the required dependencies:

```bash
pip install pandas python-dotenv openpyxl dceapi
```

---

## 🔑 Configuration

Create a `.env` file in the project root directory:

```env
DCE_API_KEY=your_api_key
DCE_SECRET=your_api_secret
```

---

## 🚀 Usage

Run the script:

```bash
python get-dce-option-price.py
```

The program will generate two Excel files containing the requested data.

---

## 📊 Project Structure

```
dce-market-data-downloader/
│
├── get-dce-option-price.py   # Main script
├── .env                      # API credentials (not tracked)
├── .gitignore
├── README.md
└── output/
    ├── market_settle_snapshot_YYYYMMDD.xlsx
    └── trade_params_snapshot_YYYYMMDD.xlsx
```

---

## ⚠️ Notes

* The `trade_param` interface returns data for the current trading day by default.
* Settlement prices for options are sourced from market quotes.
* Ensure that your API credentials are valid and have the necessary permissions.

---

## 📜 License

This project is intended for educational and research purposes. Please ensure compliance with the Dalian Commodity Exchange data usage policies.

---


## ⭐ Acknowledgements

* Dalian Commodity Exchange (DCE)
* Contributors of the `dceapi` Python SDK
