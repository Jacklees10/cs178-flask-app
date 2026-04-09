# dbCode.py
# Author: Ben Jackels
# Helper functions for database connection and queries

import pymysql
import creds
import boto3

# Create and return a connection to the MySQL RDS database
def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    try:
        conn = pymysql.connect(
            host=creds.host,
            user=creds.user,
            password=creds.password,
            db=creds.db,
        )
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Execute a SELECT query and return results as a list of dictionaries
def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    try:
        # Use DictCursor so results come back as key-value pairs
        cur = get_conn().cursor(pymysql.cursors.DictCursor)
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return rows
    except pymysql.Error as e:
        print(f"Error executing query: {e}")
        return []

# Execute INSERT, UPDATE, or DELETE queries on MySQL
def execute_update(query, args=()):
    """Executes INSERT, UPDATE, or DELETE queries."""
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Run query and commit changes
        cur.execute(query, args)
        conn.commit()

        cur.close()
        conn.close()
    except pymysql.Error as e:
        print(f"Error executing update: {e}")

# Connect to AWS DynamoDB and return the Favorites table
def get_dynamodb():
    try:
        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-1'
        )
        return dynamodb.Table('Favorites')
    except Exception as e:
        print(f"Error connecting to DynamoDB: {e}")
        return None

# Add a new favorite country to DynamoDB
def add_favorite(country_name, population, language):
    try:
        table = get_dynamodb()

        # Store item with multiple attributes
        table.put_item(
            Item={
                'CountryName': country_name,  # Primary key
                'Population': int(population),
                'Language': language
            }
        )
    except Exception as e:
        print(f"Error adding favorite: {e}")

# Retrieve all favorite countries from DynamoDB
def get_favorites():
    try:
        table = get_dynamodb()

        # Scan returns all items in the table
        response = table.scan()
        return response['Items']
    except Exception as e:
        print(f"Error getting favorites: {e}")
        return []

# Delete a favorite country using its primary key
def delete_favorite(country_name):
    try:
        table = get_dynamodb()

        # Delete item based on CountryName (primary key)
        table.delete_item(Key={'CountryName': country_name})
    except Exception as e:
        print(f"Error deleting favorite: {e}")