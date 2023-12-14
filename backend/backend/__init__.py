from backend.conf import initialise_app
from backend.db.migration.reset import reset_db

initialise_app()
reset_db()