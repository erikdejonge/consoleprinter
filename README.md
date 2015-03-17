
# consoleprinter
Console printer with linenumbers, stacktraces, logging, conversions and coloring.

Active8 BV
Active8 (05-03-15)
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
Stacktracing
Object reflection printing

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
```bash
2.48 | unittester.py:85 | == | Can't find tests, looked in test*.py | File "/Users/rabshakeh/workspace/unittester/unittester/unittester.py", line 85 (run_unit_test) | ==
``

##Reflection
```python
with zipfile.ZipFile(zippath) as zf:
    for member in zf.infolist():
        console(member)
```
> ![kindle](res/Screen Shot 2015-03-17 at 17.45.50.png)