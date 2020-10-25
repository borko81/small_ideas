from collections import defaultdict
result = defaultdict(dict)

while True:
    line = input()
    if line == 'filter base':
        break

    name, arg = line.split(' -> ')

    if name not in result:
        result[name] = {'Age': 0, 'Salary': 0, 'Position': ''}

    try:
        arg = int(arg)
        result[name]['Age'] += arg
    except ValueError:
        try:
            arg = float(arg)
            result[name]['Salary'] += arg
        except ValueError:
            result[name]['Position'] = arg


result = dict(result)
last_ask = input()

if last_ask == 'Position':
    for k, v in result.items():
        if v[last_ask] != '':
            output = ''
            output += f'Name: {k}\n'
            output += f'Position: {v[last_ask]}\n'
            output += '===================='
            print(output)

elif last_ask == 'Age':
    for k, v in result.items():
        if v[last_ask] != '':
            output = ''
            output += f'Name: {k}\n'
            output += f'Age: {v[last_ask]}\n'
            output += '===================='
            print(output)

elif last_ask == 'Salary':
    for k, v in result.items():
        if v[last_ask] != '':
            output = ''
            output += f'Name: {k}\n'
            output += f'Salary: {v[last_ask]}\n'
            output += '===================='
            print(output)


'''
You have been tasked to sort out a database full of information about employees. You will be given several input lines containing information in one of the following formats:
    • {name} -> {age}
    • {name} -> {salary}
    • {name} -> {position}
As you see you have 2 parameters. There can be only 3 cases of input:
If the second parameter is an integer, you must store it as name and age.
If the second parameter is a floating-point number, you must store it as name and salary.
If the second parameter is a string, you must store it as name and position.
You must read input lines, then parse and store the information from them, until you receive the command 
“filter base”. When you receive that command, the input sequence of employee information should end.
On the last line of input you will receive a string, which can either be “Age”, “Salary” or “Position”. Depending on the case, you must print all entries which have been stored as name and age, name and salary, or name and position.
In case, the given last line is “Age”, you must print every employee, stored with its age in the following format:
Name: {name1}
Age: {age1}
====================
Name: {name2}
. . .


In case, the given last line is “Salary”, you must print every employee, stored with its salary in the following format:
Name: {name1}
Salary: {salary1}
====================
Name: {name2}
. . .
In case, the given last line is “Position”, you must print every employee, stored with its position in the following format:
Name: {name1}
Position: {position1}
====================
Name: {name2}
. . .
NOTE: Every entry is separated with the other, with a string of 20 character ‘=’.
There is NO particular order of printing – the data must be printed in order of input.
'''