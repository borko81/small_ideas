'''
Block open site, add url to host-file
script must be run with admin wrights
'''

# script www.facebook.com -add -> add url ot file
# script www.facebook.com -del -> delete line from file

import sys
import fileinput

PATH_TO_FILE = r'C:\Windows\System32\drivers\etc\hosts'

try:
    name = sys.argv[1]
    choice = sys.argv[2]
except IndexError as e:
    print('Example: ./script-name www.facebook.com -add (to add line) or -del (to remove line)')
    sys.exit()
else:
    if choice == '-add':
        with(open(PATH_TO_FILE, 'a')) as f:
            f.write(f'127.0.0.1 {name}\n')
    elif choice == '-del':
        for line in fileinput.input(PATH_TO_FILE, inplace=True):
            if name in line:
                pass
            else:
                print(line.strip())
        fileinput.close()
