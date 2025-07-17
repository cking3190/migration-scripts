


# SQL Server to MongoDB ETL Script

This Python script performs efficient, batch-based ETL from a SQL Server table or query into a MongoDB collection. It is designed for Proof of Concept data migrations.

## 🚀 Features

- Streamed batch loading to avoid memory pressure
- Converts SQL Server rows to MongoDB documents using `pandas`
- Command-line configuration with validation
- Connection testing for SQL Server and MongoDB
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
pyodbc==5.1.0
pandas==2.2.2
pymongo==4.7.2
```

## 📥 Usage

Run the script with:

```bash
python migratesqlMongo.py \
  --srcSqlConnString "DRIVER={ODBC Driver 18 for SQL Server};SERVER=host;DATABASE=db;UID=user;PWD=pass;Encrypt=yes;TrustServerCertificate=yes" \
  --tgtMongoConnString "mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority" \
  --sqlQuery "SELECT * FROM your_table" \
  --tgtDb your_mongo_db \
  --tgtColl your_collection \
  --batchSize 1000
```

### Parameters

| Argument               | Description                                      |
|------------------------|--------------------------------------------------|
| `--srcSqlConnString`   | SQL Server ODBC connection string                |
| `--tgtMongoConnString` | MongoDB URI (Atlas or local)                     |
| `--sqlQuery`           | SQL query to extract data                        |
| `--tgtDb`              | MongoDB database name                            |
| `--tgtColl`            | MongoDB collection name                          |
| `--batchSize`          | Rows to process per batch (default: 500)         |

## ⚠️ Notes

- Only `SELECT` queries are supported.
- Ensure the ODBC Driver is installed and available on your system.
- Many-to-many relationships are not embedded — post-process with helper scripts as needed.

## ✅ Example

```bash
python migratesqlMongo.py \
  --srcSqlConnString "DRIVER={ODBC Driver 18 for SQL Server};SERVER=sqlserver.example.com;DATABASE=database;UID=user;PWD=password;Encrypt=yes;TrustServerCertificate=yes" \
  --tgtMongoConnString "mongodb+srv://USER:PASSWORD@SERVER.mongodb.net/?retryWrites=true&w=majority" \
  --sqlQuery "SELECT * FROM orders" \
  --tgtDb test \
  --tgtColl orders \
  --batchSize 500
```

## 📂 File Structure

```
migration-scripts/
└── src/
    └── sqlserver/
        ├── migratesqlMongo.py
        └── requirements.txt
```

## 🧪 Connection Testing

The script validates SQL Server and MongoDB connections at startup and exits if invalid.

## 🛣️ Roadmap Ideas

- Add automatic embedding for 1:many or many:many relations
- Retry logic for failed batches
- Partitioned loads by date or key ranges
- Optional schema mapping and data transformation layer

## 📝 License

MIT License
