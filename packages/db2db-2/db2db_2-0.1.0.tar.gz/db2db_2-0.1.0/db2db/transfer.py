# db2db/transfer.py

from .core import DatabaseTransfer
from .utils import create_connection_string
import logging

def transfer_data(source_db_config, target_db_config, source_table, target_table):
    """Orchestrate the data transfer process."""
    try:
        # Create connection strings
        source_conn_str = create_connection_string(**source_db_config)
        target_conn_str = create_connection_string(**target_db_config)
        logging.info("Connection strings created successfully.")
        
        # Initialize DatabaseTransfer class
        transfer = DatabaseTransfer(source_conn_str, target_conn_str)
        
        # Transfer data
        transfer.transfer(source_table, target_table)
        logging.info("Data transfer completed successfully.")
    except Exception as e:
        logging.error(f"error occurred during the data transfer process: {e}")
        raise
