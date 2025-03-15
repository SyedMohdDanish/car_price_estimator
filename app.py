# app.py

from flask import Flask, render_template, request
from models.price_estimator import get_estimated_price
from database.setup_db import setup_database

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            try:
                # Get form data
                year = request.form.get("year", "").strip()
                make = request.form.get("make", "").strip()
                model = request.form.get("model", "").strip()
                mileage = request.form.get("mileage", "").strip()

                # Debugging statements
                print(f"Received input: Year={year}, Make={make}, Model={model}, Mileage={mileage}")

                # Validate inputs
                if not year.isdigit() or not make or not model:
                    return render_template("index.html", error="Invalid input! Please enter valid values.")

                year = int(year)
                mileage = int(mileage) if mileage.isdigit() else None

                # Call price estimator function
                estimated_price, listings = get_estimated_price(year, make, model, mileage)

                # Debugging statement
                print(f"Estimated Price: {estimated_price}, Listings: {len(listings)}")

                if estimated_price is None:
                    return render_template("index.html", error="No data found for the given inputs.")

                # Render results page
                return render_template("results.html", estimated_price=estimated_price, listings=listings)

            except ValueError as e:
                print(f"ValueError: {e}")  # Debugging
                return render_template("index.html", error="Invalid input! Please enter valid year and mileage.")

        return render_template("index.html")

    except Exception as e:
        print(f"Unexpected error: {e}")  # Debugging
        return render_template("index.html", error="An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    try:
        print("Setting up database...")
        setup_database()
        print("Starting Flask server...")
        app.run(debug=True)
    except Exception as e:
        print(f"Critical error: Failed to start server. {e}")