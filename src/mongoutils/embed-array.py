import argparse
from pymongo import MongoClient

def embed_documents(mongo_uri, db_name, source_coll, target_coll, local_field, foreign_field, embed_field):
    client = MongoClient(mongo_uri)
    db = client[db_name]

    source_index_fields = {list(index["key"].keys())[0] for index in db[source_coll].list_indexes()}
    target_index_fields = {list(index["key"].keys())[0] for index in db[target_coll].list_indexes()}

    # Ensure indexes exist on local and foreign fields
    if local_field not in source_index_fields:
        db[source_coll].create_index(local_field)

    if foreign_field not in target_index_fields:
        db[target_coll].create_index(foreign_field)

    # Use aggregation with $lookup and $merge for scalable performance
    pipeline = [
        {
            "$lookup": {
                "from": target_coll,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": embed_field
            }
        },
        {
            "$merge": {
                "into": source_coll,
                "whenMatched": "merge",
                "whenNotMatched": "discard"
            }
        }
    ]

    db[source_coll].aggregate(pipeline, allowDiskUse=True)
    print(f"Embedding complete from {target_coll} into {source_coll} as field '{embed_field}' using aggregation.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed a single matching doc from one collection into another.")
    parser.add_argument("--mongoUri", required=True, help="MongoDB connection string")
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--sourceColl", required=True, help="Source collection name")
    parser.add_argument("--targetColl", required=True, help="Target collection name to find documents from")
    parser.add_argument("--localField", required=True, help="Field in source collection to match on")
    parser.add_argument("--foreignField", required=True, help="Field in target collection to match against")
    parser.add_argument("--embedField", required=True, help="Field name to embed the document into")

    args = parser.parse_args()
    embed_documents(
        mongo_uri=args.mongoUri,
        db_name=args.db,
        source_coll=args.sourceColl,
        target_coll=args.targetColl,
        local_field=args.localField,
        foreign_field=args.foreignField,
        embed_field=args.embedField
    )
