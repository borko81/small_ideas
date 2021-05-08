from tkinter import Tk, Label, Entry, Button, N, W

from firebird_connect.fdb_con import con_to_firebird
from query.query_sold import sold

def value_from_entry():
    f = one.get()
    l = two.get()
    data = {'first': f, 'last': l}
    request = con_to_firebird(sold, **data)
    with open(f'sold-{f}-{l}.txt', 'w') as f:
        for line in request:
            print('^'.join(str(x).strip() for x in line), file=f)


window = Tk()

window.title("Rival - Purchase")
window.geometry('250x150')

date_one = Label(window, text="Първа фактура")
date_one.grid(row=0, column=0, sticky='nw')
one = Entry(window)
one.focus()
one.grid(row=0, column=1)

date_two = Label(window, text="Последна фактура")
date_two.grid(row=1, column=0, sticky='nw')
two = Entry(window)
two.grid(row=1, column=1)

result = Button(text='Зареди...', command=value_from_entry, bg="lightgreen")
result.grid(row=2, columnspan=3, sticky='w'+'e', pady=15, padx=5)

window.mainloop()