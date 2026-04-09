# dbCode.py
# Author: Ben Jackels
# Helper functions for database connection and queries

import pymysql
import creds
import boto3

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def execute_update(query, args=()):
    """Executes INSERT, UPDATE, or DELETE queries."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

def get_dynamodb():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='us-east-1'
    )
    return dynamodb.Table('Favorites')

def add_favorite(country_name):
    table = get_dynamodb()
    table.put_item(Item={'CountryName': country_name})

def get_favorites():
    table = get_dynamodb()
    response = table.scan()
    return response['Items']

def delete_favorite(country_name):
    table = get_dynamodb()
    table.delete_item(Key={'CountryName': country_name})