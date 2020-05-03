from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
import os,shutil
from datetime import datetime
import tkinter

import Database
import GuiGloballVariable
import ProcessStudio

class ObjectStudio(object):

    def __init__(self,root,db,object_studio_notebook):
        self.root=root
        self.object_studio_notebook=object_studio_notebook
        self.num_rows = 4
        self.database=db
        self.studio_window=''

    def get_variables(self,os_modules_handle_om_var,os_modules_action_om_var,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):

        global os_modules_handle_optionmenu_var,os_modules_action_optionmenu_var
        os_modules_handle_optionmenu_var=os_modules_handle_om_var
        os_modules_action_optionmenu_var=os_modules_action_om_var

        '''global fr_os_module_table,frame_os_module_config
        fr_os_module_table = object_studio_module_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0]
        frame_os_module_config = (object_studio_module_tab.winfo_children()[4])

        global fr_os_input_table,lb_os_input_config_handle_value,lb_os_input_config_action_value
        fr_os_input_table = ((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0]
        lb_os_input_config_handle_value=(object_studio_input_tab.winfo_children()[4]).winfo_children()[1]
        lb_os_input_config_action_value=(object_studio_input_tab.winfo_children()[4]).winfo_children()[3]


        global  fr_os_output_table,lb_os_output_config_handle_value,lb_os_output_config_action_value
        fr_os_output_table = ((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0]
        lb_os_output_config_handle_value=((object_studio_output_tab.winfo_children()[4]).winfo_children()[1])
        lb_os_output_config_action_value=((object_studio_output_tab.winfo_children()[4]).winfo_children()[3])'''

    def row_add_button_call(self,fr_cn_os_run_tbl,wids_per_row,fr_os_run_table,cn_os_run_tbl,sb_run_table):
        children=fr_cn_os_run_tbl.winfo_children()
        no_of_children=0
        rows=0
        for each in children:
            no_of_children+=1
            print(each)
        rows=no_of_children/wids_per_row
        next_row=int(rows+1)
        print('next_row:',next_row)

        var_om_os_run_tbl_handle = StringVar()
        var_choices_om_os_run_tbl_handle = ['Test 1wwwwwwwwwwwwwwwwwwwww']
        om_os_run_tbl_handle = OptionMenu(fr_cn_os_run_tbl, var_om_os_run_tbl_handle, *var_choices_om_os_run_tbl_handle)
        # om_os_run_tbl_handle.grid(row=eaach,column=1,columnspan=2)
        om_os_run_tbl_handle.config(width=30, anchor='w')
        om_os_run_tbl_handle.grid(row=next_row, column=1)

        var_om_os_run_tbl_action = StringVar()
        var_choices_om_os_run_tbl_action = ['Test 1rrrrrrrrrrrrrrrrrrrrrxxx']
        om_os_run_tbl_handle = OptionMenu(fr_cn_os_run_tbl, var_om_os_run_tbl_action, *var_choices_om_os_run_tbl_action)
        om_os_run_tbl_handle.config(width=30, anchor='w')
        om_os_run_tbl_handle.grid(row=next_row, column=2)

        lb_os_run_tbl_input = Label(fr_cn_os_run_tbl, text='Click', fg="blue", width=20, underline=0, relief=RAISED)
        '''lb_os_run_tbl_input.configure(command=lambda button=input_validate_button,
                                                       value_entry=input_value_entry,
                                                       frame=frame:
                                                        self.os_input_row_validate_button_call(button, value_entry, frame))'''

        # lb_os_run_tbl_input.bind('<Button-1>',lambda fr=fr_os_run_table,handle_var=var_om_os_run_tbl_handle,action_var=var_om_os_run_tbl_action : self.os_run_input_window(fr,handle_var,action_var))
        lb_os_run_tbl_input.bind('<Button-1>', lambda fr=fr_os_run_table, handle_var=var_om_os_run_tbl_handle,
                                                      action_var=var_om_os_run_tbl_action: self.os_run_input_window(
            fr, handle_var, action_var))

        lb_os_run_tbl_input.grid(row=next_row, column=3)
        # print(lb_os_run_tbl_input)

        lb_os_run_tbl_output = Label(fr_cn_os_run_tbl, text='Click', fg="blue", width=20, underline=0, relief=RAISED)
        lb_os_run_tbl_output.grid(row=next_row, column=4)

        cn_os_run_tbl.configure(scrollregion=cn_os_run_tbl.bbox('all'), yscrollcommand=sb_run_table.set)

    def lb_onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        global input_lb_selected_value
        input_lb_selected_value = w.get(index)
        print('You selected item %d: "%s"' % (index, input_lb_selected_value))

    def update_input_value_entrybox(self,var_ent):
        print(var_ent)
        var_evt=var_ent.widget
        len_val=(len(var_evt.get()))+2

        #var_evt.delete(0,END)
        text="'&" + str(input_lb_selected_value) + "&'"
        print(text)

        var_evt.insert(len_val,text)
        #print(input_lb_selected_value)
        #var_ent.set(input_lb_selected_value)
        #et_input_value_val.bind('<Button-1>', lambda ent=et_input_value_val: et_input_value_val.insert(0,input_lb_selected_value))

    def os_run_input_window(self,fr_os_run,handle_var,action_var):
        print("in toplevel window")
        input_window=Toplevel(self.studio_window)
        input_window.title('Input')
        input_window.geometry("800x400")


        fr_input_table=Frame(input_window,bg='snow')
        fr_input_table.place(relx=.025, rely=.025, relwidth=.71, relheight=.9)

        fr_input_var_listbox = Frame(input_window, bg='snow')
        fr_input_var_listbox.place(relx=.75, rely=.025, relwidth=.24, relheight=.9)

        cn_input_table=Canvas(fr_input_table)
        sb_input_table=Scrollbar(fr_input_table,orient="vertical",command=cn_input_table.yview)

        fr_cn_input_table=Frame(cn_input_table)

        '''cn_os_run_tbl = Canvas(fr_os_run_table)
        sb_run_table = Scrollbar(fr_os_run_table, orient="vertical", command=cn_os_run_tbl.yview)

        fr_cn_os_run_tbl = Frame(cn_os_run_tbl)'''

        lb_input_name=Label(fr_cn_input_table,text="Input Name", font=("Arial Bold", 10), bg='gray87', width=22,relief=GROOVE).grid(row=1,column=1)
        lb_input_value = Label(fr_cn_input_table, text="Input Value", font=("Arial Bold", 10), bg='gray87', width=43,relief=GROOVE).grid(row=1, column=2)
        lb_input_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=3)

        r=2
        for each in range(30):
            lb_input_name_vale = Label(fr_cn_input_table, text="Input Value", font=("Arial", 10), bg='gray87', width=22).grid(row=r, column=1)
            var_ent=StringVar()
            et_input_value_val=Entry(fr_cn_input_table, width=58,textvariable=var_ent)

            et_input_value_val.grid(row=r, column=2)
            et_input_value_val.bind('<Button-3>', lambda var_ent=var_ent: self.update_input_value_entrybox(var_ent))
            #et_input_value_val.configure(command=lambda ent=et_input_value_val: self.update_input_value_entrybox(ent,var_ent))
            bt_input_validate = Button(fr_cn_input_table, text="", bg='gray87', width=1)
            bt_input_validate.grid(row=r, column=3)
            bt_input_validate.configure(command=lambda bt=bt_input_validate,ent=et_input_value_val,fr=fr_input_table, :self.os_input_row_validate_button_call(bt,ent,fr))
            r+=1

        cn_input_table.create_window(0, 0, anchor = 'nw', window = fr_cn_input_table)

        cn_input_table.update_idletasks()

        cn_input_table.configure(scrollregion=cn_input_table.bbox('all'), yscrollcommand=sb_input_table.set)
        cn_input_table.pack(side='left', expand=True, fill='both')
        sb_input_table.pack(side='right', fill='both')



        sb_variable_listbox = Scrollbar(fr_input_var_listbox)
        sb_variable_listbox.pack(side=RIGHT, fill=Y)

        lb_var = Listbox(fr_input_var_listbox)
        lb_var.pack(side='left',fill='both',expand=True)

        for i in range(100):
            lb_var.insert(END, i)

        # attach listbox to scrollbar
        lb_var.config(yscrollcommand=sb_variable_listbox.set)
        sb_variable_listbox.config(command=lb_var.yview)

        lb_var.bind('<<ListboxSelect>>', self.lb_onselect)


    #-----------------------------------------------------------------------------------------------------------------------
    def os_run_tab(self,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab,object_studio_run_tab):
        fr_os_run_config=Frame(object_studio_run_tab,bg='red')
        fr_os_run_config.place(relx=0.025,rely=.025,relwidth=0.61,relheight=0.1)

        fr_os_run_table = Frame(object_studio_run_tab, bg='red')
        fr_os_run_table.place(relx=0.025, rely=.14, relwidth=0.61, relheight=0.84)

        fr_os_run_inputoutput = Frame(object_studio_run_tab, bg='red')
        fr_os_run_inputoutput.place(relx=0.65, rely=.14, relwidth=0.34, relheight=0.6)

        #sb_run_table.pack(side='right',fill =Y)

        cn_os_run_tbl=Canvas(fr_os_run_table)
        sb_run_table = Scrollbar(fr_os_run_table, orient="vertical", command=cn_os_run_tbl.yview)

        fr_cn_os_run_tbl=Frame(cn_os_run_tbl)
        #cn_os_run_tbl.pack(side=LEFT,fill=BOTH)



        for eaach in range(10):
            print(eaach)
            if eaach==0:
                handle_label = Label(fr_cn_os_run_tbl, text="Module", font=("Arial Bold", 10), bg='gray87', width=27,relief=GROOVE).grid(column=1, row=eaach)
                #handle_label.config(width=30, anchor='w')
                #handle_label.grid(column=0, row=r)

                action_label = Label(fr_cn_os_run_tbl, text="Action", font=("Arial Bold", 10), bg='gray87', width=27,relief=GROOVE).grid(column=2, row=eaach)
                #handle_label.config(width=30, anchor='w')
                input_label = Label(fr_cn_os_run_tbl, text="Input", font=("Arial Bold", 10), bg='gray87', width=17,relief=GROOVE).grid(column=3, row=eaach)
                output_label = Label(fr_cn_os_run_tbl, text="Output", font=("Arial Bold", 10), bg='gray87', width=17,relief=GROOVE).grid(column=4, row=eaach)
            if eaach>0:
                var_om_os_run_tbl_handle=StringVar()
                var_choices_om_os_run_tbl_handle=['Test 1wwwwwwwwwwwwwwwwwwwww']
                om_os_run_tbl_handle=OptionMenu(fr_cn_os_run_tbl,var_om_os_run_tbl_handle,*var_choices_om_os_run_tbl_handle)
                #om_os_run_tbl_handle.grid(row=eaach,column=1,columnspan=2)
                om_os_run_tbl_handle.config(width=30,anchor='w')
                om_os_run_tbl_handle.grid(row=eaach, column=1)

                var_om_os_run_tbl_action = StringVar()
                var_choices_om_os_run_tbl_action = ['Test 1rrrrrrrrrrrrrrrrrrrrrxxx']
                om_os_run_tbl_handle = OptionMenu(fr_cn_os_run_tbl, var_om_os_run_tbl_action, *var_choices_om_os_run_tbl_action)
                om_os_run_tbl_handle.config(width=30,anchor='w')
                om_os_run_tbl_handle.grid(row=eaach, column=2)

                lb_os_run_tbl_input=Label(fr_cn_os_run_tbl,text='Click',fg="blue",width=20,underline=0,relief=RAISED)
                '''lb_os_run_tbl_input.configure(command=lambda button=input_validate_button,
                                                               value_entry=input_value_entry,
                                                               frame=frame:
                                                                self.os_input_row_validate_button_call(button, value_entry, frame))'''

                #lb_os_run_tbl_input.bind('<Button-1>',lambda fr=fr_os_run_table,handle_var=var_om_os_run_tbl_handle,action_var=var_om_os_run_tbl_action : self.os_run_input_window(fr,handle_var,action_var))
                lb_os_run_tbl_input.bind('<Button-1>', lambda fr=fr_os_run_table, handle_var=var_om_os_run_tbl_handle,
                                                              action_var=var_om_os_run_tbl_action: self.os_run_input_window(
                    fr, handle_var, action_var))

                lb_os_run_tbl_input.grid(row=eaach, column=3)
                #print(lb_os_run_tbl_input)

                lb_os_run_tbl_output = Label(fr_cn_os_run_tbl, text='Click', fg="blue", width=20, underline=0,relief=RAISED)
                lb_os_run_tbl_output.grid(row=eaach, column=4)


        cn_os_run_tbl.create_window(0, 0, anchor='nw', window=fr_cn_os_run_tbl)
        cn_os_run_tbl.update_idletasks()

        cn_os_run_tbl.configure(scrollregion=cn_os_run_tbl.bbox('all'), yscrollcommand=sb_run_table.set)

        cn_os_run_tbl.pack(side='left',fill='both',expand=True)
        sb_run_table.pack(side='right',fill ='y')

        cn_fr_inputoutput=Canvas(fr_os_run_inputoutput)
        sb_fr_inputoutput=Scrollbar(fr_os_run_inputoutput,orient="vertical", command=cn_fr_inputoutput.yview)

        fr_on_cn_on_fr_inputoutput = Frame(cn_fr_inputoutput)
        for each in range(30):
            lb=Label(fr_on_cn_on_fr_inputoutput,text="Test Label").pack()

        cn_fr_inputoutput.create_window(0, 0, anchor='nw', window=fr_on_cn_on_fr_inputoutput)
        cn_fr_inputoutput.update_idletasks()

        cn_fr_inputoutput.configure(scrollregion=cn_fr_inputoutput.bbox('all'),
                                yscrollcommand=sb_fr_inputoutput.set)

        cn_fr_inputoutput.pack(side='left', fill='both', expand=True)
        sb_fr_inputoutput.pack(side='right', fill='y')
        #

        fr_os_run_config.grid_rowconfigure(0, weight=1)
        fr_os_run_config.grid_columnconfigure(0, weight=1)
        bt_os_run_tbl_row_add = Button(fr_os_run_config, text="Add",command=lambda fr=fr_cn_os_run_tbl,wids=4,fr2=fr_os_run_table,cn=cn_os_run_tbl,sb=sb_run_table:self.row_add_button_call(fr,wids,fr2,cn,sb))
        bt_os_run_tbl_row_del = Button(fr_os_run_config, text="Del")
        #bt_os_run_tbl_row_add.pack(side=)
        bt_os_run_tbl_row_add.grid(row=99,column=98)
        bt_os_run_tbl_row_del.grid(row=99, column=99)

        #os_input_add_button_call( row, frame, canvas, scroll_y)

#------------------------------------------------------------------------------------------------------------------------
    def os_module_action_optionmenu_call(self,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
        print("calling os_module_action_optionmenu_call")
        frame_os_module_table = object_studio_module_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0]
        frame_os_moduel_config=(object_studio_module_tab.winfo_children()[4])
        table_frame_os_input_tab = (((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_output_tab = (((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])

        text_code = (object_studio_code_tab.winfo_children()[0]).winfo_children()[1]

        #destory any widgets available after action option menu
        children_widgets_module_config_frame=frame_os_moduel_config.winfo_children()


        os_modules_action_optionmenu_value = os_modules_action_optionmenu_var.get()
        os_modules_handle_optionmenu_value=os_modules_handle_optionmenu_var.get()
        print(os_modules_action_optionmenu_value)
        if os_modules_action_optionmenu_value == 'Create New Action':
            new_action_label = Label(frame_os_moduel_config, text="New Action:", font=("Arial Bold", 9)).place(relx=0.05, rely=0.74,relheight=.18,relwidth=0.2)
            new_action_entry = Entry(frame_os_moduel_config).place(relx=0.25, rely=0.74,  relwidth=0.5)

            # clear text in module tab table
            children_widgets_module_table_frame = frame_os_module_table.winfo_children()
            for each in children_widgets_module_table_frame:
                if each.winfo_class() == 'Entry':
                    each.delete(0, END)

            # clear entry boxes in input and output tabs
            childs_table_frame_os_input_tab = table_frame_os_input_tab.winfo_children()
            childs_table_frame_os_output_tab = table_frame_os_output_tab.winfo_children()

            for each in childs_table_frame_os_input_tab:
                if each.winfo_class() == 'Entry':
                    each.delete(0, END)

            for each in childs_table_frame_os_output_tab:
                if each.winfo_class() == 'Entry':
                    each.delete(0, END)

            # clear text in input labels
            ((object_studio_input_tab.winfo_children()[4]).winfo_children()[1]).configure(text="")
            ((object_studio_input_tab.winfo_children()[4]).winfo_children()[3]).configure(text="")

            # clear text in output labels
            ((object_studio_output_tab.winfo_children()[4]).winfo_children()[1]).configure(text="")
            ((object_studio_output_tab.winfo_children()[4]).winfo_children()[3]).configure(text="")

            # clear text in code
            print(((object_studio_code_tab.winfo_children()[0]).winfo_children()[1]).get('1.0', END))
            text_box_obj = (object_studio_code_tab.winfo_children()[0]).winfo_children()[1]
            text_box_obj.delete('1.0', END)
        elif os_modules_action_optionmenu_value != 'Create New Action' and len(os_modules_action_optionmenu_value)>0 :
            print("retriving values>>>>")
            print(os_modules_handle_optionmenu_value,os_modules_action_optionmenu_value)
            loop_count = 0
            for child_widget in children_widgets_module_config_frame:
                loop_count+=1
                if loop_count>5:
                    child_widget.destroy()

            # destroy all entry boxes in module tab table
            children_widgets_module_table_frame = frame_os_module_table.winfo_children()
            for each in children_widgets_module_table_frame:
                if each.winfo_class() == 'Entry':
                    each.destroy()

            #destroy entry boxes in input and output tabs
            childs_table_frame_os_input_tab = table_frame_os_input_tab.winfo_children()
            childs_table_frame_os_output_tab = table_frame_os_output_tab.winfo_children()
            loop_count=0
            for each in childs_table_frame_os_input_tab:
                print(each)
                #if each.winfo_class() == 'Entry':
                if loop_count>1:
                    print("deleting all entry input")
                    each.destroy()
                loop_count += 1

            loop_count = 0
            for each in childs_table_frame_os_output_tab:
                #if each.winfo_class() == 'Entry':
                if loop_count > 1:
                    each.destroy()
                loop_count+=1

            # clear text in input labels
            ((object_studio_input_tab.winfo_children()[4]).winfo_children()[1]).configure(text=os_modules_handle_optionmenu_value)
            ((object_studio_input_tab.winfo_children()[4]).winfo_children()[3]).configure(text=os_modules_action_optionmenu_value)

            # clear text in output labels
            ((object_studio_output_tab.winfo_children()[4]).winfo_children()[1]).configure(text=os_modules_handle_optionmenu_value)
            ((object_studio_output_tab.winfo_children()[4]).winfo_children()[3]).configure(text=os_modules_action_optionmenu_value)

            # clear text in code
            print(((object_studio_code_tab.winfo_children()[0]).winfo_children()[1]).get('1.0', END))
            text_box_obj = (object_studio_code_tab.winfo_children()[0]).winfo_children()[1]
            text_box_obj.delete('1.0', END)

            #retrive doc for handle and action
            module, input_name, input_value, output_name, output_value, code=self.database.retrive_action_document_from_primary_databse\
                (frame_os_module_table,os_modules_handle_optionmenu_value,os_modules_action_optionmenu_value)
            print(module, input_name, input_value, output_name, output_value, code)

            #fill modules
            if len(module)>0:
                r=2
                for each in module:
                    entry_os_module_name = Entry(frame_os_module_table, width=40)
                    entry_os_module_name.grid(column=0, row=r, sticky=NW)
                    entry_os_module_name.insert(0,each)
                    module_header_label = Entry(frame_os_module_table, width=59).grid(column=1, row=r, sticky=NW, columnspan=10)
                    r+=1

            #fill input
            if len(input_name) > 0:
                r=2
                loop_count=0
                for each in input_name:
                    input_name_entry = Entry(table_frame_os_input_tab, width=40)
                    input_name_entry.grid(column=0, row=r, sticky=NW)
                    input_name_entry.insert(0,each)
                    input_value_entry = Entry(table_frame_os_input_tab, width=57)
                    input_value_entry.grid(column=1, row=r, sticky=NW, columnspan=1)
                    if str(input_value[loop_count]) != "str()": input_value_entry.insert(0, input_value[loop_count])
                    #input_value_entry.insert(0,input_value[loop_count])
                    input_validate_button = Button(table_frame_os_input_tab, height=1)
                    input_validate_button.configure(command=lambda button=input_validate_button, value_entry=input_value_entry,
                                                                   frame=table_frame_os_input_tab: self.os_input_row_validate_button_call(button,
                                                                                                                       value_entry,
                                                                                                                       frame))
                    input_validate_button.grid(column=2, row=r, sticky=NW, columnspan=1)

                    r+=1
                    loop_count+=1

            # fill output
            if len(output_name) > 0:
                r = 2
                loop_count = 0
                for each in output_name:
                    output_name_entry = Entry(table_frame_os_output_tab, width=40)
                    output_name_entry.grid(column=0, row=r, sticky=NW)
                    output_name_entry.insert(0,each)
                    output_value_entry = Entry(table_frame_os_output_tab, width=57)
                    output_value_entry.grid(column=1, row=r, sticky=NW, columnspan=1)
                    if output_value[loop_count]!="str()":output_value_entry.insert(0,output_value[loop_count])
                    output_validate_button = Button(table_frame_os_output_tab, height=1)
                    output_validate_button.configure(
                        command=lambda button=output_validate_button, value_entry=output_value_entry,
                                       frame=table_frame_os_output_tab: self.os_input_row_validate_button_call(button, value_entry, frame))
                    output_validate_button.grid(column=2, row=r, sticky=NW, columnspan=1)

                    r += 1
                    loop_count += 1

            text_code.insert('1.0',code)

        #print("all activity completed in os module action option menu call")

    def load_os_module_action_optionmenu(self,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
        os_modules_handle_optionmenu_value=os_modules_handle_optionmenu_var.get()
        os_modules_action_optionmenu_value = os_modules_action_optionmenu_var.get()

        action_list=self.database.retrive_action_for_handles(os_modules_handle_optionmenu_value)
        print(action_list)

        os_module_action_option_menu=(object_studio_module_tab.winfo_children()[4]).winfo_children()[4]

        print("print option menus")
        print(os_module_action_option_menu)
        print(os_module_action_option_menu['menu'])

        # Reset var and delete all old options
        menu=os_module_action_option_menu['menu']
        os_modules_action_optionmenu_var.set('')
        menu.delete(0, 'end')


        def module_refersh_button_call(action,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
            print("actions: ",action)
            os_modules_action_optionmenu_var.set(action)

            self.os_module_action_optionmenu_call(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)

            os_modules_action_optionmenu_var.trace("w", module_refersh_button_call)


        for actions in action_list:
            menu.add_command(label=actions,command=lambda action=actions :module_refersh_button_call(action,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab))

    def load_os_module_handle_optionmenu(self,optionmenu_variable,object_studio_module_tab,select_object_frame, slected_value_handle, frame,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
        handles_list=self.database.retrive_all_handles()
        print(handles_list)

        os_module_handle_option_menu=(object_studio_module_tab.winfo_children()[4]).winfo_children()[1]

        print("print option menus")
        print(os_module_handle_option_menu)
        print(os_module_handle_option_menu['menu'])

        # Reset var and delete all old options
        menu=os_module_handle_option_menu['menu']
        optionmenu_variable.set('')
        menu.delete(0, 'end')


        def module_refersh_button_call(handles,select_object_frame,slected_value_handle, frame,object_studio_input_tab, object_studio_output_tab,object_studio_code_tab):
            print("handles: ",handles)
            optionmenu_variable.set(handles)
            #self.os_module__handle_refresh_button_call(select_object_frame, frame,object_studio_module_tab,object_studio_input_tab, object_studio_output_tab,object_studio_code_tab)
            # frame, value, table_frame, object_studio_module_tab, object_studio_input_tab, object_studio_output_tab, object_studio_code_tab
            self.os_module__handle_refresh_button_call(select_object_frame,optionmenu_variable ,frame, object_studio_module_tab,object_studio_input_tab, object_studio_output_tab,object_studio_code_tab)
            optionmenu_variable.trace("w", module_refersh_button_call)




        for handles in handles_list:
            menu.add_command(label=handles,command=lambda handles=handles :module_refersh_button_call(handles,select_object_frame, slected_value_handle, frame,object_studio_input_tab, object_studio_output_tab,object_studio_code_tab))


        print((object_studio_module_tab.winfo_children()[4]))
        for each in (object_studio_module_tab.winfo_children()[4]).winfo_children():
            print(each)

#--------------------------------------------------------------------------------------------------------------------------
    def os_code_save_button_call(self,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):

        table_frame_os_input_tab = (((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_output_tab = (((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        childs_table_frame_os_input_tab=table_frame_os_input_tab.winfo_children()
        childs_table_frame_os_output_tab = table_frame_os_output_tab.winfo_children()

        os_modules_handle_optionmenu_value=os_modules_handle_optionmenu_var.get()
        os_modules_action_optionmenu_value=os_modules_action_optionmenu_var.get()

        if os_modules_handle_optionmenu_value=="Create New Handle":

            #validate values in module,input, output an dcode tab
            os_input_validation_error=self.os_input_validate_button_call(table_frame_os_input_tab,tab='Input') #validate input tab
            os_output_validation_error=self.os_input_validate_button_call(table_frame_os_output_tab,tab='Output')#validate output tab

            #if any error identified, teminate the process
            if len(os_input_validation_error) >0 or len(os_output_validation_error)>0:
                messagebox.showerror("Termination", "Create new module activity is terminated due to the validation error " , parent=table_frame_os_input_tab)
                return "Create new module activity is terminated due to the validation error"

            os_module_new_handle_entry_widget = (object_studio_module_tab.winfo_children()[4]).winfo_children()[4]
            os_module_new_action_entry_widget = (object_studio_module_tab.winfo_children()[4]).winfo_children()[6]

            os_module_new_handle_entry_value=os_module_new_handle_entry_widget.get()
            os_module_new_action_entry_value=os_module_new_action_entry_widget.get()
            #retrive and format input
            loop_count=0
            input_list,input_name_list,input_vale_list=list(),list(),list()
            input=''
            for each_input_entry in childs_table_frame_os_input_tab:
                if each_input_entry.winfo_class() == 'Entry':
                    loop_count+=1
                    entry_value=each_input_entry.get()
                    if loop_count%2!=0:input=input + '\n\t' + entry_value
                    if loop_count % 2 == 0:
                        if len(entry_value)>0:input=input + '=' + entry_value
                        if len(entry_value) == 0: input = input + '=' + "str()"

            # retrive and format output
            loop_count = 0
            output = ''
            for each_output_entry in childs_table_frame_os_output_tab:
                if each_output_entry.winfo_class() == 'Entry':
                    loop_count += 1
                    output_entry_value = each_output_entry.get()
                    if loop_count % 2 != 0: output = output + '\n\t' + output_entry_value
                    if loop_count % 2 == 0:
                        if len(output_entry_value) > 0: output = output + '=' + output_entry_value
                        if len(output_entry_value) == 0: output = output + '=' + "str()"

            #retrive and format module
            table_frame_os_module_table=object_studio_module_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children()
            module=""
            loop_count = 0
            for each_module in table_frame_os_module_table:
                if each_module.winfo_class() == 'Entry':
                    loop_count+=1
                    module_value = each_module.get()
                    if loop_count%2!=0:module=module + '\n' + module_value


            #retrive and format code
            text_box_obj = (object_studio_code_tab.winfo_children()[0]).winfo_children()[1]
            code=text_box_obj.get('1.0', END)

            print(os_module_new_handle_entry_value)
            print(os_module_new_action_entry_value)
            print(module)
            print(input)
            print(output)
            print(code)

            self.database.create_new_handler_action_in_primary_databse(
                frame=table_frame_os_input_tab,
                handler=os_module_new_handle_entry_value,
                module=module,
                action=os_module_new_action_entry_value,
                input=input,
                output=output,
                code=code)

            self.database.create_new_handler_action_in_secondary_databse(
                frame=table_frame_os_input_tab,
                handler=os_module_new_handle_entry_value,
                module=module,
                action=os_module_new_action_entry_value,
                input=input,
                output=output,
                code=code)

            #messagebox.showinfo("Success","New Handler Created",parent=table_frame_os_input_tab)

        elif os_modules_handle_optionmenu_value != "Create New Handle" and len(
            os_modules_handle_optionmenu_value) > 0 and os_modules_action_optionmenu_value == "Create New Action":
            print("create new action")
            etr_os_module_config_new_action=(object_studio_module_tab.winfo_children()[4]).winfo_children()[6]
            val_etr_os_module_config_new_action=((object_studio_module_tab.winfo_children()[4]).winfo_children()[6]).get()
            print(os_modules_handle_optionmenu_value,val_etr_os_module_config_new_action)

            #validate values in module,input, output an dcode tab
            os_input_validation_error=self.os_input_validate_button_call(table_frame_os_input_tab,tab='Input') #validate input tab
            os_output_validation_error=self.os_input_validate_button_call(table_frame_os_output_tab,tab='Output')#validate output tab

            #if any error identified, teminate the process
            if len(os_input_validation_error) >0 or len(os_output_validation_error)>0:
                messagebox.showerror("Termination", "Create new Action activity is terminated due to the validation error " , parent=table_frame_os_input_tab)
                return "Create new action activity is terminated due to the validation error"
            loop_count=0
            input_list,input_name_list,input_vale_list=list(),list(),list()
            input=''
            for each_input_entry in childs_table_frame_os_input_tab:
                if each_input_entry.winfo_class() == 'Entry':
                    loop_count+=1
                    entry_value=each_input_entry.get()
                    if loop_count%2!=0:input=input + '\n\t' + entry_value
                    if loop_count % 2 == 0:
                        if len(entry_value)>0:input=input + '=' + entry_value
                        if len(entry_value) == 0: input = input + '=' + "str()"

            # retrive and format output
            loop_count = 0
            output = ''
            for each_output_entry in childs_table_frame_os_output_tab:
                if each_output_entry.winfo_class() == 'Entry':
                    loop_count += 1
                    output_entry_value = each_output_entry.get()
                    if loop_count % 2 != 0: output = output + '\n\t' + output_entry_value
                    if loop_count % 2 == 0:
                        if len(output_entry_value) > 0: output = output + '=' + output_entry_value
                        if len(output_entry_value) == 0: output = output + '=' + "str()"

            #retrive and format module
            table_frame_os_module_table=object_studio_module_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children()
            module=""
            loop_count = 0
            for each_module in table_frame_os_module_table:
                if each_module.winfo_class() == 'Entry':
                    loop_count+=1
                    module_value = each_module.get()
                    if loop_count%2!=0:module=module + '\n' + module_value


            #retrive and format code
            text_box_obj = (object_studio_code_tab.winfo_children()[0]).winfo_children()[1]
            code=text_box_obj.get('1.0', END)

            print(os_modules_handle_optionmenu_value)
            print(val_etr_os_module_config_new_action)
            print(module)
            print(input)
            print(output)
            print(code)

            self.database.create_new_handler_action_in_primary_databse(
                frame=table_frame_os_input_tab,
                handler=os_modules_handle_optionmenu_value,
                module=module,
                action=val_etr_os_module_config_new_action,
                input=input,
                output=output,
                code=code)

            self.database.create_new_handler_action_in_secondary_databse(
                frame=table_frame_os_input_tab,
                handler=os_modules_handle_optionmenu_value,
                module=module,
                action=val_etr_os_module_config_new_action,
                input=input,
                output=output,
                code=code)

            #messagebox.showinfo("Success","New Handler Created",parent=table_frame_os_input_tab)


            for each in (object_studio_module_tab.winfo_children()[4]).winfo_children():
                print(each)

        elif os_modules_handle_optionmenu_value!="Create New Handle"  \
                and len(os_modules_handle_optionmenu_value) > 0 \
                and os_modules_action_optionmenu_value != "Create New Action"\
                and len(os_modules_action_optionmenu_value) != 0:

            #validate values in module,input, output an dcode tab
            os_input_validation_error=self.os_input_validate_button_call(table_frame_os_input_tab,tab='Input') #validate input tab
            os_output_validation_error=self.os_input_validate_button_call(table_frame_os_output_tab,tab='Output')#validate output tab

            #if any error identified, teminate the process
            if len(os_input_validation_error) >0 or len(os_output_validation_error)>0:
                messagebox.showerror("Termination", "Create new module activity is terminated due to the validation error " , parent=table_frame_os_input_tab)
                return "Create new module activity is terminated due to the validation error"

            #retrive and format input
            loop_count=0
            input_list,input_name_list,input_vale_list=list(),list(),list()
            input=''
            for each_input_entry in childs_table_frame_os_input_tab:
                if each_input_entry.winfo_class() == 'Entry':
                    loop_count+=1
                    entry_value=each_input_entry.get()
                    if loop_count%2!=0:input=input + '\n\t' + entry_value
                    if loop_count % 2 == 0:
                        if len(entry_value)>0:input=input + '=' + entry_value
                        if len(entry_value) == 0: input = input + '=' + "str()"

            # retrive and format output
            loop_count = 0
            output = ''
            for each_output_entry in childs_table_frame_os_output_tab:
                if each_output_entry.winfo_class() == 'Entry':
                    loop_count += 1
                    output_entry_value = each_output_entry.get()
                    if loop_count % 2 != 0: output = output + '\n\t' + output_entry_value
                    if loop_count % 2 == 0:
                        if len(output_entry_value) > 0: output = output + '=' + output_entry_value
                        if len(output_entry_value) == 0: output = output + '=' + "str()"

            #retrive and format module
            table_frame_os_module_table=object_studio_module_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children()
            module=""
            loop_count = 0
            for each_module in table_frame_os_module_table:
                if each_module.winfo_class() == 'Entry':
                    loop_count+=1
                    module_value = each_module.get()
                    if loop_count%2!=0:module=module + '\n' + module_value


            #retrive and format code
            text_box_obj = (object_studio_code_tab.winfo_children()[0]).winfo_children()[1]
            code=text_box_obj.get('1.0', END)

            print(os_modules_handle_optionmenu_value)
            print(os_modules_action_optionmenu_value)
            print(module)
            print(input)
            print(output)
            print(code)

            self.database.update_action_doc_in_primary_databse(
                frame=table_frame_os_input_tab,
                handler=os_modules_handle_optionmenu_value,
                module=module,
                action=os_modules_action_optionmenu_value,
                input=input,
                output=output,
                code=code)

            '''self.database.create_new_handler_action_in_secondary_databse(
                frame=table_frame_os_input_tab,
                handler=os_modules_handle_optionmenu_value,
                module=module,
                action=os_modules_action_optionmenu_value,
                input=input,
                output=output,
                code=code)'''

            #messagebox.showinfo("Success","New Handler Created",parent=table_frame_os_input_tab)
    def os_code_run_button_call(self,text_obj,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab):
        code = text_obj.get('1.0', END)

        table_frame_os_module_tab = (((object_studio_module_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_input_tab = (((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_output_tab = (((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])


        #read and format modules into a list
        childs_table_frame_os_module_tab=table_frame_os_module_tab.winfo_children()
        loop_count=0
        module_list=list()
        for each_widget in childs_table_frame_os_module_tab:
            if each_widget.winfo_class()=='Entry' :
                loop_count += 1
                if len(each_widget.get())>0 and  loop_count%2!=0:
                    module_list.append('import ' + each_widget.get() + '\n')

        #read and format input name and value into a list
        input_name_list,input_value_list,input_list=list(),list(),list()
        loop_count =0
        childs_table_frame_os_input_tab = table_frame_os_input_tab.winfo_children()
        for each_widget in childs_table_frame_os_input_tab:
            if each_widget.winfo_class()=='Entry':
                loop_count += 1
                if loop_count%2!=0:input_name_list.append('\t' + each_widget.get() + '=')
                if loop_count % 2 == 0 and len(each_widget.get())>0:input_value_list.append(each_widget.get() + '\n')
                if loop_count % 2 == 0 and len(each_widget.get())==0:input_value_list.append("str()\n")
        for each_item in range(len(input_name_list)):input_list.append(input_name_list[each_item]+input_value_list[each_item])

        #read and format output name and value into a list
        output_name_list,output_value_list,output_list=list(),list(),list()
        loop_count =0
        childs_table_frame_os_output_tab = table_frame_os_output_tab.winfo_children()
        for each_widget in childs_table_frame_os_output_tab:
            if each_widget.winfo_class()=='Entry':
                loop_count += 1
                if loop_count%2!=0:output_name_list.append('\t' +each_widget.get() + '=')
                if loop_count % 2 == 0 and len(each_widget.get())>0:output_value_list.append(each_widget.get() + '\n')
                if loop_count % 2 == 0 and len(each_widget.get())==0:output_value_list.append("str()\n")
        for each_item in range(len(output_name_list)):output_list.append(output_name_list[each_item]+output_value_list[each_item])


        #derive finction and execute
        outcome_dict={}
        output=((','.join(output_name_list)).replace("=","")).strip()
        print(output)
        function = ''.join(module_list) + "def action():\n"  +  ''.join(input_list) +  ''.join(output_list) + "\n" + code + "\n\t" + "return " + output +  "\n" + "global outcome" + "\n" + "outcome=action()" + "\n" + "print(outcome)"
        print(function)
        try:
            exec(function)
            #output_value_list=outcome.split(",")
            output_key_list=output.split(",")



            if "tuple" in str(outcome):
                loop_count = 0
                for each in output_key_list:
                    outcome_dict[each.strip()] = outcome[loop_count]
                    loop_count += 1
            else:
                for each in output_key_list:outcome_dict[each.strip()] = outcome


            print(outcome_dict)
            messagebox.showinfo("Output",outcome_dict,parent=table_frame_os_module_tab)
        except Exception as e:
            error="Error in run as: " + str(e)
            messagebox.showinfo("Error",  error , parent=table_frame_os_module_tab)

    def os_code_debug_button_call(self,text_obj,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab):
        print(text_obj.get('1.0',END))
        text=text_obj.get('1.0',END)
        print(text)

        #---vaidate all the values
        table_frame_os_module_tab = (((object_studio_module_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_input_tab = (((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_output_tab = (((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])

        self.os_module_validate_button_call(table_frame_os_module_tab)
        self.os_input_validate_button_call(table_frame_os_input_tab)
        self.os_input_validate_button_call(table_frame_os_output_tab)

    def os_code_tab(self, object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
        #code_textbox=Text(object_studio_code_tab,bd=4)
        #code_textbox.place(relx=.05,rely=.05,relheight=.9,relwidth=.9)
        txt = scrolledtext.ScrolledText(object_studio_code_tab, undo=True)
        txt['font'] = ('consolas', '12')
        #txt.pack(expand=True, fill='both')
        txt.place(relx=.025,rely=.05,relheight=.9,relwidth=.86)
        debug_button=Button(object_studio_code_tab,text="Debug",width=7,command=lambda :self.os_code_debug_button_call(txt,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab))
        debug_button.place(relx=.89,rely=.05)
        run_button = Button(object_studio_code_tab, text="Run", width=7,
                              command=lambda: self.os_code_run_button_call(txt, object_studio_module_tab,
                                                                             object_studio_input_tab,
                                                                             object_studio_output_tab))
        run_button.place(relx=.89, rely=.095)
        save_button = Button(object_studio_code_tab, text="Save", width=7,
                              command=lambda: self.os_code_save_button_call(object_studio_module_tab,
                                                                             object_studio_input_tab,
                                                                             object_studio_output_tab,object_studio_code_tab))
        save_button.place(relx=.89, rely=0.14)
#-----------------------------------------------------------------------------------------------------------------------

    def os_output_tab(self, object_studio_output_tab):
        parent = Frame(object_studio_output_tab)
        parent.place(relx=0.2, rely=0.26, relheight=.4, relwidth=0.5)

        canvas = Canvas(parent, bd=0, highlightthickness=0)
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview)

        frame = Frame(canvas, bd=0)
        height = 0
        global r
        r = 1
        input_name_entry_obejct_list, input_value_entry_obejct_list, input_validate_button_obejct_list = list(), list(), list()

        for i in range(3):
            if r == 1:
                outputname_header_label = Label(frame, text="Output Name", font=("Arial Bold", 10), bg='gray87',
                                            width=30,
                                            relief=GROOVE).grid(column=0, row=r)
                outputvalue_header_label = Label(frame, text="Output Value", font=("Arial Bold", 10), bg='gray87',
                                            width=45,
                                            relief=GROOVE).grid(column=1, row=r, sticky=E, columnspan=10)
                outputvalueValidate_header_label = Label(frame, text="", font=("Arial Bold", 10), bg='gray87',
                                            width=2,
                                            relief=GROOVE).grid(column=2, row=r, sticky=E, columnspan=10)
            else:
                name_entry = 'name_entry' + str(i)
                output_name_entry = Entry(frame, width=40)
                output_name_entry.grid(column=0, row=r, sticky=NW)
                output_value_entry = Entry(frame, width=57)
                output_value_entry.grid(column=1, row=r, sticky=NW, columnspan=1)
                output_validate_button = Button(frame, height=1)
                output_validate_button.configure(
                    command=lambda button=output_validate_button, value_entry=output_value_entry,
                                   frame=frame: self.os_input_row_validate_button_call(button, value_entry, frame))
                output_validate_button.grid(column=2, row=r, sticky=NW, columnspan=1)


            r += 1
        print(input_name_entry_obejct_list, input_value_entry_obejct_list, input_validate_button_obejct_list)

        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        add_button = Button(object_studio_output_tab, text='Add',
                            command=lambda: self.os_input_add_button_call(r, frame, canvas, scroll_y)).place(
            relx=.703, rely=.27, relheight=.03, relwidth=.05)
        remove_button = Button(object_studio_output_tab, text='Remove',
                               command=lambda: self.os_input_remove_button_call(frame)).place(relx=.703, rely=.31,
                                                                                              relheight=.03,
                                                                                              relwidth=.05)
        validate_button = Button(object_studio_output_tab, text='Validate',
                                 command=lambda: self.os_input_validate_button_call(frame)).place(relx=.703, rely=.35,
                                                                                                  relheight=.03,
                                                                                                  relwidth=.05)

        select_object_frame = Frame(object_studio_output_tab)
        select_object_frame.place(relx=0.2, rely=0.1, relheight=.15, relwidth=0.5)

        sleelct_handle_label = Label(select_object_frame, text="Handle:",
                                     font=("Arial Bold", 9)).place(relx=0.05, rely=0.32, relheight=.18,
                                                                   relwidth=0.2)
        sleelct_handle_label = Label(select_object_frame, text="", bg="azure",
                                     font=("Arial Bold", 9)).place(relx=0.25, rely=0.32, relheight=.18,
                                                                   relwidth=0.5)

        new_handle_label = Label(select_object_frame, text="Action:", font=("Arial Bold", 9)).place(relx=0.05, rely=0.6,
                                                                                                    relheight=.18,
                                                                                                    relwidth=0.2)
        new_handle_label = Label(select_object_frame, text="", bg="azure", font=("Arial Bold", 9)).place(relx=0.25,
                                                                                                         rely=0.6,
                                                                                                         relheight=.18,
                                                                                                         relwidth=0.5)

#------------------------------------------------------------------------------------------------------------------------

    def os_input_validate_button_call(self,frame,tab):
        text_list = list()
        input_name_list = list()
        input_value_list = list()
        validation_error_list = list()
        loop_count = 0
        children_widgets = frame.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                loop_count += 1
                text = child_widget.get()
                if loop_count % 2 != 0 and len(text) >= 0: input_name_list.append(text)
                if loop_count % 2 == 0 and len(text) >= 0: input_value_list.append(text)
                if len(text) > 0: text_list.append(text)

        for each in input_value_list:
            try:
                text=str(each)
                if len(each)>0:
                    value = str(eval(text))
                    code="value = str(eval(text))"
                    print(value)
                    exec(code)
            except Exception as e:
                error = "Error: " + str(e)
                validation_error_list.append(error)


        loop_count=0
        for each in input_name_list:
            loop_count+=1
            if len(each)==0:
                validation_error_list.append(tab + ' name Missing in line: ' + str(loop_count) )
                #messagebox.showinfo('Error', message="Input/Output Name Missing", parent=frame)
                #break
            if input_name_list.count(each) > 1:
                validation_error_list.append(tab + " name Duplicated in line "+ str(loop_count))
                #messagebox.showinfo('Error', message="Input/Output Name Duplicated: "+each, parent=frame)
                #break
        if len(validation_error_list)>0:
            messagebox.showerror('Error', message=tab +" tab: "+ ", ".join(validation_error_list), parent=frame)
        else:
            messagebox.showinfo('Success', message=tab +" tab: "+"Successfully validated", parent=frame)
        return validation_error_list
    def os_input_row_validate_button_call(self,button,input_value_entry,frame):
        print(button)
        print(input_value_entry)
        #print(input_value_entry.get())
        #str="print(input_value_entry.get())"
        try:
            text=input_value_entry.get()
            if len(text)>0:
                print("value taken")
                value=str(eval(input_value_entry.get()))
            if len(text)==0:value='None'
            string="messagebox.showinfo('Input Value',message=value,parent=frame)"
            exec(string)
        except Exception as e:
            error="Error: " + str(e)
            string = "messagebox.showinfo('Input Value',message=error,parent=frame)"
            exec(string)



        #print(value)
    def os_input_add_button_call(self,row,frame,canvas,scroll_y):
        self.num_rows += 1
        input_name_entry = Entry(frame, width=40).grid(column=0, row=self.num_rows, sticky=NW)
        input_value_entry = Entry(frame, width=57)
        input_value_entry.grid(column=1, row=self.num_rows, sticky=NW, columnspan=1)
        input_validate_button = Button(frame)
        input_validate_button.configure(command=lambda button=input_validate_button,
                                                       value_entry=input_value_entry,frame=frame: self.os_input_row_validate_button_call(button,value_entry,frame))
        input_validate_button.grid(column=2, row=self.num_rows, sticky=NW, columnspan=1)

        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')
        print("Total grids after clicking add button - module tab -frame: ",len(frame.grid_slaves()))

    def os_input_remove_button_call(self,frame):
        entry_widgets_list,button_widget_list=list(),list()
        children_widgets = frame.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':entry_widgets_list.append(child_widget)
            if child_widget.winfo_class() == 'Button': button_widget_list.append(child_widget)
            print(child_widget.winfo_class())


        if len(entry_widgets_list)>0:
            entry_widgets_list[len(entry_widgets_list)-1].destroy()
            entry_widgets_list[len(entry_widgets_list) - 2].destroy()
            button_widget_list[len(button_widget_list) - 1].destroy()

    def os_input_tab(self,object_studio_input_tab):
        parent = Frame(object_studio_input_tab)
        parent.place(relx=0.2, rely=0.26, relheight=.4, relwidth=0.5)

        canvas = Canvas(parent, bd=0, highlightthickness=0)
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview)

        frame = Frame(canvas, bd=0)
        height = 0
        global r
        r = 1
        input_name_entry_obejct_list,input_value_entry_obejct_list,input_validate_button_obejct_list=list(),list(),list()

        for i in range(3):
            if r == 1:
                module_header_label = Label(frame, text="Input Name", font=("Arial Bold", 10), bg='gray87',
                                            width=30,
                                            relief=GROOVE).grid(column=0, row=r)
                module_header_label = Label(frame, text="Input Value", font=("Arial Bold", 10), bg='gray87',
                                            width=45,
                                            relief=GROOVE).grid(column=1, row=r, sticky=E, columnspan=10)
                module_header_label = Label(frame, text="", font=("Arial Bold", 10), bg='gray87',
                                            width=2,
                                            relief=GROOVE).grid(column=2, row=r, sticky=E, columnspan=10)
            else:
                name_entry='name_entry'+str(i)
                input_name_entry = Entry(frame, width=40)
                input_name_entry.grid(column=0, row=r, sticky=NW)
                input_value_entry = Entry(frame,width=57)
                input_value_entry.grid(column=1, row=r, sticky=NW, columnspan=1)
                input_validate_button = Button(frame,height=1)
                input_validate_button.configure(command=lambda button=input_validate_button,value_entry=input_value_entry,frame=frame: self.os_input_row_validate_button_call(button,value_entry,frame))
                input_validate_button.grid(column=2, row=r, sticky=NW, columnspan=1)



            r += 1
        print(input_name_entry_obejct_list, input_value_entry_obejct_list, input_validate_button_obejct_list)

        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        add_button = Button(object_studio_input_tab, text='Add',
                            command=lambda: self.os_input_add_button_call(r, frame, canvas, scroll_y)).place(
            relx=.703, rely=.27, relheight=.03, relwidth=.05)
        remove_button = Button(object_studio_input_tab, text='Remove',
                               command=lambda: self.os_input_remove_button_call(frame)).place(relx=.703, rely=.31,
                                                                                               relheight=.03,
                                                                                               relwidth=.05)
        validate_button = Button(object_studio_input_tab, text='Validate',
                                 command=lambda: self.os_input_validate_button_call(frame,'Input')).place(relx=.703, rely=.35,
                                                                                            relheight=.03,
                                                                                            relwidth=.05)

        select_object_frame = Frame(object_studio_input_tab)
        select_object_frame.place(relx=0.2, rely=0.1, relheight=.15, relwidth=0.5)

        sleelct_handle_label = Label(select_object_frame, text="Handle:",
                                     font=("Arial Bold", 9)).place(relx=0.05, rely=0.32, relheight=.18,
                                                                   relwidth=0.2)
        sleelct_handle_label = Label(select_object_frame, text="", bg="azure",
                                     font=("Arial Bold", 9)).place(relx=0.25, rely=0.32, relheight=.18,
                                                                   relwidth=0.5)


        new_handle_label = Label(select_object_frame, text="Action:", font=("Arial Bold", 9)).place(relx=0.05,rely=0.6,relheight=.18,relwidth=0.2)
        new_handle_label = Label(select_object_frame, text="", bg="azure", font=("Arial Bold", 9)).place(relx=0.25, rely=0.6,relheight=.18,relwidth=0.5)

#---------------------------------------------------------------------------------------------------------------------------
    def os_module__action_refresh_button_call(self,frame,var):
        print("refresh buttopn called with optionmenu")
        option_value = var.get()
        print(option_value)
        if option_value == 'Create New Action':
            new_action_label = Label(frame, text="New Action:", font=("Arial Bold", 9)).place(relx=0.05, rely=0.74,
                                                                                              relheight=.18,
                                                                                              relwidth=0.2)
            new_action_entry = Entry(frame).place(relx=0.25, rely=0.74,  relwidth=0.5)
        else:
            children_widgets = frame.winfo_children()
            label_list = list()
            loop_count = 0
            for child_widget in children_widgets:
                loop_count += 1
                if loop_count > 6:
                    child_widget.destroy()

    def os_module__handle_refresh_button_call(self,frame,value,table_frame,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
        children_widgets = frame.winfo_children()
        label_list=list()
        loop_count=0
        for child_widget in children_widgets:
            loop_count+=1
            if loop_count>3:
                child_widget.destroy()

        option_value=value.get()
        if option_value=='Create New Handle':
            new_handle_label = Label(frame, text="New Handle:",font=("Arial Bold", 9)).place(relx=0.05, rely=0.48, relheight=.18,relwidth=0.2)
            new_handle_entry = Entry(frame).place(relx=0.25,rely=0.45,relheight=.20,relwidth=0.5)
            new_action_label = Label(frame, text="New Action:", font=("Arial Bold", 9)).place(relx=0.05, rely=0.67,relheight=.18,relwidth=0.2)
            new_handle_entry = Entry(frame).place(relx=0.25, rely=0.67, relheight=.20, relwidth=0.5)
        else:
            action_label = Label(frame, text="Action:", font=("Arial Bold", 9)).place(relx=0.05, rely=0.5,relheight=.18,relwidth=0.2)
            action_value_var = StringVar(frame)
            action_choices = ["Create New Action", "Dummy - Not in Use"]
            action_menu = OptionMenu(frame, action_value_var, *action_choices).place(relx=0.25, rely=0.45,relheight=.24,relwidth=0.5)
            #action_value_var.trace("w",)
            self.get_variables(value,action_value_var,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)
            #action_refersh_button = Button(frame, text="Refresh", bd=3,command=lambda: self.os_module__action_refresh_button_call(frame,action_value_var,frame)).place(relx=0.80, rely=0.49,relheight=.16, relwidth=0.09)


        print("printing widgets class after all refresh")
        #clear text in module tab table
        child_widgets_table_frame=table_frame.winfo_children()
        for each in child_widgets_table_frame:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        # clear entry boxes in input and output tabs
        table_frame_os_input_tab = (((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_output_tab = (((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        childs_table_frame_os_input_tab=table_frame_os_input_tab.winfo_children()
        childs_table_frame_os_output_tab = table_frame_os_output_tab.winfo_children()

        for each in childs_table_frame_os_input_tab:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        for each in childs_table_frame_os_output_tab:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        #clear text in input labels
        ((object_studio_input_tab.winfo_children()[4]).winfo_children()[1]).configure(text="")
        ((object_studio_input_tab.winfo_children()[4]).winfo_children()[3]).configure(text="")

        # clear text in output labels
        ((object_studio_output_tab.winfo_children()[4]).winfo_children()[1]).configure(text="")
        ((object_studio_output_tab.winfo_children()[4]).winfo_children()[3]).configure(text="")

        #clear text in code
        print(((object_studio_code_tab.winfo_children()[0]).winfo_children()[1]).get('1.0', END))
        text_box_obj=(object_studio_code_tab.winfo_children()[0]).winfo_children()[1]
        text_box_obj.delete('1.0', END)

        self.load_os_module_action_optionmenu(object_studio_module_tab, object_studio_input_tab,object_studio_output_tab, object_studio_code_tab)



    def os_module_add_button_call(self,row,frame,canvas,scroll_y):
        self.num_rows += 1
        module_header_label = Entry(frame, width=40).grid(column=0, row=self.num_rows, sticky=NW)
        module_header_label = Entry(frame, width=59).grid(column=1, row=self.num_rows, sticky=NW, columnspan=10)

        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')
        print("Total grids after clicking add button - module tab -frame: ",len(frame.grid_slaves()))

    def os_module_remove_button_call(self,frame):
        entry_widgets_list=list()
        children_widgets = frame.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                entry_widgets_list.append(child_widget)
        if len(entry_widgets_list)>1:
            entry_widgets_list[len(entry_widgets_list)-1].destroy()
            entry_widgets_list[len(entry_widgets_list) - 2].destroy()


    def os_module_validate_button_call(self,frame):
        text_list=list()
        modue_name_list=list()
        module_path_list=list()
        validation_error_list=list()
        loop_count=0
        children_widgets = frame.winfo_children()
        for child_widget in children_widgets:
            loop_count+=1
            if child_widget.winfo_class() == 'Entry':
                text=child_widget.get()
                if loop_count%2!=0 and len(text)>0:modue_name_list.append(text)
                if loop_count % 2 == 0 and len(text)>0: module_path_list.append(text)
                if len(text)>0:text_list.append(text)

        if len(module_path_list)>len(modue_name_list):validation_error_list.append("Module name missing for a given module path")
        for each in module_path_list:
            if os.path.exists(each)==False:validation_error_list.append("Module path not exist: " + each )
        if len(validation_error_list)>0:messagebox.showerror("Error",validation_error_list,parent=frame)
        for each in modue_name_list:
            script="try:\n\timport " + each +"\nexcept:\n\tmessagebox.showerror('Error'," + "'"+ "Module not installed: " + each + "'," + "parent=frame)  "
            exec(script)

        print(text_list)


    def os_module_tab(self,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):

        parent = Frame(object_studio_module_tab)
        parent.place(relx=0.2, rely=0.31, relheight=.4, relwidth=0.5)

        canvas = Canvas(parent,bd=0,highlightthickness=0)
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview)

        frame = Frame(canvas,bd=0)
        height=0
        global r
        r=1
        for i in range(3):
            if r==1:
                module_header_label = Label(frame, text="Module Name", font=("Arial Bold", 10), bg='gray87', width=30,
                                            relief=GROOVE).grid(column=0,row=r)
                module_header_label = Label(frame, text="Module Path", font=("Arial Bold", 10), bg='gray87',width=50,
                                            relief=GROOVE).grid(column=2, row=r,sticky=E,columnspan=10)
            else:
                module_header_label = Entry(frame, width=40).grid(column=0,row=r,sticky=NW)
                module_header_label = Entry(frame,width=59 ).grid(column=1, row=r,sticky=NW,columnspan=10)
            r+=1


        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        add_button = Button(object_studio_module_tab, text='Add',command=lambda:self.os_module_add_button_call(r,frame,canvas,scroll_y)).place(relx=.703, rely=.32, relheight=.03, relwidth=.05)
        remove_button = Button(object_studio_module_tab, text='Remove',command=lambda:self.os_module_remove_button_call(frame)).place(relx=.703, rely=.36, relheight=.03,relwidth=.05)
        validate_button = Button(object_studio_module_tab, text='Validate',command=lambda:self.os_module_validate_button_call(frame)).place(relx=.703, rely=.40, relheight=.03,relwidth=.05)

        select_object_frame = Frame(object_studio_module_tab)
        select_object_frame.place(relx=0.2, rely=0.1, relheight=.20, relwidth=0.5)

        handle_label = Label(select_object_frame, text="Handle:",
                                     font=("Arial Bold", 9)).place(relx=0.05, rely=0.2, relheight=.18, relwidth=0.2)
        slected_value_handle = StringVar(select_object_frame)
        choices = ["Create New Handle", "Dummy - Not in Use"]
        handle_option_menus = OptionMenu(select_object_frame, slected_value_handle, *choices)
        handle_option_menus.place(relx=0.25, rely=0.15,relwidth=0.5)

        #test_label=Label(parent,text='')
        #test_label.pack(side=LEFT)

        # load optionmenu
        self.load_os_module_handle_optionmenu(slected_value_handle,object_studio_module_tab,select_object_frame, slected_value_handle, frame,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)

        def module_refersh_button_call(*args):self.os_module__handle_refresh_button_call(select_object_frame, slected_value_handle, frame,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)
        slected_value_handle.trace("w",module_refersh_button_call)

        #handle_refersh_button = Button(select_object_frame, text="Refresh", bd=3,command=lambda: self.os_module__handle_refresh_button_call(select_object_frame,slected_value_handle,frame)).place(relx=0.80, rely=0.20,relheight=.15, relwidth=0.09)
        action_label = Label(select_object_frame, text="Action:", font=("Arial Bold", 9)).place(relx=0.05,rely=0.5,relheight=.18,relwidth=0.2)
        action_value_var = StringVar(select_object_frame)
        action_choices = ["Create New Action", "Dummy - Not in Use"]
        action_menu = OptionMenu(select_object_frame, action_value_var, *action_choices).place(relx=0.25, rely=0.45,relwidth=0.5)




        #load optionmenu
        #self.load_os_module_handle_optionmenu(object_studio_module_tab)

        self.get_variables(slected_value_handle,action_value_var,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)

    def object_studio(self):
        # Make 1st tab
        object_studio_module_tab = Frame(self.object_studio_notebook,bd=0,bg="snow")
        object_studio_input_tab = Frame(self.object_studio_notebook, bd=0, bg="snow")
        object_studio_output_tab = Frame(self.object_studio_notebook, bd=0, bg="snow")
        object_studio_code_tab = Frame(self.object_studio_notebook, bd=0, bg="snow")
        object_studio_run_tab = Frame(self.object_studio_notebook, bd=0, bg="snow")
        # Add the tabs
        self.object_studio_notebook.add(object_studio_module_tab, text="Module")
        self.object_studio_notebook.add(object_studio_input_tab, text="Input")
        self.object_studio_notebook.add(object_studio_output_tab, text="Output")
        self.object_studio_notebook.add(object_studio_code_tab, text="Code")
        self.object_studio_notebook.add(object_studio_run_tab, text="Run")

        self.os_module_tab(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)
        self.os_input_tab(object_studio_input_tab)
        self.os_output_tab(object_studio_output_tab)
        self.os_code_tab(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)
        self.os_run_tab(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab,object_studio_run_tab)


class Studio:

    def __init__(self, root, db):
        self.root = root
        self.num_rows = 4
        self.database = db
        self.studio_window = ''

    def mainFrame(self):
        self.root.title('Studio')
        self.root.geometry("200x200")
        self.root.resizable(0, 0)
        button1 = Button(root, text="open new window", command=self.Studio_window)
        button1.place(x=50, y=25, width=100, height=25)

    def Studio_window(self):  # new window definition
        self.studio_window = Toplevel(self.root)
        self.studio_window.title('New Window')
        #newwin.geometry("200x100")
        #newwin.resizable(0, 0)
        self.studio_window.state('zoomed')

        style = ttk.Style(self.studio_window)
        style.configure('lefttab.TNotebook', tabposition='wn')
        nb = ttk.Notebook(self.studio_window, style='lefttab.TNotebook')
        nb.place(x=0,y=0,relheight=1,relwidth =1)

        # Make 1st tab
        object_studio_frame_tab = Frame(nb)
        # Add the tab
        nb.add(object_studio_frame_tab, text="Object Studio")

        # Make 2nd tab
        process_studio_frame_tab = Frame(nb)
        # Add 2nd tab
        nb.add(process_studio_frame_tab, text="Process Studio")

        nb.select(object_studio_frame_tab)

        object_studio_notebook = ttk.Notebook(object_studio_frame_tab)
        object_studio_notebook.place(relx=0.01,rely=0.01,relheight=0.98,relwidth =0.98)

        process_studio_notebook = ttk.Notebook(process_studio_frame_tab)
        process_studio_notebook.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

        os=ObjectStudio(root,db,object_studio_notebook)
        os.object_studio()

        ps=ProcessStudio.ProcessStudio(process_studio_notebook,self.database)
        ps.process_studio()

        #return object_studio_notebook,process_studio_notebook

        #self.object_studio(object_studio_notebook)

root = Tk()
db=Database.database(r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json",r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomSecondaryDatabase.json")
app = Studio(root,db)

app.mainFrame()
root.mainloop()
