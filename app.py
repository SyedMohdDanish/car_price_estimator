from flask import Flask, render_template, request
from models.price_estimator import PriceEstimator
from database.setup_db import SetupDatabase
from database.db import Database
from config import DATA_FILE_PATH

class CarPriceApp:
    def __init__(self):
        try:
            self.app = Flask(__name__)
            self.db = Database()
            self.estimator = PriceEstimator()
            self.setup_db = SetupDatabase(self.db)
            self.setup_routes()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize the application -> {e}")
    
    def setup_routes(self):
        """Sets up Flask routes."""
        @self.app.route("/", methods=["GET", "POST"])
        def index():
            try:
                if request.method == "POST":
                    form_data = {k: v.strip() for k, v in request.form.items()}
                    year = form_data.get("year", "")
                    make = form_data.get("make", "")
                    model = form_data.get("model", "")
                    mileage = form_data.get("mileage", "")

                    if not year.isdigit() or not make or not model:
                        return render_template("index.html", error="Invalid input! Please enter valid values.")

                    year, mileage = int(year), int(mileage) if mileage.isdigit() else None
                    estimated_price, listings = self.estimator.get_estimated_price(year, make, model, mileage)
                    if estimated_price is None:
                        return render_template("index.html", error="No data found for the given inputs.")
                    return render_template("results.html", estimated_price=estimated_price, listings=listings)

                return render_template("index.html")
            except Exception as e:
                return render_template("index.html", error=f"An internal error occurred. Please try again - {e}")
    
    def run(self):
        try:
            print("Setting up database...")
            self.setup_db.setup_database(DATA_FILE_PATH)
            print("Starting Flask server...")
            self.app.run(debug=True)
        except Exception as e:
            print(f"Error: Application failed to start - {e}")

if __name__ == "__main__":
    try:
        CarPriceApp().run()
    except Exception as e:
        print(f"Critical error: Unable to start the application - {e}")