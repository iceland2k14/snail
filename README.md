## Info
_Attempt to search unsolved 84 puzzles keys of 1000 BTC_  
The program starts with a random number in 160 bit and then use this to create masked keys in each bit space of 160 bit till 66 bit. The total puzzles to search can be controlled through the _unsolved.txt_ file. Using the specified value -n, (default = 1 million) the program searches for each bit range the sequential search and checks with the hash160 of the unsolved puzzles. Therefore 1 random number generated in 160 bit is reused for all the lower puzzles to check if they got any collision in respective bitrange. The outer Loop is repeated once 1 search for all the bit range is completed in their respective sequential -n million keys.

This script is slow, that's why the name ***snail*** search. Currenly single CPU.

## Requirements
The required library (3 files) can be obtained from the location https://github.com/iceland2k14/secp256k1


# Run
```
(base) C:\Anaconda3>python snail.py

[+] Starting Program.... Please Wait !
[+] Search Mode: Sequential Random in each Loop. seq=1000000
[+] Total Unsolved: 84 Puzzles in the bit range [66-160]
[Loop: 1] [Puzzle: 67 bit] [Speed: 189553.38 K/s] [00:00:10] [0x7a35ff50e782a0754]
SIGINT or CTRL-C detected. Exiting gracefully. BYE

(base) C:\Anaconda3>python snail.py -h
usage: snail.py [-h] [-p P] [-n N]

This tool use random number reusability for sequentially searching all unsolved BTC puzzles

optional arguments:
  -h, --help  show this help message and exit
  -p P        Unsolved Puzzles file. default=unsolved.txt
  -n N        Total sequential search in 1 loop. default=1000000

Enjoy the program! :) Tips BTC: bc1q39meky2mn5qjq704zz0nnkl0v7kj4uz6r529at

```
