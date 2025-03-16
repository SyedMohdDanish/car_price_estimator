import pytest
from app import CarPriceApp
from database.db import Database
from models.price_estimator import PriceEstimator

def test_db_connection():
    """Test if database connection is successful."""
    db = Database()
    conn = db.connect()
    assert conn is not None, "Database connection failed"
    conn.close()

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    App = CarPriceApp()
    App.app.config['TESTING'] = True
    with App.app.test_client() as client:
        yield client

def test_homepage(client):
    """Test if homepage loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Car Price Estimator" in response.data

def test_estimate_price():
    """Test price estimation logic with sample data."""
    year, make, model, mileage = 2020, "Toyota", "Camry", 30000
    estimator = PriceEstimator()
    estimated_price, listings = estimator.get_estimated_price(year, make, model, mileage)
    assert estimated_price is not None, "Price estimation failed"
    assert isinstance(estimated_price, (int, float)), "Estimated price should be a number"

def test_post_request(client):
    """Test form submission and results page rendering."""
    response = client.post('/', data={
        'year': '2020',
        'make': 'Toyota',
        'model': 'Camry',
        'mileage': '30000'
    })
    assert response.status_code == 200
    assert b"Estimated Price" in response.data or b"No data found" in response.data
