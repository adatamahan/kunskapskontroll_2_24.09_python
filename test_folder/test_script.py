# test_script.py

'''
A script that performs pytests on the scripts below
- load_from_repo.py
- data_cleaner_class.py
- data_handlar.py
'''


import pytest
import pandas as pd
import sqlite3
import os
import re

from load_from_repo import FileProcessor
from data_handlar import import_to_database, read_from_sqlite
from data_cleaner_class import TextStatistics


# testing the load_from_repo.py script

processor = FileProcessor(
        bash_script ='extract_stuff_prefix.sh',
        source_dir ='/home/astrid/dev/',
        dest_dir ='/home/astrid/dev/test_text_directory/'
    )
processor.process('hcaeventyr0')


def test_load_from_repo():
    '''     
    A function that performs tests on the the load_from_repo script
    The following is tested:
    - if there are files saved in the destination directory
    - if the files are text files
    '''
    
    assert len(os.listdir('/home/astrid/dev/test_text_directory')) > 0
    'No files saved in the destination directory'
    
    assert all([file.endswith('.text') for file in os.listdir('/home/astrid/dev/test_text_directory')])
    'Not all files are text files'
     


# testing the data_cleaner_class.py script

directory = '/home/astrid/dev/test_texts/'
test_stats = TextStatistics(directory)
df_test = test_stats.process_texts()
print(df_test)


def test_data_cleaner_class():
    '''
    A function that tests the data_cleaner_class.py script.  
    The following is tested:
    - that a DataFrame is returned
    - that the DataFrame has as many rows as there are '-workid'-files in the directory
    - that the DataFrame has 11 columns
    - checks that the workids in the files match the workids in the DataFrame column
    - that the numeric columns holds numeric values
    - that the object columns holds string values
    '''
    
    assert isinstance(df_test, pd.DataFrame)
    "The function does not return a DataFrame"
    
    assert df_test.shape[0] == len([file for file in os.listdir(directory) if '-workid' in file])
    'No. of columns != no. "-workid" files in directory'
    
    assert df_test.shape[1] == 11
    'No. of columns != 11'
    
    file_workids = set('workid' + re.search(r'-workid(\d+)', file).group(1)
                   for file in os.listdir(directory) 
                   if re.search(r'-workid\d+', file))
    df_workids = set(df_test['workid']) #.astype(str))  
    assert file_workids == df_workids
    'Mismatch between file workids and DataFrame workids'
    
    numeric_columns = ['character_count', 'token_count', 'word_count', 'vocabulary_count', 'sentence_count',
                       'avg_words_in_sentence', 'mean_word_length', 'lexical_diversity']
    for col in numeric_columns:
        assert df_test[col].dtype in ['int64', 'float64']
        f'Column {col} is not of type int64 or float64'
        
    object_columns = ['prefix', 'workid', 'title']
    for col in object_columns:
        assert df_test[col].dtype == 'object'
        f'Column {col} is not of object dtype'
    


# testing the data_handlar.py script

folder_path = '/home/astrid/dev/'
database = os.path.join(folder_path, 'test_text_database.db')
table_name = 'test_text_statistics'
test_df = pd.DataFrame({'workdid': ['workid00001', 'workid00002'], 'word_count': [4, 4], 'char_count': [18, 24], 'word_density': [4.5, 5.5]})

import_to_database(test_df, database, table_name)
df = read_from_sqlite(database, table_name)


def test_data_handlar():
    ''' 
    A function that tests the data_handlar script
    The following is tested:
    - if the database file path exists after import
    - if the DataFrame contains values
    - if the table name in the database are correct 
    - if the database folder are correct
    '''
    assert os.path.exists('/home/astrid/dev/test_text_database.db')
    'The database file does not exist'
    
    assert len(df) > 0
    'The DataFrame is empty'
    
    assert table_name == 'test_text_statistics'
    'The table name is incorrect or does not exist'
    
    assert database == '/home/astrid/dev/test_text_database.db'
    'The database folder is incorrect'
    

if __name__ == "__main__":
    
    pytest.main(['-v', 'test_script.py'])
    
    print('The test script has been run')
