from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image
import time

import Database_Del, ObjectStudio, ProcessStudio_del,ProcessStudio,HandlerStudio
output_store={'Page1':{"y":100,"rt":54545}}

# importing pandas as pd
import pandas as pd

# dictionary of lists
dict = {'name': ["aparna", "pankaj", "sudhir", "Geeku"],
        'degree': ["MBA", "BCA", "M.Tech", "MBA"],
        'score': [90, 40, 80, 98]}

# creating a dataframe from a dictionary
df = pd.DataFrame(dict)

# iterating over rows using iterrows() function
print(df)
for i, j in eval('df').iterrows():
    print(j['name'])
