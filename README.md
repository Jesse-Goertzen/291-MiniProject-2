# 291-MiniProject-2

Jesse Goertzen 1505959

Zachary Kist 1508381

bsddb3 from https://www.lfd.uci.edu/~gohlke/pythonlibs/#bsddb3 

  Select version appropriate for version of Python: cp##, and Windows: win32 or win_amd64
  
  Install using pip: `pip install bsddb3-6.1.1-cp##-none-win$$$$.whl`

We also included the module tabulate in tabulate.py to print our results cleanly. 

  Source https://pypi.org/project/tabulate/
  
  
# Current Issues

Prices -- Royally messed up

Dates outside the range of the data crash the program. Should be easy to fix

betweenDates() and betweenPrices() currently are not updated to not use structs, should be a matter of referencing the other methods and fixing.
