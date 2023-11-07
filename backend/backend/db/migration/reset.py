from backend.db.migration.initialise_db import initialise_db
from backend.db.migration.drop_all_collections import drop_all_collections

if __name__ == "__main__":
    drop_all_collections()
    initialise_db()