# migration-scripts

## Overview

This project provides tools to migrate the results of SQL queries into MongoDB for proof-of-concept (PoC) purposes. The scripts support batch processing of large datasets and include utilities to transform and embed related documents.

## Components

### SQL to Mongo Migration

Scripts are available to extract data from:
- PostgreSQL
- SQL Server

These tools:
- Connect to the source database
- Execute a query or cursor-based batch pull
- Convert results to MongoDB documents
- Write to a specified MongoDB collection

### Embedding Utilities (`mongoutils`)

Once your SQL data is in MongoDB, use these tools to normalize and embed related collections:

- `embed-array.py` — Performs a `$lookup` and embeds an array of matching documents into a source collection (for one-to-many relationships).
- `embed-docs.py` — Performs a `$lookup` and `$unwind` to embed a single related document (for one-to-one relationships).

## Use Case

These tools are ideal for quickly creating embedded MongoDB data models for demonstration or PoC purposes based on normalized SQL schemas.