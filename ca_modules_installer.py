""" Requirements for this installer to work properly. """
# Must have the "neededModules.txt" file in same directory/folder in order to install.
# Must have pip installer installed on computer.
import os
try:
    os.system('pip install -r ca_needed_modules.txt')
except:
    print("There was a problem installing the proper modules.\nMake sure 'ca_needed_modules.txt' is in the same directory as this python script is.\n")
else:
    print("All of the needed modules for the cellular automata app were installed properly.\n")
