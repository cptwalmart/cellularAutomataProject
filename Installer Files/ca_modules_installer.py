""" Requirements for this installer to work properly. """
# Must have pip installer installed on computer.
# Will check if pip is installed on computer; if not, this script will install pip (for windows).

import os
from sys import platform

if platform == "linux" or platform == "linux2": # linux
    try:
        os.system('python3 -m pip3 install numpy==1.19 matplotlib sympy PyQt5')
    except:
        print("There was a problem installing the proper modules.\nMake sure 'ca_needed_modules.txt' is in the same directory as this python script is.\n")
    else:
        print("All of the needed modules for the cellular automata app were installed properly.\n")

elif platform == "darwin": # OS X
    try:
        os.system('python3 -m pip3 install numpy==1.19 matplotlib sympy PyQt5')
    except:
        print("There was a problem installing the proper modules.\nMake sure 'ca_needed_modules.txt' is in the same directory as this python script is.\n")
    else:
        print("All of the needed modules for the cellular automata app were installed properly.\n")

elif platform == "win32": # Windows.
    try:
        os.system('pip3 install numpy==1.19 matplotlib sympy PyQt5')
    except:
        print("There was a problem installing the proper modules.\nMake sure 'ca_needed_modules.txt' is in the same directory as this python script is.\n")
    else:
        print("All of the needed modules for the cellular automata app were installed properly.\n")
