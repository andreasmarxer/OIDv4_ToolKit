# Code written by Andreas Marxer, ASL ETH

import os
from tqdm import tqdm

# Path to directory with txt files
path = 'OID/Dataset/train/Window_Mirror/Label'

# Change current directory to specified directory
os.chdir(path)

# For every file in this directory
for filename in tqdm(os.listdir(os.getcwd())):
    print('Current file: ' + filename)
    os.rename(filename, 'old_' + filename)
    print('Renamed in: old_' + filename)

    # Open txt file, modify and save it again
    with open('old_' + filename, 'r') as file_in:
        with open(filename, 'w') as file_out:
            for line in file_in:
                #split the line in first word and rest
                old_class, other = line.split(None,1)

                #new class is WinMir if oldclass is Window or Mirror
                if old_class is 'Window' or 'Mirror':
                    new_class = 'WinMir'
                else:
                    print('ERROR, old class is not Mirror or Window')
                    new_class = 'ERROR'

                line = '%s %s' % (new_class, other)
                file_out.write(line)
