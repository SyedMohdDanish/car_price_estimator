# # models/price_estimator.py

import numpy as np
from sklearn.linear_model import LinearRegression
from database.db import get_db_connection

def fetch_listings(year, make, model, mileage = None):
    """Fetches matching car listings from the database."""
    if mileage:
        mileage_lower = max(0, mileage * 0.8)  # 20% below
        mileage_upper = mileage * 1.2  # 20% above
        query = """
            SELECT year, make, model, mileage, price, location FROM car_listings
            WHERE year = %s AND make = %s AND model = %s
            AND mileage BETWEEN %s AND %s
            ORDER BY ABS(mileage - %s) ASC  -- Prioritize closest mileage matches
            LIMIT 100
    """
        params = [year, make, model, mileage_lower,mileage_upper, mileage]
    else:
        query = """
            SELECT year, make, model, mileage, price, location FROM car_listings
            WHERE year = %s AND make = %s AND model = %s
    """
        params = [year, make, model]
    with get_db_connection() as conn, conn.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def calculate_estimated_price(listings, mileage):
    """Calculates the estimated price based on mileage adjustment."""
    if not listings:
        return None, []

    prices = np.array([row[4] for row in listings if row[4] is not None])  

    if len(prices) == 0:
        return None, []  # No valid data to calculate
    
    avg_price = np.mean(prices)  # Baseline average price

    if mileage is None:
        return round(avg_price, -2), listings[:100]


    mileages = np.array([row[3] for row in listings if row[3] is not None and row[3] > 0]).reshape(-1, 1)

    if len(prices) == 0:
        return None, []  # No valid data to calculate
    # Fit a simple linear regression model to estimate depreciation
    model = LinearRegression()
    model.fit(mileages, prices)  # Learn how mileage affects price
    
    # Predict estimated price for the given mileage
    estimated_price = model.predict(np.array([[mileage]]))[0]
    

    return round(estimated_price, -2), listings[:100]  

def get_estimated_price(year, make, model, mileage):
    """Main function to estimate car price."""
    try:
        listings = fetch_listings(year, make, model, mileage)
        return calculate_estimated_price(listings, mileage)
    except Exception as e:
        print(f"Error estimating price: {e}")
        return None, []
