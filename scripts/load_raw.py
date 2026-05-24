import duckdb
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.environ.get("DB_PATH",  os.path.join(ROOT, "olist.duckdb"))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(ROOT, "data"))

TABLES = {
    "raw_orders":       "olist_orders_dataset.csv",
    "raw_customers":    "olist_customers_dataset.csv",
    "raw_order_items":  "olist_order_items_dataset.csv",
    "raw_order_payments": "olist_order_payments_dataset.csv",
    "raw_order_reviews": "olist_order_reviews_dataset.csv",
    "raw_products":     "olist_products_dataset.csv",
    "raw_sellers":      "olist_sellers_dataset.csv",
    "raw_geolocation":  "olist_geolocation_dataset.csv",
    "raw_category_translation": "product_category_name_translation.csv",
}

con = duckdb.connect(DB_PATH)
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

for table, filename in TABLES.items():
    filepath = os.path.join(DATA_DIR, filename).replace("\\", "/")
    print(f"Loading {table} from {filename}...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.{table} AS
        SELECT * FROM read_csv_auto('{filepath}', header=true)
    """)
    count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
    print(f"  → {count:,} rows loaded")

print("\nAll tables loaded successfully!")
con.close()
