# main.py

#!/home/astrid/dev/.conda/bin/python3

''' 
The main script where input parameters are instantiated. 
Text files are loaded via a shell script.
The texts are processed and a DataFrame with text statistics are created.
The DataFrame is saved in an SQlite database. 
At last the DataFrame is retrieved from the database and information are printed to the terminal.
'''


import logging
import pandas as pd

from load_from_repo import FileProcessor
from text_processor import TextStatistics
from data_handlar import import_to_database, read_from_sqlite


# configuring the logging module
logging.basicConfig(
    filename = '/home/astrid/dev/log_file.log',
    format = '[%(asctime)s][%(levelname)s][%(message)s][%(name)s][%(filename)s][%(lineno)d]',
    level = logging.DEBUG,
    datefmt = '%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


# input parameters
source_dir = '/home/astrid/dev/'
dest_dir = '/home/astrid/dev/hca_directory/'
prefix = 'hcaeventyr0'
database = 'hca_database.db'
table_name = 'hca_text_statistics'


# loading and processing texts
processor = FileProcessor(source_dir, dest_dir)
processor.process(prefix)

stats = TextStatistics(dest_dir)
df = stats.process_texts()

# saving the returned DataFrame into a database
import_to_database(df, database, table_name)

# load dataframe and view the dataframe
df = read_from_sqlite(database, table_name)

print(df.head(5))
print(df.info())  
print(df.describe()) 

if __name__ == "__main__":
    
    print('The main module has been run.')
    



 
