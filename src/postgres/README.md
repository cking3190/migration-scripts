# PostgreSQL to MongoDB ETL Script

This Python script performs efficient, batch-based ETL from a PostgreSQL table or query into a MongoDB collection. It is designed for Proof of Concept data migrations.

## 🚀 Features

- Streamed batch loading to avoid memory pressure
- Automatic removal of duplicate columns caused by joins
- Converts PostgreSQL rows to MongoDB documents using `pandas`
- Command-line configuration with validation
- Connection testing for both PostgreSQL and MongoDB
- Logs batch progress and total documents inserted

## 🛠️ Requirements

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Example `requirements.txt`:
```text
psycopg2==2.9.9
pymongo==4.7.2
pandas==2.2.2
```

## 📥 Usage

Run the script with:

```bash
python migratepsqlMongo.py \
  --srcSqlConnString "host=HOSTNAME dbname=DBNAME user=USER password=PASS" \
  --tgtMongoConnString "mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority" \
  --sqlQuery "SELECT * FROM your_table" \
  --tgtDb your_mongo_db \
  --tgtColl your_collection \
  --batchSize 1000
```

### Parameters

| Argument               | Description                                      |
|------------------------|--------------------------------------------------|
| `--srcSqlConnString`   | PostgreSQL connection string                     |
| `--tgtMongoConnString` | MongoDB URI (Atlas or local)                     |
| `--sqlQuery`           | SQL query to extract data                        |
| `--tgtDb`              | MongoDB database name                            |
| `--tgtColl`            | MongoDB collection name                          |
| `--batchSize`          | Rows to process per batch (default: 500)         |

## ⚠️ Notes

- Only `SELECT` queries are supported.
- If duplicate column names occur from joins, only the first instance is retained.
- Many-to-many relationships are not flattened — embed manually if needed post-load.

## ✅ Example

```bash
python migratepsqlMongo.py \
  --srcSqlConnString "DRIVER={ODBC Driver 18 for SQL Server};SERVER=sqlserver.example.com,1433;DATABASE=sampledb;UID=dbuser;PWD=securePass123!;Encrypt=yes;TrustServerCertificate=yes" \
  --tgtMongoConnString "mongodb+srv://USER:PASS@SERVER.mongodb.net/?retryWrites=true&w=majority" \
  --sqlQuery "SELECT * FROM orders" \
  --tgtDb test \
  --tgtColl orders \
  --batchSize 500
```

## 📂 File Structure

```
migration-scripts/
└── src/
    └── postgres/
        ├── migratepsqlMongo.py
        └── requirements.txt
```

## 🧪 Connection Testing

The script validates both source and target connections at startup. If a connection fails, it exits with a clear error.

