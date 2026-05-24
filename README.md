# Olist E-Commerce Analytics

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.8.0-FF694B?logo=dbt&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-1.5.3-FFF000?logo=duckdb&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.7-3F4F75?logo=plotly&logoColor=white)
[![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Spaces-FFD21E?logo=huggingface&logoColor=black)](https://evgeniimatveevusa-olist-analytics.hf.space)

End-to-end analytics pipeline built on **100,000+ Brazilian e-commerce orders** — from raw CSVs to production dbt models, 54 data quality tests, and a live Streamlit dashboard.

> "Built a full analytics engineering stack from scratch: ingestion → dbt modeling → data quality → visualization."

**[Live Demo → HuggingFace Spaces](https://evgeniimatveevusa-olist-analytics.hf.space)**

---

## Screenshots

<details>
<summary>📊 Overview — KPI Cards & Revenue Trend</summary>

![Overview](assets/Overview.png)

</details>

<details>
<summary>💰 Revenue — Monthly Timeline & Top Categories</summary>

![Revenue](assets/Revenue.png)

</details>

<details>
<summary>🚚 Delivery — On-Time Rate & State Analysis</summary>

![Delivery](assets/Delivery.png)

</details>

<details>
<summary>👥 Customers — LTV Segments & Quintiles</summary>

![Customers](assets/Customers.png)

</details>

<details>
<summary>🏪 Sellers — Performance Scatter & Rankings</summary>

![Sellers](assets/Sellers.png)

</details>

<details>
<summary>⭐ Reviews — Score Trends & Volume</summary>

![Reviews](assets/Reviews.png)

</details>

---

## Key Findings

| Metric | Value |
|--------|-------|
| Total gross revenue | **$13,221,498** |
| Total delivered orders | **96,478** |
| Unique customers | **93,357** |
| Avg order value | **$124.96** |
| On-time delivery rate | **91.9%** |
| Avg delivery time | **12.5 days** |
| Avg review score | **3.99 / 5.0** |
| One-time customers | **97%** — massive retention opportunity |
| Slowest state (delivery) | **AM (Amazonas)** → 25+ days avg |
| Top category by revenue | **health_beauty** |
| Revenue growth | **$0 → $1M/month** in 18 months (2016→2018) |
| dbt models | **13 models** · **54 tests** · **100% passing** |

---

## Architecture

```
Kaggle CSVs (9 files · 1.5M rows)
        ↓  Python ingestion
   DuckDB (raw schema)
        ↓  dbt run
   staging/  ← 8 views · clean + typed
        ↓  dbt run
   marts/    ← 5 tables · business logic
        ↓  Streamlit
   Dashboard (6 pages · Plotly)
        ↓  Docker
   HuggingFace Spaces (always-on)
```

---

## dbt Lineage

```
raw.raw_orders ──────────────┐
raw.raw_customers ───────────┤──► stg_orders ──────────────┐
raw.raw_order_items ─────────┤──► stg_customers ───────────┤──► mart_revenue
raw.raw_order_payments ──────┤──► stg_order_items ─────────┤──► mart_delivery_analysis
raw.raw_order_reviews ───────┤──► stg_order_payments ──────┤──► mart_customer_ltv
raw.raw_products ────────────┤──► stg_order_reviews ───────┤──► mart_seller_performance
raw.raw_sellers ─────────────┤──► stg_products ────────────┤──► mart_reviews
raw.raw_geolocation ─────────┘──► stg_sellers              │
raw.raw_category_translation ───► stg_geolocation ─────────┘
```

**54 data quality tests:** `not_null` · `unique` · `accepted_values` · all passing ✅

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Data source | Kaggle — Olist Brazilian E-Commerce (public) |
| Database | DuckDB 1.5.3 (embedded, zero config) |
| Transformation | dbt-core 1.8 + dbt-duckdb adapter |
| Data quality | dbt tests (54 assertions) |
| Dashboard | Streamlit + Plotly |
| Containerization | Docker + Docker Compose |
| Deployment | HuggingFace Spaces (Docker SDK) |
| DB Explorer | DBeaver |

---

## Dashboard Pages

**Overview** — 7 KPI cards · Monthly revenue area chart · Top 10 categories bar

**Revenue** — Monthly gross revenue · Order volume · Category breakdown (Top 15)

**Delivery** — On-time vs late donut · Avg days by state heatmap · On-time rate by state

**Customers** — Segment pie (one-time / returning / loyal) · LTV quintile bars · Segment table

**Sellers** — Revenue vs rating scatter (bubble = order volume) · Top 10 table · Sellers by state

**Reviews** — Avg score trend · Review volume · Positive rate over time

---

## Quick Start

### Option A — Docker (recommended)

```bash
git clone https://github.com/evgeniimatveev/olist-e-commerce-analytics.git
cd olist-e-commerce-analytics

# Place Kaggle CSVs in data/ folder first (see "Load Your Own Data" below)
docker compose up --build
```
Open **http://localhost:8501**

### Option B — Python

```bash
git clone https://github.com/evgeniimatveev/olist-e-commerce-analytics.git
cd olist-e-commerce-analytics

pip install duckdb --only-binary=:all:
pip install -r requirements.txt

# Place CSVs in data/ folder, then:
python scripts/load_raw.py
dbt run --profiles-dir .

python -m streamlit run dashboard/app.py
```

---

## Load Your Own Data

1. **Download dataset** from Kaggle: search `"olist brazilian ecommerce"`
2. **Place all 9 CSVs** in `data/` folder:
   ```
   data/
   ├── olist_orders_dataset.csv
   ├── olist_customers_dataset.csv
   ├── olist_order_items_dataset.csv
   ├── olist_order_payments_dataset.csv
   ├── olist_order_reviews_dataset.csv
   ├── olist_products_dataset.csv
   ├── olist_sellers_dataset.csv
   ├── olist_geolocation_dataset.csv
   └── product_category_name_translation.csv
   ```
3. **Run the pipeline:**
   ```bash
   python scripts/load_raw.py   # CSVs → DuckDB raw schema
   dbt run --profiles-dir .     # raw → staging → marts
   dbt test --profiles-dir .    # 54 quality checks
   ```
4. **Launch dashboard:**
   ```bash
   python -m streamlit run dashboard/app.py
   ```

---

## Project Structure

```
olist-e-commerce-analytics/
├── data/                        # CSVs here (gitignored)
├── models/
│   ├── staging/                 # 8 views — clean + typed
│   │   ├── _sources.yml
│   │   ├── _staging_models.yml  # 30+ data tests
│   │   ├── stg_orders.sql
│   │   ├── stg_customers.sql
│   │   ├── stg_order_items.sql
│   │   ├── stg_order_payments.sql
│   │   ├── stg_order_reviews.sql
│   │   ├── stg_products.sql
│   │   ├── stg_sellers.sql
│   │   └── stg_geolocation.sql
│   └── marts/                   # 5 tables — business logic
│       ├── _marts_models.yml    # 24 data tests
│       ├── mart_revenue.sql
│       ├── mart_delivery_analysis.sql
│       ├── mart_customer_ltv.sql
│       ├── mart_seller_performance.sql
│       └── mart_reviews.sql
├── scripts/
│   └── load_raw.py              # CSV → DuckDB ingestion
├── dashboard/
│   ├── app.py                   # Streamlit (6 pages)
│   └── db.py                    # DuckDB query layer
├── assets/                      # Screenshots
├── .streamlit/
│   └── config.toml
├── dbt_project.yml
├── profiles.yml
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Data Schema

| Table (raw) | Rows | Description |
|-------------|------|-------------|
| `raw_orders` | 99,441 | Order lifecycle — status, timestamps |
| `raw_order_items` | 112,650 | Line items — price, freight, seller |
| `raw_order_payments` | 103,886 | Payments — type, installments, value |
| `raw_order_reviews` | 99,224 | Customer reviews — score, text |
| `raw_customers` | 99,441 | Customer locations |
| `raw_products` | 32,951 | Product catalog + categories |
| `raw_sellers` | 3,095 | Seller locations |
| `raw_geolocation` | 1,000,163 | Zip code → lat/lng |
| `raw_category_translation` | 71 | PT → EN category names |

---

## Insights That Surprised Me

**97% of customers buy only once** — Olist's biggest business problem is right there in the data. Retention is near zero, which makes avg order value and delivery experience critical.

**AM (Amazonas) takes 25+ days** — Geography is destiny in Brazil. The Amazon region has drastically longer delivery times — a real operational challenge visible in the data.

**Revenue grew 0 → $1M/month in 18 months** — The platform was in hyper-growth mode from late 2016 through 2018. The monthly trend tells the whole story at a glance.

**91.9% on-time rate hides state-level extremes** — Nationally the number looks good, but broken down by state, some regions are consistently late — a finding only visible with proper dimensional modeling.

---

## Skills Demonstrated

- **Analytics Engineering** — dbt project with staging + marts layers, `ref()` dependency graph
- **Data Modeling** — star schema design, dimensional thinking, denormalization tradeoffs
- **Data Quality** — 54 automated tests: `not_null`, `unique`, `accepted_values`
- **SQL** — window functions (`ntile`, `datediff`), CTEs, multi-table joins, aggregations
- **Data Engineering** — CSV ingestion pipeline, DuckDB schema design, environment-agnostic paths
- **Visualization** — Streamlit multi-page app, Plotly charts (area, bar, scatter, donut, pie)
- **DevOps** — Docker containerization, Docker Compose, HuggingFace Spaces deployment

---

## Availability

| Layer | Detail |
|-------|--------|
| Hosting | HuggingFace Spaces (Docker SDK) |
| Uptime | 24/7 — HF Spaces does not sleep |
| Database | DuckDB embedded — bundled in Docker image |
| Build | Pipeline runs at image build time (`load_raw` + `dbt run`) |

---

*Data: Olist Brazilian E-Commerce · Kaggle public dataset · 2016–2018*
