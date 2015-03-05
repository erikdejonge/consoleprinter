
# consoleprinter
Console printer with linenumbers, stacktraces, logging, conversions and coloring.

Active8 BV
erik@a8.nl (05-03-15)
license: GNU-GPL2

##install
```bash
pip install consoleprinter
```

##contains
Utility functions for working with commandline applications.
Logging
Printing
Exception parsing

##usage
```python
from consoleprinter import console

colors = ['black', 'blue', 'cyan', 'default', 'green', 'grey', 'magenta', 'orange', 'red', 'white', 'yellow']

for color in colors:
    console(color, color=color)
```

## PyCharm
Console detects when run in PyCharm or Intellij, and adds links to the orinating line
```python
    if len(suite._tests) == 0:
        console_warning("Can't find tests, looked in test*.py")

```
```
2.48 | unittester.py:85 | == | Can't find tests, looked in test*.py | File "/Users/rabshakeh/workspace/unittester/unittester/unittester.py", line 85 (run_unit_test) | ==
``