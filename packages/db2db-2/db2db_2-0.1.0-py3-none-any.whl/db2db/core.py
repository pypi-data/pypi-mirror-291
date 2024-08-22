# db2db/core.py

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging

class DatabaseTransfer:
    def __init__(self, source_connection_string, target_connection_string):
        try:
            self.source_engine = create_engine(source_connection_string)
            self.target_engine = create_engine(target_connection_string)
        except SQLAlchemyError as e:
            logging.error(f"Error creating engines: {e}")
            raise
        except Exception as e:
            logging.error(f"error occurred while creating engines: {e}")
            raise

    def transfer(self, source_table, target_table):
        """Transfer data from source to target using pandas."""
        try:
            # Extract data
            df = pd.read_sql_table(source_table, self.source_engine)
            logging.info(f"Data extracted from {source_table}.")
        except SQLAlchemyError as e:
            logging.error(f"Error extracting data from {source_table}: {e}")
            raise
        except ValueError as e:
            logging.error(f"Invalid source table {source_table}: {e}")
            raise
        except Exception as e:
            logging.error(f"error occurred during data extraction: {e}")
            raise

        try:
            # Load data
            df.to_sql(target_table, self.target_engine, if_exists='replace', index=False)
            logging.info(f"Data loaded into {target_table}.")
        except SQLAlchemyError as e:
            logging.error(f"Error loading data into {target_table}: {e}")
            raise
        except ValueError as e:
            logging.error(f"Invalid target table {target_table}: {e}")
            raise
        except Exception as e:
            logging.error(f"error occurred during data loading: {e}")
            raise
