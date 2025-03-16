import numpy as np
from sklearn.linear_model import LinearRegression
from database.db import Database

class PriceEstimator:
    def __init__(self):
        self.db = Database()
    
    def fetch_listings(self, year, make, model, mileage=None):
        """Fetches matching car listings from the database."""
        try:
            conn = self.db.connect()
            with conn.cursor() as cursor:
                if mileage:
                    mileage_lower, mileage_upper = max(0, mileage * 0.8), mileage * 1.2
                    query = """
                        SELECT year, make, model, mileage, price, location FROM car_listings
                        WHERE year = %s AND make = %s AND model = %s
                        AND mileage BETWEEN %s AND %s
                        ORDER BY ABS(mileage - %s) ASC
                        LIMIT 100;
                    """
                    cursor.execute(query, [year, make, model, mileage_lower, mileage_upper, mileage])
                else:
                    query = """
                        SELECT year, make, model, mileage, price, location FROM car_listings
                        WHERE year = %s AND make = %s AND model = %s;
                    """
                    cursor.execute(query, [year, make, model])
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching listings: {e}")
            return []
        finally:
            self.db.close()

    def calculate_estimated_price(self, listings, mileage):
        """Calculates the estimated price based on mileage adjustment."""
        if not listings:
            return None, []

        prices = np.array([row[4] for row in listings if row[4] is not None])
        if prices.size == 0:
            return None, []

        avg_price = np.mean(prices)
        if mileage is None:
            return round(avg_price, -2), listings[:100]

        mileages = np.array([row[3] for row in listings if row[3] is not None and row[3] > 0]).reshape(-1, 1)
        model = LinearRegression()
        model.fit(mileages, prices)
        estimated_price = model.predict(np.array([[mileage]]))[0]
        return round(estimated_price, -2), listings[:100]

    def get_estimated_price(self, year, make, model, mileage):
        """Main function to estimate car price."""
        listings = self.fetch_listings(year, make, model, mileage)
        return self.calculate_estimated_price(listings, mileage)