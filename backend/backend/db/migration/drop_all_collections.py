from mongoengine import connect, get_connection, get_db

from backend.conf import initialise_app

initialise_app()
db = get_db()

# Loop through all collections and drop them
for collection_name in db.list_collection_names():
    # Drop the collection
    db.drop_collection(collection_name)
    print(f"Dropped collection: {collection_name}")

print("All collections have been dropped.")
