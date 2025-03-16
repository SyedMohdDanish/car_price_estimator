# database/setup_db.py

import os
import pandas as pd
import psycopg2
import time
from database.db import Database

class SetupDatabase:
    TABLE_NAME = "car_listings"

    def __init__(self, db: Database):
        self.db = db

    def create_table(self, conn):
        """Creates the car_listings table if it does not exist."""
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
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
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
                print(f"Table '{self.TABLE_NAME}' ensured.")
        except psycopg2.Error as e:
            print(f"Database error while creating table: {e}")

    def load_data(self, file_path):
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

    def insert_data(self, conn, df):
        """Inserts data from a DataFrame into the PostgreSQL table."""
        if df.empty:
            print("No data to insert.")
            return

        records = df.to_records(index=False).tolist()
        query = f"""
            INSERT INTO {self.TABLE_NAME} (year, make, model, mileage, price, location)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        try:
            with conn.cursor() as cursor:
                start_time = time.time()
                cursor.executemany(query, records)
                conn.commit()
                elapsed_time = time.time() - start_time
                print(f"{len(records)} records inserted successfully in {elapsed_time:.4f} seconds.")
        except psycopg2.Error as e:
            print(f"Database error while inserting data: {e}")

    def setup_database(self, file_path):
        """Ensures table creation and data ingestion."""
        conn = self.db.connect()  # Open connection once
        try:
            self.create_table(conn)
            
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME};")
                count = cursor.fetchone()[0]
                
                if count > 0:
                    print(f"Database already has {count} records. Skipping import.")
                    return  

            df = self.load_data(file_path)
            if df is not None:
                self.insert_data(conn, df)

        except Exception as e:
            print(f"Unexpected error in database setup: {e}")
        finally:
            self.db.close()

