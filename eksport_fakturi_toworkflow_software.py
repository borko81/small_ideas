# Make fak eksport to worflow software

import fdb
from collections import defaultdict
import re
import sys
import os
import csv
import pandas as pd
import openpyxl
from decimal import *


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
    'user': 'expect username',
    'password': 'expect password',
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
pay_tip.name_cyr,
case
    when fak.tip = 0
    then 'Фактура'
    else 'КИ'
end
from fak
left join firmi on firmi.id = fak.firma_id
inner join pay_tip on pay_tip.id = fak.v_broi
where fak.number = {} and fak.is_deleted = 0
'''

get_element_info = '''
select
fak.number,
fak_el.text,
'бр' ,
cast(fak_el.kol as int),
cast(fak_el.cena as decimal(10, 3)),
fak_el.suma_dds,
fak_el.suma_total,
dds_stavka.dds,
pay_tip.name_cyr,
case
    when fak.tip = 0
    then 'Фактура'
    else 'КИ'
end
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
        result['element'][line[0]].append(line[0:])

    # Read data from dictionary 1
    for x, v in result['fak'].items():
        f = str(x).zfill(10)
        for i in v:
            fak_symbol = 'F'
            fak_number = str(f)  # two times
            fak_number2 = str(f)
            date_time = str(re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3.\2.\1', str(i[0])))
            fak_klient_name = str(i[1])
            bulstat = str(i[2])
            idn_number = str(i[3])
            empty = ''  # two time
            pay_tip = str(i[6])
            fak_type = str(i[7])
            yield ";".join([fak_symbol, fak_number, fak_number2, date_time,
                            fak_klient_name, bulstat, idn_number, empty, empty, pay_tip, fak_type])

    # Read data from dictionary 2
    for f, v in result['element'].items():
        f = str(f).zfill(10)
        for i in v:
            fak_number = str(i[0]).zfill(10)
            usl_name = str(i[1])
            element_br = i[2]
            kol = str(i[3])
            ed_price = i[4]
            ed_price = str(round(float(i[4]), 2))
            dds_price = f'{(i[5]):.2f}'
            total_price = f'{(i[6]):.2f}'
            dds = f'{i[7]:.0f}'
            pay_type = str(i[8])
            fak_type = str(i[9])
            # print(fak_number, usl_name, element_br, kol, ed_price, dds_price, total_price, dds, pay_type)
            if usl_name.startswith('Нощу') or usl_name == 'Туристически данък' or usl_name.startswith('Депозит') \
                    or usl_name == 'Спа Услуги' or usl_name == 'Връщане на сума' or usl_name.startswith('Авансово'):
                yield ";".join(['U', f, usl_name, element_br, kol,
                                ed_price, dds_price, total_price, dds, pay_type, fak_type])
            else:
                yield ";".join(['M', f, usl_name, element_br, kol,
                                ed_price, dds_price, total_price, dds, pay_type, fak_type])


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
            if line[0].startswith('U') or line[0].startswith('M'):
                check = float(f'{((float(line[4]) * float(line[5]) + float(line[6])))}')
                result[line[-2]].append(check)

    for k, v in result.items():
        print(f'{k} - {sum(v)}')


if __name__ == '__main__':
    with open(REAL_PATH, 'a') as f:
        f.write('Тип;Номер;Елемент;Дата;Име;Булстат;ИдНомер;Тотал;ДДС;Вид Плащане;Тип Фактура' + '\n')
    for f in range(f_faktura, s_faktura + 1):
        # main(f) # -> open for test with print
        write_to_file(f)
    # next two line convert csv to excel file
    read_file = pd.read_csv(REAL_PATH, delimiter=';', encoding='cp1251', dtype='str')
    read_file['Тотал'] = read_file['Тотал'].astype('float')
    read_file['ДДС'] = pd.to_numeric(read_file['ДДС'], errors='coerce')


    read_file.to_excel(EXCEL_FILES, index=None, header=True, encoding='utf8', sheet_name='Workflow')
    return_result_to_check()
