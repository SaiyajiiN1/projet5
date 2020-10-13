from mysql.connector import MySQLConnection

import settings

db = MySQLConnection(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    charset=settings.DB_CHARSET,
    collation=settings.DB_COLLATION,
)

_managers = []


def register_manager(manager):
    """Register a manager."""
    _managers.append(manager)


def create_tables():
    """Create the database tables if necessary."""
    import purbeurre.models

    for manager in _managers:
        print(f"Creating table {manager.table}")
        manager.create_table()


def drop_tables():
    """Removes tables from the database if they are present."""
    import purbeurre.models

    for manager in reversed(_managers):
        print(f"Dropping table {manager.table}")
        manager.drop_table()
