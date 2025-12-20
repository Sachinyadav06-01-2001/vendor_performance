# Vendor Performance Analysis (End-to-End Data Analytics Project)

##  Project Overview
This project focuses on analyzing vendor performance using transactional, inventory, and sales data.
The objective is to evaluate vendor efficiency, profitability, inventory movement, and pricing effectiveness
to support data-driven procurement and sales decisions.

The project follows a complete analytics lifecycle:
Raw Data → Database → SQL Transformations → KPIs → Exploratory Data Analysis → Business Insights.

---

##  Business Problem
Organizations work with multiple vendors but often lack clear visibility into:
- Which vendors drive the most value
- Which brands underperform despite high margins
- Inventory turnover efficiency
- Pricing and bulk purchase impact
- Vendor contribution concentration (Pareto principle)

This project addresses these gaps by building a vendor-level analytical model.

---

##  Datasets Used
Raw data files include:
- Sales data
- Purchase data
- Vendor invoice data (freight cost)
- Purchase pricing data
- Beginning inventory
- Ending inventory

All raw files are ingested into a SQLite database for analysis.

---

##  Tech Stack
- **Python**
- **Pandas, NumPy**
- **SQL (SQLite)**
- **SQLAlchemy**
- **Matplotlib & Seaborn**
- **Jupyter Notebook**
- **Git & GitHub**

---

##  Project Workflow

### 1️⃣ Raw Data Ingestion
- Multiple CSV / Excel files are loaded using Pandas
- Data is ingested into a SQLite database (`project.db`)
- Chunk-based inserts are used for performance
- Logging is implemented for traceability

### 2️⃣ SQL-Based Vendor Summary
- SQL CTEs are used to modularize transformations
- Data from purchases, sales, freight, and pricing tables is joined
- Vendor-Brand level aggregation is created

### 3️⃣ KPI Engineering
The following business KPIs are calculated:
- **Gross Profit**
- **Profit Margin**
- **Stock Turnover**
- **Sales-to-Purchase Ratio**
- **Freight Cost Impact**

### 4️⃣ Exploratory Data Analysis (EDA)
EDA is performed on the final analytical table (`vendor_sales_summary`) instead of raw data to ensure
business-focused insights.

---

##  Key EDA & Analytical Techniques

### 🔹 Distribution & Outlier Analysis
- Histograms and boxplots for numerical features
- Identification of loss-making products and zero-sales inventory
- Detection of premium-priced products and freight cost variance

### 🔹 Correlation Analysis
- Strong correlation between purchase quantity and sales quantity
- Weak relationship between price and profitability
- Faster inventory turnover does not always imply higher margins

### 🔹 Vendor & Brand Performance
- Top vendors and brands by total sales
- Identification of low-sales but high-margin brands for promotion or pricing adjustment
- Brand-level scatter analysis for strategic targeting

### 🔹 Pareto Analysis (80/20 Rule)
- Top vendors contribute a majority of total purchases
- Cumulative contribution analysis using Pareto and donut charts

### 🔹 Bulk Pricing Impact
- Order sizes categorized into Small, Medium, and Large
- Larger order sizes receive significantly lower unit prices
- Demonstrates effectiveness of bulk pricing strategies

### 🔹 Statistical Analysis
- Confidence interval comparison between top-performing and low-performing vendors
- Hypothesis testing to evaluate differences in profit margins
- Insight: Low-sales vendors often maintain higher margins than high-volume vendors

---

## 📈 Key Business Insights
- A small number of vendors drive the majority of purchase value
- Several brands have high profit margins but low sales volumes, indicating promotion opportunities
- High sales volume does not always correlate with higher profitability
- Bulk purchasing significantly reduces unit cost and improves margins
- Freight costs vary widely across vendors, impacting overall profitability

---

## 📁 Project Structure

## Note: Full sales and purchase pricing datasets exceed GitHub size limits, so representative sample files are included.

