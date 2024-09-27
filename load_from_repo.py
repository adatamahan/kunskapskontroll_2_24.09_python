# load_from_repo.py

#!/home/astrid/dev/.conda/bin/python3

'''
A script that imports texts and titles via a shell script from kb.dk's repository https://github.com/kb-dk/public-adl-text-sources
The script extract_stuff.sh from the repository have been modified to accept prefix as a parameter.
See updated script extract_stuff_prefix.sh below
Run chmod +x extract_stuff_prefix.sh to make the script executable.

---------------------------------------------------------------------

#!/bin/bash

prefix=${1:-hcaeventyr0}

tei_files=(texts/${prefix}*)

for file in ${tei_files[@]}; do

    echo $file
    data_file_base=`basename "$file" .xml`

    xsltproc  get_titles.xsl $file > "$data_file_base"_titles.text
    xsltproc --stringparam source "$data_file_base"  get_the_text.xsl  $file
    
done
---------------------------------------------------------------------

'''

import subprocess
import os
import shutil
import logging


class FileProcessor:
    '''A class that runs a bash shell script that loads text files into a directory. 
        The loaded text files are afterwards moved to another directory.'''
        
    def __init__(self, bash_script: str, source_dir: str, dest_dir: str) -> None:
        self.bash_script = bash_script
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.logger = logging.getLogger(__name__)
        

    def run_shell_script(self, prefix: str) -> None:
        '''Run the shell script with the prefix parameter.'''
        result = subprocess.run(['bash', self.bash_script, prefix], capture_output=True, text=True)

        if result.returncode != 0:   # unix convention: 0 is success
            self.logger.error('Error: %s', result.stderr)
        else:
            self.logger.info('Shell script executed successfully.')
            

    def move_files(self) -> None:
        '''Move the retrieved files to a folder in the workspace.'''
        os.makedirs(self.dest_dir, exist_ok=True)
        
        for filename in os.listdir(self.source_dir):
            if filename.endswith('.text'):
                source_file = os.path.join(self.source_dir, filename)
                dest_file = os.path.join(self.dest_dir, filename)
                shutil.move(source_file, dest_file)
                

    def process(self, prefix: str) -> None:
        '''Run the entire process.'''
        try:
            self.run_shell_script(prefix)
            self.move_files()
            self.logger.info('Files moved from %s to %s', self.source_dir, self.dest_dir)
        except Exception as e:
            self.logger.error('Error processing files: %s', type(e).__name__)


if __name__ == "__main__":
    
    # testing the class
    processor = FileProcessor(
        bash_script ='extract_stuff_prefix.sh',
        source_dir ='/home/astrid/dev/py_files/',
        dest_dir ='/home/astrid/dev/hca_text_directory/'
    )
    processor.process('hcaeventyr0')
    
    print('load_from_repo.py has been run.')
