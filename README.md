# Datatrail (alpha)
**For Python 3**

### Top sound tracks by The Data Miners, feat. Engineers:

1. Where's that one file, again?
2. So... what are the differences between these files?
3. WTF! Did they delete that?
4. Why the heck is this here?
5. Ummm... when was this made?
6. Screw it! I'll just redo this.
7. Should I quit my job?
8. Can the world end now?

## Log your processes, track down your data with *Datatrail*

#### Start a new log for your project and make a file:
```python
from datatrail import logger
logger.init()       # Only once in the parent directory of your project
file_path = logger.make('new_file.txt')
```

Meanwhile in your .dtrail log...
```
2018-07-21T18:43:42.443233
    Initialized at /home/john/Research/.dtrail

2018-07-21T18:44:00.655391
    make('/home/john/Research/new_file.txt',)
    @RETURN=/home/john/Research/new_file.txt
```

#### And when you want to remove that file:
```python
logger.remove('new_file.txt')
```

Now that's in your log, too!
```
2018-07-21T18:43:42.443233
    Initialized at /home/john/Research/.dtrail

2018-07-21T18:44:00.655391
    make('/home/john/Research/new_file.txt',)
    @RETURN=/home/john/Research/new_file.txt

2018-07-21T18:45:57.828979
    remove('new_file.txt',)
    @RETURN=None
```

#### What about my own data processing functions?
```python
def x(y,z):
    return(y+z)

logger.run(x, 4, 5)
```

That's in the .dtrail log as well!
```
2018-07-21T18:43:42.443233
    Initialized at /home/john/Research/.dtrail

2018-07-21T18:44:00.655391
    make('/home/john/Research/new_file.txt',)
    @RETURN=/home/john/Research/new_file.txt

2018-07-21T18:45:57.828979
    remove('new_file.txt',)
    @RETURN=None

2018-07-21T18:56:15.589604
    x(4,5,)
    @RETURN=9
```

#### Things to help you
| Functions | Descriptions |
| --- | --- |
| **.run**(func, *args, **kwargs) | Run a function |
| **.make**(file_path) | Make a file |
| **.remove**(file_path) | Remove a file |
| **.copy**(src_path, optional_dest_dir) | Copy a file |
| **.move**(src_path, dest_dir) | Move a file |
| **.rename**(src_path, new_name) | Rename a file |
| **.set_verbose**(True) | To make it talk a lot, default is **False** |
| **.load**(log_file_path) | Don't need to use this unless changing log |
| **.show_log_path**() | If you forget where the **.dtrail** log is |

## To install
Make sure you are using Python 3
```
$ sudo python3 -m pip install --index-url https://test.pypi.org/simple/ datatrail
```
## Disclaimer
Current version is a bit limiting since it can only work with functions.
Also, obviously, if you don't run everything through logger.run() then nothing gets tracked.

## Functionalities to come
* Command line tools
* Get the history of a specific file
* Date/time filter
* Project file structure/history graph

## Support :)
Via Github or email me at withinfinitelife@gmail.com
