import argparse
import sys
import psycopg2
import pandas as pd
from pymongo import MongoClient
from datetime import datetime


# === Parse command-line arguments ===
parser = argparse.ArgumentParser(description="ETL from PostgreSQL to MongoDB")
parser.add_argument("--srcSqlConnString", required=True, help="PostgreSQL connection string")
parser.add_argument("--tgtMongoConnString", required=True, help="MongoDB connection URI")
parser.add_argument("--sqlQuery", required=True, help="SQL query to execute")
parser.add_argument("--tgtDb", required=True, help="Target MongoDB database name")
parser.add_argument("--tgtColl", required=True, help="Target MongoDB collection name")
parser.add_argument("--batchSize", type=int, default=500, help="Number of rows to process per batch")

args = parser.parse_args()

# Validate connection strings and query
if "dbname=" not in args.srcSqlConnString:
    sys.exit("Error: srcSqlConnString must contain 'dbname='")

if "mongodb" not in args.tgtMongoConnString.lower():
    sys.exit("Error: tgtMongoConnString must be a valid MongoDB URI")

if "select" not in args.sqlQuery.lower():
    sys.exit("Error: sqlQuery must be a SELECT statement")

# Test PostgreSQL connection
try:
    test_sql_conn = psycopg2.connect(args.srcSqlConnString)
    test_sql_conn.close()
except Exception as e:
    sys.exit(f"Error: Unable to connect to PostgreSQL: {e}")

# Test MongoDB connection
try:
    test_mongo_client = MongoClient(args.tgtMongoConnString, serverSelectionTimeoutMS=5000)
    test_mongo_client.server_info()  # Forces connection check
    test_mongo_client.close()
except Exception as e:
    sys.exit(f"Error: Unable to connect to MongoDB: {e}")

sql_server_conn_str = args.srcSqlConnString
TABLE_QUERY = args.sqlQuery
BATCH_SIZE = args.batchSize
MONGO_URI = args.tgtMongoConnString
MONGO_DB = args.tgtDb
MONGO_COLLECTION = args.tgtColl

# === Connect to PostgreSQL ===
sql_conn = psycopg2.connect(sql_server_conn_str)
cursor = sql_conn.cursor()
cursor.execute(TABLE_QUERY)

# Get column names
cursor_scroll = sql_conn.cursor()
cursor_scroll.execute(TABLE_QUERY + " WHERE 1=0" if "where" not in TABLE_QUERY.lower() else TABLE_QUERY + " AND 1=0")
columns = [desc[0] for desc in cursor_scroll.description]
cursor_scroll.close()

# === Connect to MongoDB ===
mongo_client = MongoClient(MONGO_URI)
mongo_collection = mongo_client[MONGO_DB][MONGO_COLLECTION]

total_inserted = 0

while True:
    batch = cursor.fetchmany(BATCH_SIZE)
    if not batch:
        break

    # Convert batch to DataFrame
    df = pd.DataFrame(batch, columns=columns)
    
    # Drop duplicate columns by name, keeping the first occurrence
    df = df.loc[:, ~df.columns.duplicated()]


    # Safer serialization of date and NaT values using JSON round-trip
    json_str = df.to_json(orient="records", date_format="iso")
    docs = pd.read_json(json_str).to_dict(orient="records")

    if docs:
        mongo_collection.insert_many(docs)
        total_inserted += len(docs)
        print(f"Inserted {len(docs)} documents (Total: {total_inserted})")

# === Cleanup ===
cursor.close()
sql_conn.close()
mongo_client.close()

print(f"Done. Total documents inserted: {total_inserted}")