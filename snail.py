# -*- coding: utf-8 -*-
"""
Usage :
 > python snail.py -n 1200000
 
@author: iceland
"""
import secp256k1 as ice
import time
import os
import sys
import random
import argparse

#==============================================================================
parser = argparse.ArgumentParser(description='This tool use random number reusability for sequentially searching all unsolved BTC puzzles', 
                                 epilog='Enjoy the program! :)    Tips BTC: bc1q39meky2mn5qjq704zz0nnkl0v7kj4uz6r529at')
parser.version = '02052023'
parser.add_argument("-p", help = "Unsolved Puzzles file. default=unsolved.txt", action="store")
parser.add_argument("-n", help = "Total sequential search in 1 loop. default=1000000", action='store')

args = parser.parse_args()
#==============================================================================

seq = int(args.n) if args.n else 1000000  # 1 Million
p_file = args.p if args.p else 'unsolved.txt'  # 'unsolved.txt'

if os.path.isfile(p_file) == False:
    print('File {} not found'.format(p_file))
    sys.exit()
puzz = {int(line.split()[0]):line.split()[1] for line in open(p_file,'r')}
puzz_bits = list(puzz.keys())
puzz_h160 = [bytes.fromhex(ice.address_to_h160(line)) for line in puzz.values()]
#==============================================================================

# Very Very Slow. Made only to get a random number completely non pseudo stl.
def randk(bits):
    return random.SystemRandom().randint(2**(bits-1), -1+2**bits)

def print_success(my_key):
    print('\n============== KEYFOUND ==============')
    print(f'Puzzle FOUND PrivateKey: {hex(my_key)}   Address: {ice.privatekey_to_address(0, True, my_key)}')
    print('======================================')
    with open('KEYFOUNDKEYFOUND.txt','a') as fw:
        fw.write('Puzzle_FOUND_PrivateKey '+hex(my_key)+'\n')
    exit()
    
def chunks(s):
    for start in range(0, 65*seq, 65):
        yield s[start : start + 65]

def display_time(seconds):
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}"
    
#==============================================================================

print('\n[+] Starting Program.... Please Wait !')
print(f'[+] Search Mode: Sequential Random in each Loop. seq={seq}')
print(f'[+] Total Unsolved: {len(puzz_bits)} Puzzles in the bit range [{min(puzz_bits)}-{max(puzz_bits)}]')

loop = 0
start = time.time()
while True:
    try:
        key_int = randk(160)
        loop += 1
        counter = 0
        for cbits in puzz_bits:
            counter += 1
            bitkey = int('1'+bin(key_int)[2:][(1+160-cbits):], 2)
            P = ice.scalar_multiplication(bitkey)
            if ice.pubkey_to_h160(0, True, P) in puzz_h160: 
                print_success(bitkey)
                
            cnt = 0
            for t in chunks(ice.point_sequential_increment(seq, P)):
                curr160 = ice.pubkey_to_h160(0, True, t)
                if curr160 in puzz_h160:
                    print_success(bitkey + cnt + 1)

                cnt += 1
            elapsed = time.time() - start
            speed = ( (loop-1)*(seq+1)*len(puzz_bits) + (seq+1)*counter ) / elapsed
            print(' '*120,end='\r')
            print(f'[Loop: {loop}] [Puzzle: {cbits} bit] [Speed: {speed:.2f} K/s] [{display_time(elapsed)}] [{hex(bitkey)}]', end='\r')
    except(KeyboardInterrupt, SystemExit):
        exit('\nSIGINT or CTRL-C detected. Exiting gracefully. BYE')
