# Make fak eksport to worflow software

import fdb
from collections import defaultdict
import re
import sys
import os
import csv
import pandas as pd
import openpyxl


# Взема първа и последна фактура за рендж от фактури
try:
    f_faktura = sys.argv[1]
    s_faktura = sys.argv[2]
    try:
        f_faktura = int(f_faktura)
        s_faktura = int(s_faktura)
    except ValueError as e:
        print(e)
        print('Въведете номер на фактура')
        sys.exit()
except IndexError as e:
    print(e)
    print('Въведете начален и краен номер на фактури за експорт')
    sys.exit()


# Hard code param
database_info = {
    'host': 'localhost',
    'database': r'Expect path to database',
    'user': 'Expect username',
    'password': 'Expect password',
    'charset': 'win1251'
}

# Queryset's
get_firma_info = '''
select
fak.number,
fak.date_sdelka,
case
    when fak.firma_id is not null
    then firmi.name_fak
    else fak.mol
end,
case
    when fak.firma_id is not null
    then firmi.bulstat
    else fak.idnumber
end,
case
    when fak.firma_id is not null
    then coalesce(firmi.idnomdds, '')
    else fak.idnumber
end,
'',
'',
'',
''
from fak
left join firmi on firmi.id = fak.firma_id
where fak.number = {} and fak.is_deleted = 0
'''

get_element_info = '''
select
fak.number,
fak_el.text,
'бр' ,
cast(fak_el.kol as int),
round(fak_el.cena, 2),
fak_el.suma_dds,
fak_el.suma_total,
dds_stavka.dds,
pay_tip.name_cyr
from fak_el
inner join fak on fak.id = fak_el.fak_id
inner join dds_stavka on dds_stavka.id = fak_el.dds_id
inner join pay_tip on pay_tip.id = fak.v_broi
where fak_el.fak_id = fak.id and fak.number = {} and fak.is_deleted = 0
'''

PATH_TO_FOLDER = os.environ['USERPROFILE']
EXTENSION = f'{f_faktura}-{s_faktura}'
FILE_NAME = f'workflow{EXTENSION}.csv'
FILE_NAME_FOR_EXCEL = f'workflow{EXTENSION}.xlsx'
REAL_PATH = os.path.join(PATH_TO_FOLDER, FILE_NAME)
EXCEL_FILES = os.path.join(PATH_TO_FOLDER, FILE_NAME_FOR_EXCEL)
print(f'Пътя до файла е: {REAL_PATH}')

# Function's


def conn_to_databse():
    '''Return con to fdb database
       use in function, get_cur
    '''
    try:
        con = fdb.connect(**database_info)
    except fdb.Error as e:
        print(e)
    else:
        return con


def get_cur(query):
    con = conn_to_databse()
    cur = con.cursor()
    try:
        cur.execute(query)
    except fdb.Error as e:
        print(e)
    else:
        for line in cur.fetchall():
            yield line


def main(number):
    result = {'fak': defaultdict(list), 'element': defaultdict(list)}
    # ADD data for dictionary
    for line in get_cur(get_firma_info.format(number)):
        result['fak'][line[0]].append(line[1:])
    for line in get_cur(get_element_info.format(number)):
        result['element'][line[0]].append(line[1:])

    # Read data from dictionary 1
    for x, v in result['fak'].items():
        for i in v:
            yield ";".join(['F', str(x), re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3.\2.\1', str(i[0])),
                            str(i[1]), str(i[2]), str(i[3]), str(i[4]), str(i[5]), str(i[6]), str(i[7])])

        # Read data from dictionary 2
        for i, v in result['element'].items():
            for i in v:
                if i[0].startswith('Нощу') or i[0] == 'Туристически данък' or i[0].startswith('Депозит') or i[0] == 'Спа Услуги':
                    yield ";".join(['U', str(i[0]), str(i[1]), str(i[2]), str(f'{i[3]:.2f}'),
                                    str(f'{i[4]:.2f}'), str(f'{i[5]:.2f}'), str(f'{i[6]:.0f}'), str(i[7])])
                else:
                    yield ";".join(['M', str(i[0]), str(i[1]), str(i[2]), str(f'{i[3]:.2f}'), str(f'{i[4]:.2f}'),
                                    str(f'{i[5]:.2f}'), str(f'{i[6]:.0f}'), str(i[7])])


def write_to_file(number):
    ''' result write to file'''
    with open(REAL_PATH, 'a') as f:
        for line in main(number):
            f.write(line + '\n')


def return_result_to_check():
    '''
        check returne result for corect output.
    '''
    result = defaultdict(list)
    with open(REAL_PATH, 'r') as f:
        csv_file = csv.reader(f, delimiter=';')
        next(csv_file)
        for line in csv_file:
            if line[-1] != '':
                check = float(f'{((float(line[3]) * float(line[4]) + float(line[5])))}')
                result[line[-1]].append(check)

    for k, v in result.items():
        print(f'{k} - {sum(v)}')


if __name__ == '__main__':
    # with open(REAL_PATH, 'a') as f:
    #     f.write('Едно;Две;Три;Четери;Пет;Шест;Седем;Осем' + '\n')
    for f in range(f_faktura, s_faktura + 1):
        write_to_file(f)
    # next two line convert csv to excel file
    read_file = pd.read_csv(REAL_PATH, delimiter=';', encoding='cp1251')
    read_file.to_excel(EXCEL_FILES, index=None, header=True, encoding='utf8')
    return_result_to_check()
