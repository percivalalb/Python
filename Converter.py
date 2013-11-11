'''
Created on 11 Nov 2013
@author: Alex
'''

from cx_Freeze import setup, Executable

setup(
    name = "test" ,
    version = "0.1" ,
    description = "Random Test" ,
    executables = [Executable("Gui.pyw")],
    )
