from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image
import time

#import files
import Database, ObjectStudio, ProcessStudio,ProcessStudio1,HandlerStudio
outcome_dict={'m':''}

try:

    # import modules
    import os


    def function():

        # input
        x = 100
        y = 27

        # output
        m = 10

        # code
        m = x * y
        return m
except Exception as e:
    error = 'Error: Error in running the action as:' + str(e)
    messagebox.showerror('Error', error)
try:
    outcome = function()
    if len(str(outcome))>0:
        print(type(outcome))
        #if str(type(outcome))=="<class 'int'>" or str(type(outcome))=="<class 'str'>":
        if 'int' in  str(type(outcome))  or 'str' in  str(type(outcome)) :
            print('test1')
            outcome=[outcome]
            print(outcome)
        print(outcome)
        loop_count = 0
        for each in outcome_dict:
            outcome_dict[each] = outcome[loop_count]
            loop_count += 1

    print(outcome_dict)
    #if len(outcome_dict)>0:
       # messagebox.showinfo('Result', outcome_dict)
    #messagebox.showinfo('Result', outcome_dict)
except Exception as e:
    error = 'Error: Error in running the action as:' + str(e)
    print(error)
    #messagebox.showerror('Error', error)


x=100
y='test'

print(type(x))
print(type(y))



"\n\toutcome = function()\n\tif len(str(outcome))>0:\n\t\tif str(type(outcome))=='<class 'int'>' or str(type(outcome))=='<class 'str'>': \n\t\t\toutcome=[outcome]\n\tloop_count = 0 \n\tfor each in outcome_dict:\n\t\t\toutcome_dict[each] = outcome[loop_count]\n\t\t\tloop_count += 1"