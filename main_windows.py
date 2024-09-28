# main.py

#!/home/astrid/dev/.conda/bin/python3

''' The main script that imports text files from a repository, processes the text files and saves the returned DataFrame in SQlite,'''


import logging
import pandas as pd

from load_from_repo import FileProcessor
from text_processor import TextStatistics
from data_handlar import import_to_database, read_from_sqlite


# configuring the logging module
logging.basicConfig(
    filename = 'C:/Users/Bruger/OneDrive/Skrivebord/data_science/8_pythonprogrammering/kunskapskontroll_2/dev/log_file.log',
    format = '[%(asctime)s][%(levelname)s][%(message)s][%(name)s][%(filename)s][%(lineno)d]',
    level = logging.DEBUG,
    datefmt = '%Y-%m-%d %H:%M')
 
logger = logging.getLogger(__name__)


# loop thorugh the files in the directory and process them with the script -> dataframe
directory = 'C:/Users/Bruger/OneDrive/Skrivebord/data_science/8_pythonprogrammering/kunskapskontroll_2/dev/hca_directory/'
hca_directory = TextStatistics(directory)
hca_df = hca_directory.process_texts()


# save the returned dataframe
database = 'hca_database.db'
table_name = 'hca_text_statistics'
import_to_database(hca_df, database, table_name)


# load dataframe and view the dataframe
df = read_from_sqlite(database, table_name)

print(df.tail(10))
print(df.info())  
print(df.describe()) 

if __name__ == "__main__":
    
    print('The main module has been run.')
    



 
