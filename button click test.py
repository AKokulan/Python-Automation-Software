import tkinter as tk


class App(object):
    def new_row(self):
        # Create widgets
        new_entry = tk.Entry(root, width=7)

        # Put widgets in grid
        self.num_rows += 1
        new_entry.grid(column=0, row=self.num_rows, sticky='WE')

    def __init__(self):
        self.num_rows = 1
        createRow_button = tk.Button(
            root, text='New Row', command=self.new_row)
        createRow_button.grid()

root = tk.Tk()
app = App()
root.mainloop()