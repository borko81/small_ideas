from tkinter import Tk, Label, Entry, Button, N, W

from firebird_connect.fdb_con import con_to_firebird
from query.query_sold import sold


def read_what_you_need_from_gui():
    f_data = one.get()
    l_data = two.get()
    data = {'first': f_data, 'last': l_data}
    return data


def value_from_entry():
    """ Get first and last fak number from gui
        write simple txt file
    """
    data = read_what_you_need_from_gui()
    request = con_to_firebird(sold, **data)
    with open(f"sold-{data.get('first', 0)}-{data.get('last', 0)}.txt", 'w') as f:
        for line in request:
            print('^'.join(str(x).strip() for x in line), file=f)


# Gui configuration
window = Tk()

window.title("Rival - Purchase")
window.geometry('250x150')

# Number one
date_one = Label(window, text="Първа фактура")
date_one.grid(row=0, column=0, sticky='nw')
one = Entry(window)
one.focus()
one.grid(row=0, column=1)

# Number two
date_two = Label(window, text="Последна фактура")
date_two.grid(row=1, column=0, sticky='nw')
two = Entry(window)
two.grid(row=1, column=1)

# Generate button
result = Button(text='Зареди...', command=value_from_entry, bg="lightgreen")
result.grid(row=2, columnspan=3, sticky='w'+'e', pady=15, padx=5)

if __name__ == '__main__':
    window.mainloop()
