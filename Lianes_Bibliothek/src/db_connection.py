import getpass
from sqlalchemy import create_engine

# Verbindungsdaten zur Datenbank
schema = "lianes_library"
host = "127.0.0.1"
user = "root"
password = getpass.getpass("MySQL-Passwort für 'root': ")
port = 3306
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
engine = create_engine(connection_string)
