# PyCrack
Bruteforce attack for zip, 7z, rar

```
usage: pycrack.py [-h] [--start START] [--stop STOP] [--threads THREADS]
                  [--verbose VERBOSE] [--alphabet ALPHABET] [--file FILE]

Python combination generator

options:
  -h, --help           show this help message and exit
  --start START        Number of characters of the initial string [1 -> "a", 2
                       -> "aa"]
  --stop STOP          Number of characters of the final string [3 -> "ßßß"]
  --threads THREADS    Number cpu use for cracking
  --verbose VERBOSE    Show combintations
  --alphabet ALPHABET  alternative chars to combinations
  --file FILE          archive file

```


#### Example

```
$ python pyrarcrack.py --start 10 --stop 10 --file example_path.rar --alphabet 1234567890

Password found: 1234567890
Time: 0.06715750694274902
```
