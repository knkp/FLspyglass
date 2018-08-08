###########################################################################
#  Spyglass - Visual Intel Chat Analyzer								  #
#  Copyright (C) 2017 Crypta Eve (crypta@crypta.tech)                     #
#																		  #
#  This program is free software: you can redistribute it and/or modify	  #
#  it under the terms of the GNU General Public License as published by	  #
#  the Free Software Foundation, either version 3 of the License, or	  #
#  (at your option) any later version.									  #
#																		  #
#  This program is distributed in the hope that it will be useful,		  #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of		  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the		  #
#  GNU General Public License for more details.							  #
#																		  #
#																		  #
#  You should have received a copy of the GNU General Public License	  #
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.  #
###########################################################################

import os
import sys

def changeUnixToWinPath(path):
    tokens = path.split('/')
    for x in range(0, len(tokens) - 1):
        tokens[x] = tokens[x] + '\\'
    winPath = "".join(tokens)
    print winPath
    return winPath
        

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller
    """
    returnpath = ''
    if getattr(sys, 'frozen', False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    else:
        basePath = os.path.abspath(".")
    if sys.platform.startswith("win32"):
        returnpath = os.path.join(basePath, changeUnixToWinPath(relativePath))
    else:
        returnpath = os.path.join(basePath, changeUnixToWinPath(relativePath))
    return returnpath
