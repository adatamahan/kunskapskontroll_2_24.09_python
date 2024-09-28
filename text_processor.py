# text_processor.py

#!/home/astrid/dev/.conda/bin/python3

''' A script loads texts files,  calculates statistics from the texts and returns a dataframe with statistics.'''

import os
import re
import nltk
import logging
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)



class TextStatistics:
    '''A class that calculates various statistics from texts in a directory and returns a dataframe.'''
    
    def __init__(self, directory: str) -> None:
        self.directory = directory
        self.text = ""
        self.logger = logging.getLogger(__name__)
        self.logger.info('TextStatistics initialized with directory: %s', directory)
        
        # Log the count of files in the directory if it exists
        try:
            file_count_workid = len([f for f in os.listdir(self.directory) if '-workid' in f])
            file_count_titles = len([f for f in os.listdir(self.directory) if '_titles' in f])
            self.logger.info('Count of files that contains "-workdid" in the filename: %s', file_count_workid)
            self.logger.info('Count of files contains "-titles" in the filename: %s', file_count_titles)
        except FileNotFoundError:
            self.logger.error('Directory %s not found', self.directory)
        except Exception as e:
            self.logger.error('Error accessing directory:', type(e).__name__)


    def get_titles(self) -> pd.DataFrame:
        '''A function that creates a dataframe from the text files with prefix, title, workid information'''
        data = []
        for filename in os.listdir(self.directory):
          if '_titles' in filename and filename.endswith('.text'):  
                prefix = filename.split('0', 1)[0]  # Splits at the first occurrence of '0'
                file_path = os.path.join(self.directory, filename)  
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        parts = line.strip().split(';', 1)  # strip removes whitepaces. splits on the 1st ;
                        if len(parts) == 2: 
                            workid, title = parts
                            data.append((prefix, workid, title))
        
        df1 = pd.DataFrame(data, columns=['prefix', 'workid', 'title'])
        self.logger.info('Dataframe with prefix, workid and titles are created with %s rows', len(df1))
        return df1

   
    def add_file(self, file_path: str) -> bool:
        '''A function that reads a text file and outputs exceptions if an error occurs.'''
        try:
            for filename in os.listdir(self.directory):
                if filename.endswith('.text'):  
                    with open(file_path, 'r', encoding='utf-8') as file:
                        self.text = file.read()
            return True
        except FileNotFoundError:
            self.logger.error('File %s not found', file_path)
            return False
        except IOError as e:
            self.logger.error('An error occurred while reading the file: %s', type(e).__name__)
            return False
        except Exception as e:
            self.logger.error('An unexpected error occurred:', type(e).__name__)
            return False
   
   
    def extract_workid(self, file_path: str) -> str:
        '''A function that extracts workids from a file path.'''
        pattern = re.compile(r'(workid\d+)')
        match = pattern.search(file_path)
        if match:
            return match.group(1)
        else:
            return None
    
    
    def character_count(self) -> int:
        '''Counts the number of characters including whitespaces in the text.'''
        return len(self.text)
    
    
    def token_count(self) -> int:
        '''Counts the number of tokens in the text, all signs included.'''
        return len(word_tokenize(self.text, language='danish'))
    
    
    def word_count(self) -> int:
        '''counts the number of proper danish words in the text.'''
        words = [w for w in word_tokenize(self.text.lower(), language='danish') 
                if w.isalpha() and (len(w) > 1 or w in ['i', 'o', 'å', 'ø', 'a', 'ø'])]
        return len(words)
    
    
    def count_vocabulary(self) -> int:
        '''Counts the vocabulary of the text. Note! No lemmatizer or stemming is used.'''
        vocab = set(w.lower() for w in word_tokenize(self.text, language='danish') 
                    if w.isalpha() and (len(w) > 1 or w in ['i', 'o', 'å', 'ø', 'a']))
        return len(vocab)
        
        
    def mean_word_length(self) -> float:
        '''Calculates the average length of words in the text.'''
        words = [w for w in word_tokenize(self.text.lower(), language='danish') 
                 if w.isalpha() and (len(w) > 1 or w in ['i', 'o', 'å', 'ø', 'a'])]
        if len(words) == 0: 
            return 0.00
        else:
            mean_length = sum(len(w) for w in words) / len(words)
            return round(mean_length, 2)
    
    
    def lexical_diversity(self) -> float:
        '''Calculates the lexical diversity of the text - vocab / word_count.'''
        if self.word_count() == 0:
            return 0.00
        else: 
            diversity_score = self.count_vocabulary() / self.word_count()
            return round(diversity_score, 2)
    
    
    def sentence_count(self) -> int:
        '''Counts the number of sentences in the text.'''
        return len(nltk.sent_tokenize(self.text, language='danish'))
    
    
    def words_in_sentences(self) -> float:
        '''Counts the average number of words in a sentence.'''
        if self.sentence_count() == 0:
            return 0.00
        else:
            avg_words_per_sentence = float(self.word_count() / self.sentence_count())
            return round(avg_words_per_sentence, 2)
    
    
    def text_statistics(self, file_path: str) -> pd.Series:
        '''A function that returns a pandas series with text statistics.'''
        data = {
            'workid': self.extract_workid(file_path),
            'character_count': self.character_count(),
            'token_count': self.token_count(),
            'word_count': self.word_count(),
            'vocabulary_count': self.count_vocabulary(),
            'sentence_count': self.sentence_count(),
            'avg_words_in_sentence': self.words_in_sentences(),
            'mean_word_length': self.mean_word_length(),
            'lexical_diversity': self.lexical_diversity()
        }
    
        # Check if any of the data keys are missing or None
        if len(data) == 9:
            series = pd.Series(data) 
            series.name = self.extract_workid(file_path)  # Set the name to the workid or any relevant identifier
            return series
        else:
            self.logger.error('Incomplete text statistics for %s Data %s', file_path, data)
            return None


    def merge_dataframes(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        '''Merges two dataframes based on the workid.'''
        try:
            merged_df = pd.merge(df1, df2, on='workid', how='right')
            return merged_df
        except Exception as e:
            self.logger.error('An error occurred while merging the dataframes: %s', type(e).__name__)
            return None
    
    
    def process_texts(self) -> pd.DataFrame:
        '''Process all text files in the directory and returns a combined dataframe.'''
        self.logger.info('Starting text processing for directory: %s', self.directory) 
        
        series_list = []
        
        for filename in os.listdir(self.directory):
            if not '_titles' in filename and filename.endswith('.text'):
                file_path = os.path.join(self.directory, filename)
        
                try:
                    self.add_file(file_path)
                    series_list.append(self.text_statistics(file_path))
                except Exception as e:
                    self.logger.error('Error processing file %s : %s', file_path, type(e).__name__)

    
        text_statistics = pd.DataFrame(series_list)
        
        df_titles = self.get_titles()
        combined_df = self.merge_dataframes(df_titles, text_statistics)
        self.logger.info('Text processing completed. Combined DataFrame shape: %s', combined_df.shape)
        
        # check if the DataFrame contains any None or invalid values and log them
        for column in combined_df.columns:
            for value in combined_df[column]:
                if value is None or (isinstance(value, (int, float)) and (value <= 0)):
                    workid = self.extract_workid(file_path)
                    self.logger.warning('Invalid value %s for: %s in file: %s in combined DataFrame', value, column, workid)
        
        return combined_df


    def __repr__(self) -> str:
        return f'Class that processes {len(os.listdir(self.directory))} number of texts from {self.directory} and returns a DataFrame with statistics on the text files in the directory.'

 
if __name__ == "__main__":
    
    # test the class
    directory = '/home/astrid/dev/py_files/test_texts/'
    
    if os.path.isdir(directory):
        test = TextStatistics(directory)
        df = test.process_texts()
        print(df)
    else:
        print(f"Directory '{directory}' not found.")

    print('The text_processor script has been run.')
    

    

