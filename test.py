#Create hiracchical treeview Application
from tkinter import *
from tkinter import ttk
app=Tk()
#App Title
app.title("Python GUI Application ")
#Lable
ttk.Label(app, text="Hierachical Treeview").pack()
#Treeview
tree=ttk.Treeview(app)

#Treeview items
tree["columns"]=("one","two","three")
tree.column("#0", width=270, minwidth=270, stretch=NO)
tree.column("one", width=150, minwidth=150, stretch=NO)
tree.column("two", width=400, minwidth=200)
tree.column("three", width=80, minwidth=50, stretch=NO)

tree.heading("#0",text="Type",anchor=W)
tree.heading("one", text="Output Name",anchor=W)
tree.heading("two", text="Stored In",anchor=W)
tree.heading("three", text="Value",anchor=W)

# Level 1
tree.insert("", 1, 'folder1', text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
tree.insert("", 2, "folder2", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
# Level 2
tree.insert('folder1', "end", "a", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
tree.insert('folder1', "end", "b", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
tree.insert('folder1', "end", "c", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))

tree.pack()
#Calling Main()
app.mainloop()