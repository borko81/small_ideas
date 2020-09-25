'''
Generate some random, number ask user to input
choice. 
'''

import random
import sys
search_number = random.randint(1, 10)


class CustomError(Exception):
    '''Custom error exception'''
    pass


# Ask for number for cycle to checj if user found correct number or not
try:
    valid_input = int(sys.argv[1])
    if valid_input <= 0:
        raise CustomError
except IndexError as e:
    print('Please enter number for cycle')
    sys.exit()
except ValueError as e:
    print('Please enter valid input (must be positive integer)')
    sys.exit()
except Error:
    print('Please enter positive integer number')
    sys.exit()

# Ask for user inpur and enter in while cycle
user_answer = int(input("[{}] Enter number :".format(valid_input)))

while valid_input > 1:
    if search_number > user_answer:
        print('+')
    elif search_number < user_answer:
        print('-')
    else:
        print('Found the number {}'.format(search_number))
        break

    valid_input -= 1
    user_answer = int(input("[{}] Enter number :".format(valid_input)))


if valid_input == 1:
    print('End game')
