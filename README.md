# 🛒 Amazon Product Analysis Pipeline

> An end-to-end analytics engineering project that identifies market opportunities in Amazon's marketplace through automated data extraction, loading, transformation, and visualization.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![dbt](https://img.shields.io/badge/dbt-Core-orange.svg)](https://www.getdbt.com/)
[![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8.svg)](https://www.snowflake.com/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Visualization-F2C811.svg)](https://powerbi.microsoft.com/)

---
## [<img src="https://img.icons8.com/?size=512&id=19318&format=png" width="15">] Full Pipeline Walkthrough

[<img src="https://img.icons8.com/?size=512&id=19318&format=png" width="120">](https://youtu.be/1dQGbyfgDQI)

##  Project Overview

This portfolio project showcases a **complete analytics engineering workflow** for Amazon product analysis. The pipeline automatically:

✅ Extracts product data from Amazon API  
✅ Loads data incrementally to Snowflake  
✅ Transforms raw data through multi-layered dbt models  
✅ Surfaces actionable insights via Power BI dashboards  

###  Business Objectives

**The primary goal of this analysis is to identify a "sweet spot" in the market for a given product category. We aim to find products that are:**
- Strong customer validation (high ratings)
- Proven demand (have existing sales and reviews)
- Lower competition (not in the hyper-competitive, "highly supplied" segment)
- Affordable pricing

The final dashboard provides a prioritized list of these "Opportunity" products to guide product research and investment decisions.

### Solution

A data-driven classification system that segments products into:

| Segment | Definition |
|---------|-----------|
| 🟢 **Opportunity** | Validated products with growth potential |
| 🟡 **Highly Supplied** | Saturated markets with high competition |
| 🔴 **Unproven** | Insufficient validation or demand |

---

##  Architecture

<img width="927" height="343" alt="image" src="https://github.com/user-attachments/assets/d024fa20-d579-4558-90f1-bc26c8f3fcbf" />


###  Data Flow Pipeline

<img width="1619" height="1099" alt="image" src="https://github.com/user-attachments/assets/66437620-ffdb-4626-9900-cc31540ac2c2" />


---

##  Project Structure

<details>
<summary>📁 <b>Click to expand full project structure</b></summary>

<pre>
AMAZON/
├── data/
│   ├── asins_to_fetch.json          # List of product ASINs to fetch
│   ├── product_details/
│   │   ├── {asin}.json              # Individual product JSON files
│   │   └── combined_products.json   # All products in one file
│   └── temp/                        # Temporary files for Snowflake loading
│
├── scripts/
│   ├── config.py                    # API keys & Snowflake credentials
│   ├── search_product.py            # Step 1: Search & extract ASINs
│   ├── get_details.py               # Step 2: Fetch product details
│   └── load_to_snowflake.py         # Step 3: Load to warehouse
│
└── dbt_project/
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_amazon__product_details.sql
│   │   ├── intermediate/
│   │   │   ├── int_amazon__products_cleaned.sql
│   │   │   ├── int_amazon__product_ratings.sql
│   │   │   └── int_amazon__sale_volume_cleaned.sql
│   │   └── marts/
│   │       └── mart_amazon__product_analysis.sql
│   └── _amazon__sources.yml
│
├── dashboard/
│   └── product_recommendation
</pre>

</details>
---

##  Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
|  Python | 3.x | ETL scripting |
|  Snowflake | Account | Data warehouse |
|  dbt Core | Latest | Data transformation |
|  Power BI | Desktop | Visualization |
|  RapidAPI | Account | Amazon product data |

---

##  Setup Instructions

### Step 1️⃣: Configure API Credentials

Create `scripts/config.py`:

```python
#  RapidAPI credentials
RAPIDAPI_KEY = "your_api_key_here"
RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"

#  Snowflake configuration
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

### Step 2️⃣: Install Python Dependencies

```bash
pip install requests snowflake-connector-python
```

### Step 3️⃣: Create Snowflake Table

```sql
CREATE TABLE RAW.AMAZON_PRODUCT.product_details (
    details_raw VARIANT,      -- Raw JSON data
    request_id VARCHAR,        -- API request identifier
    load_at TIMESTAMP_NTZ      -- Load timestamp
);
```

### Step 4️⃣: Configure dbt

Update `profiles.yml` with your Snowflake credentials and set target schemas for transformed models.

---

##  Running the Pipeline

###  Step 1: Search and Extract ASINs

```bash
python scripts/search_product.py
```

**What it does:**
-  Searches Amazon for queried products
-  Extracts product ASINs
-  Saves to `data/asins_to_fetch.json`

**Output:**
```json
[
  "B09TFNQM7Z",
  "B0C9QK9BZF",
  "B09Y85LJFR",
  ...
]
```

---

###  Step 2: Fetch Product Details

```bash
python scripts/get_details.py
```

**What it does:**
-  Reads ASINs from JSON file
-  Fetches detailed product data for each ASIN
-  Saves individual files + combined file
-  Error handling for failed requests

**Console output:**
```
Starting to fetch 10 products...
✅ Saved B09TFNQM7Z to PROJECT\AMAZON\data\product_details
✅ Saved B0C9QK9BZF to PROJECT\AMAZON\data\product_details
...
✅ Combined product details saved to combined_products.json
```

---

###  Step 3: Load to Snowflake

```bash
python scripts/load_to_snowflake.py
```

**What it does:**
-  Checks for existing ASINs in Snowflake
-  Identifies new products to load
-  Bulk loads via Snowflake COPY command
-  Cleans up temporary files

**Load process:**

<img width="517" height="1569" alt="image" src="https://github.com/user-attachments/assets/e758ad69-bdc7-4a48-8c53-505d42a554aa" />


---

### Step 4: Transform with dbt


**Transformation layers executed:**

```
Layer 1: STAGING
├── stg_amazon__product_details
│   └── Extract JSON fields → Type casting
│
Layer 2: INTERMEDIATE
├── int_amazon__products_cleaned
│   └── Parse prices → Remove $ symbols
├── int_amazon__product_ratings  
│   └── Flatten rating JSON → Separate columns
└── int_amazon__sale_volume_cleaned
    └── Parse "10K" format → Numeric values
│
Layer 3: MARTS
└── mart_amazon__product_analysis
    └── Join all → Calculate metrics → Final table
```

**All models use incremental materialization for efficiency!**

---

###  Step 5: Visualize in Power BI

1.  Connect Power BI to Snowflake
2.  Import `MART_AMAZON__PRODUCT_ANALYSIS` table
3.  Use DAX formulas for analytics

---



#### Segment Definitions

| Segment | Criteria | Interpretation |
|---------|----------|----------------|
| 🟢 **Opportunity** | • Reviews: Q1 to Median<br>• Sales: Q1 to Median<br>• Rating ≥ 4.0 | **Sweet spot!** Validated by customers but not oversaturated |
| 🟡 **Highly Supplied** | • Reviews > Median OR<br>• Sales > Median | High competition, harder to differentiate |
| 🔴 **Unproven** | • Everything else | Low validation or demand |

#### DAX Formula for Classification

```dax
Product_Status = 
SWITCH(
    TRUE(),
    
    -- OPPORTUNITY: Validated but not saturated
    MART_AMAZON__PRODUCT_ANALYSIS[num_rating] >= [Q1_Reviews_column]
        && MART_AMAZON__PRODUCT_ANALYSIS[num_rating] <= [Median_Reviews_column]
        && MART_AMAZON__PRODUCT_ANALYSIS[sales_volume] >= [Q1_Sales_Column]
        && MART_AMAZON__PRODUCT_ANALYSIS[sales_volume] <= [Median_Sales_column]
        && MART_AMAZON__PRODUCT_ANALYSIS[PRODUCT_STAR_RATING] >= 4,
        "Opportunity",
    
    -- HIGHLY SUPPLIED: High reviews OR high sales
    MART_AMAZON__PRODUCT_ANALYSIS[num_rating] > [Median_Reviews_column]
        || MART_AMAZON__PRODUCT_ANALYSIS[sales_volume] > [Median_Sales_column],
        "Highly Supplied",
    
    -- UNPROVEN: Everything else
    "Unproven"
)
```

---

### 🎯 Quality Score Metric

The Quality Score identifies the **best value products** by balancing price, rating, and validation:

```
Quality Score = Star Rating / ((Reviews / 1000) × Price)
```

**What it rewards:**
-  **High ratings** → Better quality
-  **Lower prices** → More affordable  
-  **Moderate reviews** → Validated but not oversaturated

**Example calculation:**

| Product | Rating | Reviews | Price | Quality Score | Interpretation |
|---------|--------|---------|-------|---------------|----------------|
| Product A | 4.5 | 5,788 | $6.99 | **0.11** | 🟢 Highest chance to make profit- start with these products |
| Product B | 4.6 | 9,976 | $9.98 | **0.05** | 🟡 Start with these after |
| Product C | 4.7 | 30,000 | $20.00 | **0.01** | 🔴 Lowest chance, research last |

#### DAX Formula for Quality Score

```dax
Quality_Score_WithPrice = 
MART_AMAZON__PRODUCT_ANALYSIS[PRODUCT_STAR_RATING] / 
(
    (MART_AMAZON__PRODUCT_ANALYSIS[num_rating] / 1000) * 
    MART_AMAZON__PRODUCT_ANALYSIS[product_price]
)
```

---

###  Dashboard Insights

#### Market Overview

![Project Overview](dashboard/overview.png)

#### Recommendations
![Recommendations](dashboard/details.png)



### Strategic Opportunities

**10 Opportunity Products Identified:**

- ✅ Proven demand (sales: 6,000-10,000/month)
- ✅ Strong ratings (4.0-4.7 stars)
- ✅ Customer validation (3,600-10,000 reviews)
- ✅ Not oversaturated
- ✅ Affordable ($6.99-$87.99 range)

**Recommended Action:** Focus on products with highest Quality Score

---

##  Design Decisions & Rationale

### Why Incremental Models?

```
Traditional Full Refresh:          Incremental Approach:
───────────────────────            ─────────────────────

Day 1: Process 50 records          Day 1: Process 50 records
Day 2: Process 50 records          Day 2: Process 5 new records
Day 3: Process 50 records          Day 3: Process 3 new records
...                                ...

Total: 50 × 365 = 18,250 records   Total: 50 + (8 × 365) = 2,970 records

❌ High compute costs              ✅ 83% cost reduction
❌ Slower processing               ✅ Faster runs
❌ Unnecessary reprocessing        ✅ Only process changes
```

**Conclusion:** Product data changes infrequently. Incremental models optimize for cost and speed.

---

### Why Separate Intermediate Models?

```
Option 1: Single Transformation              Option 2: Layered Transformations
──────────────────────────                   ────────────────────────────────

┌─────────────────────────────┐             ┌──────────────────┐
│  One Giant SQL Query        │             │  Price Cleaning  │
│                             │             └────────┬─────────┘
│  • Parse prices             │                      │
│  • Flatten ratings          │             ┌────────▼─────────┐
│  • Clean sales volume       │             │ Rating Flattening│
│  • Join everything          │             └────────┬─────────┘
│  • Calculate metrics        │                      │
│                             │             ┌────────▼─────────┐
│  500+ lines of SQL          │             │  Sales Parsing   │
│  Hard to debug              │             └────────┬─────────┘
│  No reusability             │                      │
│                             │             ┌────────▼─────────┐
└─────────────────────────────┘             │   Final Mart     │
                                            └──────────────────┘
❌ Monolithic                               ✅ Modular
❌ Hard to maintain                         ✅ Easy to test
❌ Can't reuse logic                        ✅ Reusable components
```

**Conclusion:** Each intermediate model handles one concern. Follows dimensional modeling best practices.

---

### Why Deduplication at Load Time?

```
Option 1: Load Duplicates               Option 2: Deduplicate at Load
────────────────────                    ──────────────────────────

API → Load everything                   API → Check existing ASINs
      ↓                                       ↓
  Snowflake (duplicates)                  Snowflake (unique only)
      ↓                                       ↓
  Handle in dbt                           Clean from start
      ↓
  Higher storage costs

❌ Duplicates in warehouse              ✅ Data quality at source
❌ Need QUALIFY in queries              ✅ Simple downstream queries
❌ Higher storage costs                 ✅ Lower storage costs
```

**Conclusion:** Prevent duplicates at ingestion rather than managing in transformations.

---


## 💼 Technical Breakdown

This project showcases core analytics engineering competencies aligned with the modern data stack:

###  Python for Data Engineering

| Skill | Implementation | File |
|-------|----------------|------|
| **API Integration** | `requests` library with headers & error handling | `search_product.py`, `get_details.py` |
| **File I/O Operations** | Read/write JSON, path management with `pathlib` | All scripts |
| **Error Handling** | Try-except blocks, graceful failures | `get_details.py` |
| **Database Connectivity** | Snowflake connector, parameterized queries | `load_to_snowflake.py` |
| **Data Structures** | Lists, dictionaries, JSON manipulation | All scripts |
| **State Management** | Track loaded ASINs, avoid duplicates | `load_to_snowflake.py` |

---

###  SQL & Data Modeling

| Skill | Implementation | Example |
|-------|----------------|---------|
| **JSON Parsing** | Extract fields from VARIANT type | `details_raw:asin::varchar` |
| **CTEs** | Structured queries with `WITH` clauses | All dbt models |
| **Type Casting** | Convert strings to proper types | `::DECIMAL(10,2)` |
| **Joins** | LEFT JOIN multiple tables | `mart_amazon__product_analysis.sql` |
| **Incremental Logic** | `{% if is_incremental() %}` | All dbt models |
| **Aggregations** | SUM, MAX calculations | Metric calculations |

---

###  dbt

| Skill | Implementation | Impact |
|-------|----------------|--------|
| **Project Structure** | Staging → Intermediate → Marts | Clean architecture |
| **Incremental Models** | `materialized='incremental'` |  Optimization |
| **Sources** | `{{ source('amazon', 'table') }}` | Lineage tracking |
| **Refs** | `{{ ref('model_name') }}` | Dependency management |
| **Unique Keys** | `unique_key='asin'` | Deduplication |
| **Documentation** | YML files for metadata | Self-documenting |

**Architecture Visualization:**
```
dbt Project Structure:
├── 📂 models/
│   ├── 📂 staging/          ← Raw data extraction
│   │   └── stg_*.sql
│   ├── 📂 intermediate/     ← Business logic
│   │   └── int_*.sql
│   └── 📂 marts/            ← Analytics-ready
│       └── mart_*.sql
└── 📄 _sources.yml          ← Source definitions
```

---

###  Cloud Data Warehouse (Snowflake)

| Skill | Implementation | Benefit |
|-------|----------------|---------|
| **VARIANT Data Type** | Store semi-structured JSON | Schema flexibility |
| **Stages** | `PUT` files to user stage | Efficient bulk loading |
| **COPY Command** | Bulk load from stage | High performance |
| **SQL Functions** | `current_timestamp()`, `NULLIF()` | Data quality |
| **Bulk Operations** | Process multiple records at once | Scalability |

**Load Process:**
```sql
-- 3-step load pattern
1. PUT file://temp.json @~ AUTO_COMPRESS=false
2. COPY INTO table FROM @~/temp.json  
3. REMOVE @~/temp.json
```

---

###  Business Intelligence (Power BI)

| Skill | Implementation | Purpose |
|-------|----------------|---------|
| **DAX Formulas** | `SWITCH()`, calculated columns |
| **Data Modeling** | Connect to Snowflake |
| **Visualizations** | Insights |
| **Calculated Measures** | Quality Score formula | Custom analytics |


---

###  Analytics Engineering Best Practices

| Practice | Implementation | Rationale |
|----------|----------------|-----------|
| **Layered Architecture** | Staging → Intermediate → Marts | Separation of concerns |
| **Incremental Models** | Process only new data | Cost & performance |
| **Deduplication** | Check before load | Data quality |
| **Error Handling** | Try-except in all scripts | Reliability |
| **Documentation** | README + code comments | Maintainability |
| **Version Control** | Git-ready project structure | Collaboration |
| **Testing** | Data validation at each layer | Trust in data |
| **Modularity** | Reusable components | Scalability |

---

## 📧 Contact & Links

**GitHub:** [github.com/mrluke269]  
**Email:** [luke.trmai@gmail.com]

---

## Project Status

Status: ✅ COMPLETED    

- All pipeline stages functional

- Documentation comprehensive
  
- Dashboard deployed



<div align="center">

### 

**Luke M**

</div>
