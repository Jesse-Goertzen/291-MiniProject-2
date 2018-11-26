# 291-MiniProject-2

Jesse Goertzen 1505959

Zachary Kist 1508381

bsddb3 from https://www.lfd.uci.edu/~gohlke/pythonlibs/#bsddb3 

  Select version appropriate for version of Python: cp##, and Windows: win32 or win_amd64
  
  Install using pip: `pip install bsddb3-6.1.1-cp##-none-win$$$$.whl`

We also included the module tabulate in tabulate.py to print our results cleanly. 

  Source https://pypi.org/project/tabulate/
  
We did not collaborate with anyone else
# Current Issues

Sorting files in phase1 needs to use linux commands

TESTING

Our testing strategy for phase 1 was simply looking at the text file that was created and comparing and contrasting to the refrence tables that were provided. We used the windows file compare command, FC to find the differences between our tables and the refrence tables. After finding differences we were able to go to the original file that we were sorting from and look up the location where our results were wrong. This often made it apparent what the issue was, because we were able to see the string containing something that we had not expected and made a case for. Testing phase 2 was done with using some of the "iteration" code from the slides to go through the databases and print out what they contained. This way we were able to put the code into each function and see their results.

Our testing strategy in phase 3 evolved from testing trivial base cases to testing complex edge cases. While creating the database we tested it in batches, such that whenever
a method was "complete" we tested the trivial cases. The trivial cases we used were for testing the base functionality of our program.
Using the queries from simple cases that were easy to follow to ensure that they were correct. Utilizing the smaller test table to be able to know each entry, so that
it was clear what each query should be returning. These queries did not often present any issues but proved that our code and logic were functional. Eventually as more of our program was developed we began to use more complex test cases. These test cases started to involve thinking of edge cases. Testing the boundaries of the queries, the literal edges of the files. Testing complex queries that involved multiple queries. We used a counter to show the amount of results in the table, so that it was easier for us to see if our results matched what we knew was in the table. Once we knew that it was working on the smallest database that we were familar with we started testing it on the larger datasets that were provided. These took more time to cross check that our results were correct.
