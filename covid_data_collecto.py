"""
get_covid_owid.py
-----------------
Downloads the latest Our World in Data (OWID) COVID-19 dataset,
filters it to 15 countries and date range Jan 1, 2022 -> Dec 31, 2024,
selects the required columns, and saves as CSV + Excel.

Requirements:
    pip install pandas requests openpyxl
"""

import io
import requests
import pandas as pd
from datetime import datetime

# ---------- SETTINGS ----------
COUNTRIES = [
    "United States", "India", "Brazil", "United Kingdom", "Germany",
    "France", "Italy", "Spain", "Russia", "Turkey",
    "Japan", "Canada", "Australia", "Argentina", "South Africa"
]

START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

# OWID CSV URL (latest and compact)
OWID_COMPACT_CSV = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"
# --------------------------------

def download_csv(url):
    print("Downloading OWID CSV (this may take a moment)...")
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    return r.content

def main():
    try:
        data_bytes = download_csv(OWID_COMPACT_CSV)
    except Exception as e:
        print("❌ Failed to download OWID CSV.")
        print("Error:", e)
        print("Try downloading manually from https://ourworldindata.org/coronavirus and updating the URL.")
        return

    print("Reading CSV into pandas...")
    df = pd.read_csv(io.BytesIO(data_bytes), parse_dates=["date"], low_memory=False)

    # ---------- Handle column naming differences ----------
    # OWID may call the country column 'location', 'country', or 'entity'
    possible_country_cols = ["location", "country", "entity"]
    country_col = None
    for col in possible_country_cols:
        if col in df.columns:
            country_col = col
            break

    if not country_col:
        print("❌ Could not find any of these columns:", possible_country_cols)
        print("Available columns:", list(df.columns)[:20])
        return

    wanted = {
        country_col: "Country",
        "date": "Date",
        "new_cases": "New Cases",
        "new_deaths": "New Deaths",
        "total_vaccinations": "Total Vaccinations",
        "stringency_index": "Stringency Index"
    }

    missing = [k for k in wanted.keys() if k not in df.columns]
    if missing:
        print("⚠️ Warning: Missing columns:", missing)
        print("Continuing with available columns only.")
    available_cols = [c for c in wanted.keys() if c in df.columns]

    # ---------- Filter data ----------
    print("Filtering by date and countries...")
    df = df.loc[
        (df["date"] >= START_DATE) &
        (df["date"] <= END_DATE) &
        (df[country_col].isin(COUNTRIES)),
        available_cols
    ]

    # ---------- Rename and format ----------
    df = df.rename(columns={k: v for k, v in wanted.items() if k in df.columns})
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df = df.sort_values(["Country", "Date"]).reset_index(drop=True)

    # ---------- Save ----------
    out_csv = "covid_2022_2024_15countries.csv"
    out_xlsx = "covid_2022_2024_15countries.xlsx"

    print(f"Saving {out_csv} ...")
    df.to_csv(out_csv, index=False)
    print(f"Saving {out_xlsx} ...")
    df.to_excel(out_xlsx, index=False, engine="openpyxl")

    print("\n✅ Done! Files saved:")
    print(f" - {out_csv}")
    print(f" - {out_xlsx}")
    print("\nSummary:")
    print("Rows:", len(df))
    print("Countries found:", df['Country'].unique().tolist())

if __name__ == "__main__":
    main()
