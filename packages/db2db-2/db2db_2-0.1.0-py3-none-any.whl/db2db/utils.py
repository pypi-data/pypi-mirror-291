# db2db/utils.py

from sqlalchemy.engine.url import URL
import logging

def create_connection_string(db_type, **kwargs):
    """Create a SQLAlchemy connection string."""
    try:
        if db_type == 'postgresql':
            return URL(
                drivername='postgresql+psycopg2',
                username=kwargs.get('user'),
                password=kwargs.get('password'),
                host=kwargs.get('host'),
                database=kwargs.get('database')
            )
        elif db_type == 'mysql':
            return URL(
                drivername='mysql+mysqlconnector',
                username=kwargs.get('user'),
                password=kwargs.get('password'),
                host=kwargs.get('host'),
                database=kwargs.get('database')
            )
        elif db_type == 'mssql':
            return URL(
                drivername='mssql+pyodbc',
                username=kwargs.get('user'),
                password=kwargs.get('password'),
                host=kwargs.get('host'),
                database=kwargs.get('database'),
                query={'driver': 'ODBC Driver 17 for SQL Server'}
            )
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    except KeyError as e:
        logging.error(f"Missing required database configuration: {e}")
        raise
    except ValueError as e:
        logging.error(f"Error creating connection string: {e}")
        raise
    except Exception as e:
        logging.error(f"error occurred while creating the connection string: {e}")
        raise
