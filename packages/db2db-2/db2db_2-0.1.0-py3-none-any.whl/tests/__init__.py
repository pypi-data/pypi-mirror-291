from db2db import transfer_data



source_db_config = {
    'db_type': 'postgresql',
    'host': 'localhost',
    'database': 'source_db',
    'user': 'user',
    'password': 'password'
}

target_db_config = {
    'db_type': 'mysql',
    'host': 'localhost',
    'database': 'target_db',
    'user': 'user',
    'password': 'password'
}

source_table = 'your_source_table'
target_table = 'your_target_table'

try:
    transfer_data(source_db_config, target_db_config, source_table, target_table)
except Exception as e:
    print(f"An error occurred: {e}")
