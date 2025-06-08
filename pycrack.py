"""
Bruteforce attack
"""

from argparse import ArgumentParser
from itertools import chain, product
from os.path import exists
from string import printable
from subprocess import PIPE, Popen
from time import time
import threading
import math

chars = (
    printable
    + 'ÁáÂâàÀÃãÅåÄäÆæÉéÊêÈèËëÐðÍíÎîÌìÏïÓóÒòÔôØøÕõÖöÚúÛûÙùÜüÇçÑñÝý®©Þþß'
)

special_chars = "();<>`|~\"&\'}]"

parser = ArgumentParser(description='Python combination generator')
parser.add_argument(
    '--start',
    help='Number of characters of the initial string [1 -> "a", 2 -> "aa"]',
    type=int,
)

parser.add_argument(
    '--stop',
    help='Number of characters of the final string [3 -> "ßßß"]',
    type=int,
)

parser.add_argument(
    '--threads',
    help='Number cpu use for cracking',
    type=int,
    default = 2,
)

parser.add_argument(
    '--verbose', help='Show combintations', default=False, required=False,
)

parser.add_argument(
    '--alphabet',
    help='alternative chars to combinations',
    default=chars,
    required=False,
)

parser.add_argument('--file', help='archive file', type=str)

args = parser.parse_args()


def generate_combinations(alphabet, length, start=1):
    """Generate combinations using alphabet."""
    yield from (''.join(string)
        for string in chain.from_iterable(
            product(alphabet, repeat=x) for x in range(start, length + 1)
        )
    )

    
def format(string):
    """Format chars to write them in shell."""
    formated = map(
        lambda char: char if char not in special_chars else f'\\{char}', string
    )
    return ''.join(formated)


def checker(string_combination, string_check, start_time):
    """Check if password is correct"""
    for combination in string_combination:
        if stop_event.is_set():
            break

        formated_combination = format(combination)

        if args.verbose:
            print(f'{time() - start_time:.2f} -> try:{combination}')

        cmd = Popen(
            f'7zz t -p{formated_combination} {args.file}'.split(),
            stdout=PIPE, stderr=PIPE)

        out, err = cmd.communicate()
        if 'Everything is Ok' in out.decode():
            stop_event.set()
            print(f'FOUND:{combination}')
            exit()

        if combination == string_check:
            break

def get_string_position():
    """ Get order number of middle string"""
    total = 0
    temp = args.start
    for i in range(args.stop-args.start + 1):
        total += pow(len(args.alphabet),temp)
        temp +=1
    return total//args.threads

stop_event = threading.Event()

if __name__ == '__main__':
    if not exists(args.file):
        print(f"File {args.file} not found!")
        exit()

    if args.stop < args.start:
        print('Stop number is less than start')
        exit()

    start_time = time()
   
    string_combination = list(generate_combinations(args.alphabet, args.stop, args.start))
    temp = get_string_position()

    threads = []
    for i in range(args.threads):
        if i+1 <  args.threads:
            string_check = string_combination[(i+1)*temp-1]
        else:
            string_check = string_combination[-1]
        
        t = threading.Thread(target=checker, args=(string_combination[i*temp::],string_check, start_time))
        threads.append(t)
        t.start()
