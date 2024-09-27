# data_handlar.py

#!/home/astrid/dev/.conda/bin/python3

''' A script that contains functions for importing data to SQLite and reading data from SQLite. '''


import pandas as pd
import sqlite3
import logging

logger = logging.getLogger(__name__)


def import_to_database(df, database, table_name) -> bool:
    '''A function that imports data to SQLite.'''
    try:
        conn = sqlite3.connect(database)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
        logger.info('Data from Dataframe imported successfully into %s and %s', database, table_name)
        return True
    except Exception as e:
        logger.error('Error importing data to %s table: %s, exception %s', database, table_name, type(e).__name__)
        return False


def read_from_sqlite(database, table_name):
    '''A function that reads data from a SQLite database and returns a DataFrame.'''
    try:
        conn = sqlite3.connect(database)
        df = pd.read_sql(f'SELECT * FROM {table_name}', conn)
        conn.close()
        logger.info('Data read from database %s and table %s', database, table_name)
        return df
    except Exception as e:
        logger.error('Error reading data to %s table: %s, exception %s', database, table_name, type(e).__name__)
        return None


if __name__ == "__main__":
    
    # testing the functions
    database = 'test_database.db'
    table_name = 'test_statistics'
    df = [{'workid': 'hcaeventyr0', 'title': 'The Little Mermaid'},]
    
    import_to_database(df, database, table_name)
    df = read_from_sqlite(database, table_name)

    print('The data_handlar script has been run.')
