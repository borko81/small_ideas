from tkinter import Tk, Label, Entry, Button, N, W, StringVar
import datetime
import time
import os
from firebird_connect.fdb_con import Fdb_Class, database, database_skl
from query.query_sold import sold, purhcase

# Needed to concat with file name for brilliance
X_TIME = datetime.datetime.now()
FORMATTED_TIME = X_TIME.strftime("%d_%m_%Y__%H_%M")

# Save file to user plot
PATH_TO_FOLDER = os.environ['USERPROFILE']


def read_what_you_need_from_gui():
    """
        Return first and last number of needed fak.
    """
    f_data = str(one.get())
    l_data = str(two.get())
    data = {'first': f_data, 'last': l_data}
    return data


def sold_value_from_entry(my_path, query, name):
    """ Get first and last fak number from gui
        write simple txt file
    """
    data = read_what_you_need_from_gui()
    request = Fdb_Class(my_path, data, query)
    file_name = f"{name}-{FORMATTED_TIME}-from-{data.get('first', 0)}-to-{data.get('last', 0)}.txt"
    full_path = os.path.join(PATH_TO_FOLDER, 'Desktop', file_name)
    with open(full_path, 'w') as f:
        for line in request.con_to_firebird_purchase3():
            print('^'.join(str(x).strip() for x in line), file=f)


# Gui configuration
window = Tk()

window.title("Rival - Purchase")
window.geometry('250x150')

# Number one
date_one = Label(window, text="Първа Дата")
date_one.grid(row=0, column=0, sticky='nw')
one_entry = StringVar()
one = Entry(window, textvariable="one_entry")
one.focus()
one.grid(row=0, column=1)

# Number two
date_two = Label(window, text="Последна Дата")
date_two.grid(row=1, column=0, sticky='nw')
two_entry = StringVar()
two = Entry(window, textvariable="two_entry")
two.grid(row=1, column=1)

# Generate button
sold_button = Button(text='Продажби...', command=lambda: sold_value_from_entry(
    database, sold, 'sold'), bg="lightgreen")
sold_button.grid(row=2, columnspan=3, sticky='w'+'e', pady=15, padx=5)

purchase_button = Button(text='Покупки...', command=lambda: sold_value_from_entry(
    database_skl, purhcase, 'purchase'), bg="lightgreen")
purchase_button.grid(row=3, columnspan=3, sticky='w'+'e', pady=4, padx=5)

if __name__ == '__main__':
    window.mainloop()
