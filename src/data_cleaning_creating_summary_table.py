# vendor_summary.py
import os
import pandas as pd
import logging
from sqlalchemy import create_engine

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Logging setup
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# DB engine
engine = create_engine("sqlite:///project.db")

def ingest_db(df: pd.DataFrame, table_name: str):
    """Ingest DataFrame into SQLite database (project.db)."""
    df.to_sql(
        table_name,
        con=engine,
        if_exists='replace',
        index=False,
        method="multi",
        chunksize=10000
    )

def create_vendor_summary(engine):
    """Merge tables to get overall vendor summary"""
    query = """
WITH FreightSummary AS (
    SELECT
        VendorNumber,
        SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
),
PurchaseSummary AS (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Price AS ActualPrice,      
        pp.Volume AS Volume,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description,
             p.PurchasePrice, pp.Price, pp.Volume
),
SalesSummary AS (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesDollars)  AS TotalSalesDollars,
        SUM(SalesPrice)    AS TotalSalesPrice,
        SUM(ExciseTax)     AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
)
SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,                
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
   AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC;
"""
    return pd.read_sql_query(query, engine)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich vendor summary data"""
    df['Volume'] = df['Volume'].astype(float)
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = df.apply(
        lambda r: (r['GrossProfit'] / r['TotalSalesDollars']) * 100 if r['TotalSalesDollars'] else 0,
        axis=1
    )
    df['StockTurnover'] = df.apply(
        lambda r: r['TotalSalesQuantity'] / r['TotalPurchaseQuantity'] if r['TotalPurchaseQuantity'] else 0,
        axis=1
    )
    df['SalesToPurchaseRatio'] = df.apply(
        lambda r: r['TotalSalesDollars'] / r['TotalPurchaseDollars'] if r['TotalPurchaseDollars'] else 0,
        axis=1
    )
    return df

if __name__ == "__main__":
    logging.info("Creating Vendor Summary Table…")
    summary_df = create_vendor_summary(engine)
    logging.info("\n%s", summary_df.head().to_string())

    logging.info("Cleaning Data…")
    clean_df = clean_data(summary_df)
    logging.info("\n%s", clean_df.head().to_string())

    logging.info("Ingesting data…")
    ingest_db(clean_df, 'vendor_sales_summary')
    logging.info("Completed.")
