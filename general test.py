from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image
import time

import Database_Del, ObjectStudio, ProcessStudio_del,ProcessStudio,HandlerStudio
function_name='function_name'

outcome_name='outcome_name'
page='page'

outcome_script_try = "\ntry:\n\t" + outcome_name + "=" + function_name + "()\n\tif len(str(" + outcome_name + "))>0:\n\t\tif 'int' in  str(type(" + outcome_name + "))  or 'str' in  str(type(" + outcome_name + ")):\n\t\t\t" + outcome_name + "=[" + outcome_name + "]\n\tloop_count = 0 \n\tfor each in" + outcome_name  + ":\n\t\toutput_store[" + page + "]["+ "output_dict[loop_count]['StoreIn']" + "] = " + outcome_name + "[loop_count]" \
                                             "\n\t\tloop_count+=1"

print(outcome_script_try)