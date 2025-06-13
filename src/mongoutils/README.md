


# Mongo Utilities

This directory contains utility scripts for embedding documents into MongoDB collections.



## `embed-array.py`

Performs a `$lookup` to embed an **array of related documents** from a secondary collection into a source collection using a one-to-many relationship.  This checks and creates indexes in the collections output is written to the source collection.

### Usage

```bash
python embed-array.py \
  --mongoUri "<your MongoDB URI>" \
  --db "yourDatabase" \
  --sourceColl "sourceCollection" \
  --targetColl "targetCollection" \
  --localField "fieldInSource" \
  --foreignField "fieldInTarget" \
  --embedField "arrayFieldName"
```

### Example

```bash
python embed-array.py \
  --mongoUri "mongodb+srv://user:pass@cluster.mongodb.net" \
  --db "northwind" \
  --sourceColl "orders" \
  --targetColl "order_details" \
  --localField "order_id" \
  --foreignField "order_id" \
  --embedField "orderDetails"
```

This will embed all matching `order_details` into each document in `orders` under the `orderDetails` array field.

---

## `embed-docs.py`

Performs a `$lookup` followed by `$unwind` to embed a **single document** from a target collection into a field on the source collection, for one-to-one relationships.  This checks and creates indexes in the collections output is written to the source collection.

### Usage

```bash
python embed-docs.py \
  --mongoUri "<your MongoDB URI>" \
  --db "yourDatabase" \
  --sourceColl "sourceCollection" \
  --targetColl "targetCollection" \
  --localField "fieldInSource" \
  --foreignField "fieldInTarget" \
  --embedField "embeddedFieldName"
```

### Example

```bash
python embed-docs.py \
  --mongoUri "mongodb+srv://user:pass@cluster.mongodb.net" \
  --db "northwind" \
  --sourceColl "products" \
  --targetColl "product_details" \
  --localField "product_id" \
  --foreignField "product_id" \
  --embedField "product_detail"
```

This will embed a single matching `product_details` document into each `products` document under the `product_detail` field.