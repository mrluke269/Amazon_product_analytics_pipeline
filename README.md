# Amazon Product Analysis Pipeline

An end-to-end data pipeline that extracts Amazon product data via API, loads it into Snowflake, transforms it using dbt, and visualizes insights through Power BI dashboards.

## Project Overview

This project demonstrates a complete analytics engineering workflow for analyzing Amazon dog food products. The pipeline identifies market opportunities by analyzing product ratings, sales volume, pricing, and customer reviews to surface products with strong potential but lower competition.

**Key Insight**: The analysis categorizes products into three segments (Opportunity, Highly Supplied, Unproven) and calculates a Quality Score to identify affordable, well-rated products with validation but not market saturation.

## Architecture

```
API (RapidAPI) → Python Scripts → Snowflake (Raw) → dbt (Transform) → Power BI (Visualize)
```

### Data Flow

1. **Extract**: Search API for products → Retrieve ASINs → Fetch detailed product data
2. **Load**: Incremental loading to Snowflake with deduplication
3. **Transform**: Multi-layered dbt models (staging → intermediate → marts)
4. **Visualize**: Power BI dashboards for product opportunity analysis

## Project Structure

```
C:\Users\Admin\PROJECT\AMAZON
├── data/
│   ├── asins_to_fetch.json
│   ├── product_details/
│   │   ├── {asin}.json
│   │   └── combined_products.json
│   └── temp/
└── scripts/
    ├── config.py
    ├── search_product.py
    ├── get_details.py
    └── load_to_snowflake.py
```

## Prerequisites

- Python 3.x
- Snowflake account with database `RAW` and schema `AMAZON_PRODUCT`
- RapidAPI key for Amazon product data API
- dbt Core installed
- Power BI Desktop

## Setup Instructions

### 1. Configure API Credentials

Create `config.py` in the scripts folder:

```python
# RapidAPI credentials
RAPIDAPI_KEY = "your_api_key"
RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"

# Snowflake configuration
snowflake_config = {
    'user': 'your_username',
    'password': 'your_password',
    'account': 'your_account',
    'warehouse': 'your_warehouse',
    'database': 'RAW',
    'schema': 'AMAZON_PRODUCT'
}

snowflake_table = 'product_details'
```

### 2. Install Python Dependencies

```bash
pip install requests snowflake-connector-python
```

### 3. Create Snowflake Table

```sql
CREATE TABLE RAW.AMAZON_PRODUCT.product_details (
    details_raw VARIANT,
    request_id VARCHAR,
    load_at TIMESTAMP_NTZ
);
```

### 4. Configure dbt

Update `profiles.yml` with your Snowflake credentials and set target database/schema for transformed models.

## Running the Pipeline

### Step 1: Search and Extract ASINs

```bash
python scripts/search_product.py
```

- Searches for "dog food" products on Amazon
- Extracts first 10 product ASINs
- Saves to `data/asins_to_fetch.json`

### Step 2: Fetch Product Details

```bash
python scripts/get_details.py
```

- Reads ASINs from JSON file
- Fetches detailed product data for each ASIN
- Saves individual JSON files and creates combined file
- Includes error handling for failed requests

### Step 3: Load to Snowflake

```bash
python scripts/load_to_snowflake.py
```

- Loads new products to Snowflake (deduplication by ASIN)
- Uses Snowflake stages for efficient bulk loading
- Creates temporary files and cleans up after load
- Prints load statistics (success/failure counts)

### Step 4: Transform with dbt

```bash
dbt run
```

Executes the transformation layers:
- **Staging**: Clean and extract raw JSON fields
- **Intermediate**: Parse prices, flatten rating distributions, clean sales volume
- **Marts**: Join all dimensions into analytical model with calculated metrics

All models use incremental materialization for efficiency.

### Step 5: Visualize in Power BI

1. Connect Power BI to Snowflake
2. Import `MART_AMAZON__PRODUCT_ANALYSIS` table
3. Use provided DAX formulas for product labeling and quality scoring

## dbt Transformation Logic

### Staging Layer (`stg_amazon__product_details`)
- Extracts fields from raw JSON variant column
- Casts to appropriate data types
- Incremental load based on `load_at` timestamp

### Intermediate Layer
- **`int_amazon__products_cleaned`**: Parses price fields, removes currency symbols
- **`int_amazon__product_ratings`**: Flattens rating distribution JSON into separate percentage columns
- **`int_amazon__sale_volume_cleaned`**: Parses sales volume strings (handles "10K" format)

### Mart Layer (`mart_amazon__product_analysis`)
- Joins all intermediate models
- Calculates derived metrics:
  - **Positive percentage**: Sum of 5-star and 4-star ratings
  - **Discount percentage**: Price reduction from original price

## Power BI Analytics

### Product Classification Logic

Products are categorized into three segments:

**Opportunity Products**:
- Reviews: Between Q1 and Median
- Sales: Between Q1 and Median  
- Rating: ≥ 4.0 stars
- *Interpretation*: Validated products with room to grow

**Highly Supplied Products**:
- Reviews > Median OR Sales > Median
- *Interpretation*: Saturated market with high competition

**Unproven Products**:
- Everything else
- *Interpretation*: Insufficient validation or demand

### Quality Score Metric

```
Quality Score = Star Rating / ((Reviews / 1000) × Price)
```

This metric identifies products that are:
- Affordable (lower price)
- Well-rated (high star rating)
- Validated but not oversaturated (moderate review count)

**Use Case**: Prioritize products with high Quality Scores in the "Opportunity" segment for potential market entry or inventory decisions.

## Key Features

### Incremental Processing
- All dbt models use incremental materialization
- Deduplication by ASIN in load script
- Efficient processing of only new/updated records

### Error Handling
- Try-except blocks in all Python scripts
- Failed API calls logged but don't stop execution
- Graceful handling of missing data

### Data Quality
- Source data validation in staging layer
- Type casting with appropriate defaults
- Null handling in metric calculations

### Scalability Considerations
- Modular script architecture for easy extension
- Parameterized queries in dbt
- Batch processing capability via temp files

## Design Decisions

**Why incremental models?**  
Product data changes infrequently. Incremental models reduce warehouse compute costs and processing time while maintaining data freshness.

**Why separate intermediate models?**  
Follows dimensional modeling best practices. Each intermediate model handles one transformation concern (price parsing, rating flattening, etc.), making the pipeline maintainable and testable.

**Why deduplication at load time?**  
Prevents duplicate ASIN records in the warehouse, ensuring data quality at the source rather than handling it in transformations.

**Why JSON as intermediate format?**  
API responses are naturally JSON. Storing raw JSON allows schema evolution and reprocessing without re-calling APIs.

## Sample Insights from Dashboard

Based on 50 products analyzed:
- **56% Highly Supplied**: Saturated markets (28 products)
- **20% Opportunity**: Growth potential (10 products)  
- **24% Unproven**: Insufficient data (12 products)

Median metrics:
- Sales Volume: 10,000 units/month
- Reviews: 10,115
- Price: $10

Top opportunity products identified with Quality Scores ranging from 0.01 to 0.11, representing affordable options with strong ratings and moderate competition.

## Future Enhancements

- Implement dbt tests for data quality validation
- Add orchestration with Apache Airflow or Fabric Pipelines
- Expand to multiple product categories
- Add historical tracking for trend analysis
- Implement CI/CD for dbt deployments
- Create automated alerting for new opportunities

## Technical Skills Demonstrated

- **Python**: API integration, file I/O, error handling, Snowflake connectivity
- **SQL**: Complex queries, window functions, JSON parsing, incremental patterns
- **dbt**: Layered transformation architecture, incremental models, Jinja templating
- **Data Modeling**: Dimensional modeling, staging → marts architecture
- **Cloud Data Warehouse**: Snowflake stages, variant data types, bulk loading
- **Business Intelligence**: DAX formulas, calculated columns, visual analytics

## License

This project is for educational and portfolio purposes.

## Contact

For questions or collaboration opportunities, please reach out via [your contact method].

---

**Project Status**: Complete and production-ready for portfolio demonstration
