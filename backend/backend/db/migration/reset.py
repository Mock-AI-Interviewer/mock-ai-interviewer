from backend.db.migration.drop_all_collections import drop_all_collections
from backend.db.migration.initialise_db import insert_example_data


def reset_db():
    drop_all_collections()
    insert_example_data()


if __name__ == "__main__":
    reset_db()
