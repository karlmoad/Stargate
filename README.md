# STARGATE

**Transporting your data from excel to database.** 

Project is only compatable with Python3, Python 2.x is not supported 

**Prep:**

```
$ git clone https://github.com/karlmoad/Stargate.git
$ cd Stargate
$ pip install -r requirements.txt
```

**Run:**

The program runs in two forms, interactive command line and command argument driven. 

To see available command arguments:

```
$ python stargate.py -h
```

 To execute in interactive mode: supply no command parameters

```
$ python stargate.py
```

**Notes:** 

- To configure database connections you must execute the command in interactive mode
- During command argument execution mode if a required argument value is not suppled the program will invoke the interactive mode elements to collect the data elements.
- Default configuration is stored at **$HOME/.stargate/config.json**

