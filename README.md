# Car Market Value Estimation 

## Project Overview
This project is a Flask-based internal search interface designed to estimate the average market value of car based on the year, make, and model. The application allows users to input car details and returns an estimated market price along with relevant sample listings. The data is processed from a provided Full Market Data file and stored in a PostgreSQL database.

## Algorithm & Evaluation Techniques
The market value estimation algorithm follows these steps:
1. **Data Ingestion**: The provided Full Market Data file is processed and stored in a PostgreSQL database.
2. **User Query Processing**: The search interface takes inputs like car year, make, and model.
3. **Filtering & Aggregation**:
   - The database is queried for relevant car listings.
   - The average market value is computed using mean calculations.
   - Linear regression is used to estimate the drop of price when mileage is mentioned.
4. **Result Display**: The estimated market value of car along with 100 sample listings is displayed to the user.

## Database Schema
The PostgreSQL database schema consists of the following tables:

- **car_listings** (Main data table containing car listings)
  - `id` (Primary Key, Auto-incremented)
  - `year` (Integer, Vehicle manufacturing year)
  - `make` (Text, Vehicle manufacturer)
  - `model` (Text, Vehicle model)
  - `price` (Float, Listed price of the vehicle)
  - `mileage` (Integer, Mileage of the vehicle)
  - `location` (Text, Location of the listing)

## Data Flow
1. **Initialization**: The application starts by loading the required Flask modules and connecting to the PostgreSQL database.
2. **Data Import**: The Full Market Data file is processed and inserted into the `car_listings` table.
3. **User Interaction**:
   - The user inputs a car's year, make, and model on the web interface.
   - The backend processes the query, filtering relevant car listings.
4. **Computation**:
   - The average market value is computed and returned.
   - If mileage is not mentioned then average prie is returned otherwise price is adjusted acording to mileage using linear      regression.
5. **Result Presentation**:
   - The estimated price and relevant listings are displayed on the front-end.

## Test Cases Explanation

1. Database Connection Test (test_db_connection)

   - Purpose: Ensures the PostgreSQL database connection is established successfully.

2. Flask Test Client Fixture (client)

   - Purpose: Provides a test client to simulate HTTP requests to the Flask app.

3. Homepage Test (test_homepage)

   - Purpose: Ensures that the homepage loads successfully.

4. Price Estimation Test (test_estimate_price)

   - Purpose: Verifies the core logic of estimating vehicle prices.

5. Form Submission & Results Test (test_post_request)

   - Purpose: Tests whether the form submission and results page rendering work correctly.

## Suggestions to Improve the Application Design & Architecture
1. Improve Data Processing & Handling

   - Implement caching (e.g. Redis) to reduce database queries and improve performance.
2. Enhance API Design

   - Convert the web app into a REST API using Flask-RESTful or FastAPI, allowing other applications to consume the estimation service.
   - Implement pagination for search results to improve performance.
3. Improve Database Performance

   - Add indexes on frequently queried fields (year, make, model).
4. Improve UI & Frontend

   - Use a frontend framework like React.js or Vue.js to make the interface more dynamic and responsive.
5. Implement Logging & Monitoring

   - Use Flask logging and tools like AWS CloudWatch or ELK Stack (Elasticsearch, Logstash, Kibana) to monitor app performance and  errors.



## Setup Instructions
To run this project on your local machine, follow these steps:

### 1. Clone the Repository
```
git clone <githuburl>
cd <desired folder>
```

### 2. Set Up a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database
1. Install PostgreSQL if not already installed.
2. Create a new database:
   ```
   psql -U postgres -c "CREATE DATABASE car_prices;"

   ```
### 5. Create .env file for database credentials
1. '''
    DB_NAME=databasename
    DB_USER=postgres
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432
   '''
    or 
   '''
   If want to run the code just to check, hardcode the db value in config.py. No need to create .env

### 6. Run the Application

python app.py

### NOTE : If using docker
1. Minor change in .env if ccreating or in config if do not want create .env. In DB_HOST use db instead of localhost. eg DB_HOST=db
2. docker-compose build
3. docker-compose up -d


If running for the first time it might take some time to insert the data into table. This is just for the first time after it will not take time unless data is deleted from the table.

Open your browser and go to `http://127.0.0.1:5000/` to use the search interface.

---

This completes the setup. You can now use the application to estimate car market values!

