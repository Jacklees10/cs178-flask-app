# dbCode.py
# Author: Ben Jackels
# Helper functions for database connection and queries

import pymysql
import creds
import boto3

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

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    try:
        cur = get_conn().cursor(pymysql.cursors.DictCursor)
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return rows
    except pymysql.Error as e:
        print(f"Error executing query: {e}")
        return []

def execute_update(query, args=()):
    """Executes INSERT, UPDATE, or DELETE queries."""
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(query, args)
        conn.commit()
        cur.close()
        conn.close()
    except pymysql.Error as e:
        print(f"Error executing update: {e}")

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

def add_favorite(country_name, population, language):
    try:
        table = get_dynamodb()
        table.put_item(
            Item={
                'CountryName': country_name,
                'Population': int(population),
                'Language': language
            }
        )
    except Exception as e:
        print(f"Error adding favorite: {e}")

def get_favorites():
    try:
        table = get_dynamodb()
        response = table.scan()
        return response['Items']
    except Exception as e:
        print(f"Error getting favorites: {e}")
        return []

def delete_favorite(country_name):
    try:
        table = get_dynamodb()
        table.delete_item(Key={'CountryName': country_name})
    except Exception as e:
        print(f"Error deleting favorite: {e}")