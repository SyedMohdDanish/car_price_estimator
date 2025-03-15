#database/setup_db.py

import os
import pandas as pd
import psycopg2
import time
from database.db import get_db_connection

TABLE_NAME = "car_listings"

def create_table():
    """Creates the car_listings table if it does not exist."""
    query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            year INT NOT NULL,
            make VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            mileage INT,
            price INT,
            location VARCHAR(150)
        );
    """
    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            print(f"Table '{TABLE_NAME}' ensured.")
    except psycopg2.Error as e:
        print(f"Database error while creating table: {e}")

def insert_data(df):
    """Inserts data from a DataFrame into the PostgreSQL table."""
    if df.empty:
        print("No data to insert.")
        return

    records = df.to_records(index=False).tolist()
    query = f"""
        INSERT INTO {TABLE_NAME} (year, make, model, mileage, price, location)
        VALUES (%s, %s, %s, %s, %s, %s);
    """

    try:
        with get_db_connection() as conn, conn.cursor() as cursor:
            start_time = time.time()  # Start timing
            cursor.executemany(query, records)
            conn.commit()
            end_time = time.time()  # End timing
            elapsed_time = end_time - start_time
            print(f"{len(records)} records inserted successfully in {elapsed_time:.4f} seconds.")
    except psycopg2.Error as e:
        print(f"Database error while inserting data: {e}")

def load_data(file_path):
    """Reads and processes the dataset."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path, delimiter="|", encoding="utf-8", on_bad_lines="skip")
        df = df[['year', 'make', 'model', 'listing_mileage', 'listing_price', 'dealer_city', 'dealer_state']]
        df['location'] = df['dealer_city'].astype(str) + ", " + df['dealer_state'].astype(str)
        df.rename(columns={'listing_mileage': 'mileage', 'listing_price': 'price'}, inplace=True)
        df.drop(columns=['dealer_city', 'dealer_state'], inplace=True)

        df["mileage"] = pd.to_numeric(df["mileage"], errors="coerce").fillna(0).astype(int)
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
        df["make"] = df["make"].str[:100]
        df["model"] = df["model"].str[:100]

        return df
    except (pd.errors.ParserError, KeyError, ValueError) as e:
        print(f"Error while processing CSV file: {e}")
        return None

def setup_database():
    """Ensures table creation and data ingestion."""
    try:
        create_table()

        with get_db_connection() as conn, conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"Database already has {count} records. Skipping import.")
                return  

        df = load_data("NEWTEST-inventory-listing-2022-08-17.txt")
        if df is not None:
            insert_data(df)

    except Exception as e:
        print(f"Unexpected error in database setup: {e}")


