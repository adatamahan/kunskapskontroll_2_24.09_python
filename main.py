# main.py

#!/home/astrid/dev/.conda/bin/python3

''' The main script that imports text files from a repository, processes the text files and saves the returned DataFrame in SQlite,'''



import logging
import pandas as pd

from load_from_repo import FileProcessor
from data_cleaner_class import TextStatistics
from data_handlar import import_to_database, read_from_sqlite


# configuring the logging module
logging.basicConfig(
    filename = '/home/astrid/dev/log_file.log',
    format = '[%(asctime)s][%(levelname)s][%(message)s][%(name)s][%(filename)s][%(lineno)d]',
    level = logging.DEBUG,
    datefmt = '%Y-%m-%d %H:%M')

logger = logging.getLogger(__name__)


# import text H. C. Andernsen text files from repo and save them in a directory -> text_directory
processor = FileProcessor(
        bash_script ='/home/astrid/dev/extract_stuff_prefix.sh',
        source_dir ='/home/astrid/dev/',
        dest_dir ='/home/astrid/dev/hca_directory/'
    )
processor.process('hcaeventyr0')


# loop thorugh the files in the directory and process them with the script -> dataframe
directory = '/home/astrid/dev/hca_directory/'
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
    



 
