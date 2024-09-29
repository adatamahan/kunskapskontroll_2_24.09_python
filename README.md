
<b> Astrid Hansen <br>
Ec Utbildning <br>
Kunskapskontroll 2<br>
24.09 <br>
</b>
<br>
This repository contains scripts that load text files through a shell script from KB's repository, extract statistics from the texts using the NLTK library, and return a dataframe with statistics that are saved to an SQLite database. The original shell script has been modified to accept a prefix and load files accordingly based on this information. The scripts can be used to produce text statistics for each author in the text folder of the KB repository, paving the way for further literary analysis.
<br>
<br>

## Contents
- main.py : main script that imports the other scripts and executes the flow<br>
- load_from_repo.py : a script that unpacks .xml files and imports texts into a directory <br>
- text_processor.py : a script that processes the texts and returns a DataFrame with various text statistics <br>
- data_handlar.py :  a script that saves or reads DataFrames to a SQlite database<br>

<b>Imported files from https://github.com/kb-dk/public-adl-text-sources</b><br>
- extra_stuff_prefix.sh : a modified script from the repo that unpacks xml files based on the prefix parameter <br>
- texts : a folder containing .xml files with texts and title information <br>
- get_the_text.xsl : creates one text file per title in the TEI file. <br>
- get_titles.xsl : creates a list of works inside a TEI file. <br>

<b>Tests folder</b><br>
- test_script : a script that performs various pytests of the scripts excluding the main.py script
- test_text : a folder containing text files for testing purposes <br>
- test_text_database.db : the created test database <br>
- screen shot from performed pytest <br>
        
<b>Directories, databases and other files</b><br>
- requirements.txt : a txt file with the packages for the environment <br>
- log_file.log : a logfile with the logged information <br>
- hca_directory : the folder with retrieved texts <br>
- hca_database : the created hca database <br>
- screen shot from Task Schedular: the above files are fitted for WSL. The script scheduled in task manager are the one below. <br>
- main_windows.py : the main script excluding the module load_from_repo.py <br>
<br>

## Output

Below are the first lines 5 rows and 11 columns of the DataFrame with text statistics for the processed texts in the H.C. Andersens Eventyr text directory.

|    | prefix     | workid      | title                                                       |   character_count |   token_count |
|---:|:-----------|:------------|:------------------------------------------------------------|------------------:|--------------:|
|  0 | hcaeventyr | workid60587 | Folkesangens Fugl. En Stemning                              |              5966 |          1285 |
|  1 | hcaeventyr | workid73931 | Nye Eventyr og Historier. Anden Række. Anden Samling. 1862  |            128897 |         27987 |
|  2 | hcaeventyr | workid74377 | Laserne                                                     |              3766 |           843 |
|  3 | hcaeventyr | workid89462 | Verdens deiligste Rose.                                     |              4480 |           995 |
|  4 | hcaeventyr | workid71035 | Eventyr, fortalte for Børn. Ny Samling. Første Hefte. 1838. |             49663 |         10872 |

<br>

|    |   word_count |   vocabulary_count |   sentence_count |   avg_words_in_sentence |   mean_word_length |   lexical_diversity |
|---:|-------------:|-------------------:|-----------------:|------------------------:|-------------------:|--------------------:|
|  0 |          964 |                490 |               70 |                   13.77 |               4.58 |                0.51 |
|  1 |        21938 |               4256 |             1103 |                   19.89 |               4.49 |                0.19 |
|  2 |          630 |                313 |               55 |                   11.45 |               4.35 |                0.5  |
|  3 |          752 |                336 |               40 |                   18.8  |               4.45 |                0.45 |
|  4 |         8807 |               1850 |              360 |                   24.46 |               4.3  |                0.21 |





 
