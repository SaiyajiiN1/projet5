from mysql.connector import MySQLConnection

import settings

db = MySQLConnection(
    user=settings.DB_NAME,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    charset=settings.DB_CHARSET,
    collation=settings.DB_COLLATION,
)
