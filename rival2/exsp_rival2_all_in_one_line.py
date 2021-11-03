import fdb
from tkinter import *
import datetime

database = {
    "host": "127.0.0.1",
    "database": "hhh",
    "user": "SYSDBA",
    "password": "masterkey",
}


main_query = """
select
fak.number as fnumber,
LPAD(extract(day from fak.date_sdelka), 2, 0) || '.' || LPAD(extract(month from fak.date_sdelka), 2, 0) || '.' || LPAD(extract(year from fak.date_sdelka), 4, 0),
case
    when FAK.FIRMA_ID is null then FAK.MOL
    else FIRMI.NAME_FAK
end as ffirma,
'',
case
    when FAK.FIRMA_ID is null then FAK.MOL
    else FIRMI.mol
end as fmol,
case
    when FAK.FIRMA_ID is null then ''
    else ''
end,
case
    when FAK.FIRMA_ID is null then ''
    else FIRMI.idnomdds
end,
case
    when FAK.FIRMA_ID is null then fak.idnumber
    else FIRMI.bulstat
end,
fak.total,
fak.dds,
(select count(*) from fak_el where fak_el.fak_id = fak.id),
FAK.v_broi,
(select list(fak.number || '|' || fak_el.text || '|' || round(fak_el.kol,2) || '|' || round(fak_el.suma_total,2) || '|' || round(fak_el.suma_dds,2), '|') from fak_el where fak_el.fak_id = fak.id)
from fak
left join FIRMI on FIRMI.ID = FAK.FIRMA_ID
where fak.date_sdelka between ? and ?
"""


def con_to_firebird(query, *args):
    con = fdb.connect(**database)
    cur = con.cursor()
    try:
        cur.execute(query, *args)
    except fdb.Error as e:
        print(e)
    else:
        for line in cur.fetchall():
            yield line
    finally:
        con.close()


def get_date():
    first_data = f_entry.get()
    second_data = l_entry.get()
    return (first_data, second_data)


def main():
    first_data, second_data = get_date()
    extension_format_for_filename = '_'.join(str(datetime.datetime.today()).replace(":", "").split(".")[0].split())
    with open(f"eksp_rival{extension_format_for_filename}.csv", "w") as f:
        for line in con_to_firebird(main_query, (first_data, second_data)):
            line = list(map(str, line))
            f.write("|".join(line) + "\n")


if __name__ == "__main__":
    root = Tk()
    root.title("Експорт Фактури по дати")
    root.geometry("320x250")
    root.resizable(False, False)
    f_data = Label(root, text="Въведете първа дата")
    f_data.grid(row=0, column=0)
    f_entry = Entry()
    f_entry.grid(row=0, column=1)
    f_entry.focus()

    l_data = Label(root, text="Въведете първа дата")
    l_data.grid(row=1, column=0)
    l_entry = Entry()
    l_entry.grid(row=1, column=1)

    b = Button(root, text="Load", command=main)
    b.grid(row=0, column=3, rowspan=2, sticky="nses")
    root.mainloop()
