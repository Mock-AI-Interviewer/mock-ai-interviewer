from backend.db.migration.initialise_db import initialise_db
from backend.db.migration.drop_all_collections import drop_all_collections

def reset_db():
    drop_all_collections()
    initialise_db()

if __name__ == "__main__":
    reset_db()