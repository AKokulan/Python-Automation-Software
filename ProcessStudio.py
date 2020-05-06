from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
import os,shutil
from datetime import datetime
import tkinter

import Database
import GuiGloballVariable

class ProcessStudio:
    def __init__(self,process_studio_notebook,database):
        self.process_studio_notebook=process_studio_notebook
        self.db=database
        self.root=100


    def process_studio(self):
        # Make 1st tab
        process_studio_process_tab = Frame(self.process_studio_notebook,bd=0,bg="snow")
        object_studio_input_tab = Frame(self.process_studio_notebook, bd=0, bg="snow")
        process_studio_output_tab = Frame(self.process_studio_notebook, bd=0, bg="snow")
        object_studio_code_tab = Frame(self.process_studio_notebook, bd=0, bg="snow")
        object_studio_run_tab = Frame(self.process_studio_notebook, bd=0, bg="snow")
        # Add the tabs
        self.process_studio_notebook.add(process_studio_process_tab, text="Process")
        #self.process_studio_notebook.add(object_studio_input_tab, text="Input")
        self.process_studio_notebook.add(process_studio_output_tab, text="Output")
        #self.process_studio_notebook.add(object_studio_code_tab, text="Code")
        #self.process_studio_notebook.add(object_studio_run_tab, text="Run")


        process_tab=ProcessStudioProcessTab(self.process_studio_notebook,self.db,process_studio_output_tab)
        process_tab.process_tab(process_studio_process_tab)

        output_tab=ProcessStudioOutputTab(self.process_studio_notebook,self.db)
        output_tab.output_tab(process_studio_output_tab)

class ProcessStudioProcessTab:

    def __init__(self,process_studio_notebook,database,process_studio_output_tab):
        self.process_studio_notebook=process_studio_notebook
        self.db=database
        #self.root=100
        self.check_button_dict = {}
        self.var_table=[]
        self.process_studio_output_tab=process_studio_output_tab
        #self.process_tab=ProcessStudioOutputTab(process_studio_notebook,database)


    def process_tab(self,process_studio_process_tab):
        fr_config=Frame(process_studio_process_tab)
        fr_config.place(relx=0.015,rely=0.015,relheight=0.2,relwidth=0.97)

        fr_table=Frame(process_studio_process_tab)
        fr_table.place(relx=0.015, rely=0.219, relheight=0.75, relwidth=0.97)

        cn_on_fr_table=Canvas(fr_table)
        cn_on_fr_table.pack(side=BOTTOM,fill=BOTH,expand=True)

        fr_header_on_fr_table=Canvas(fr_table,height=1)
        fr_header_on_fr_table.pack(side=TOP,fill=X)

        Label(fr_header_on_fr_table, text='', width=4, relief=GROOVE,bg='gray87').grid(row=1, column=1)
        Label(fr_header_on_fr_table,text='Handler',width=33,relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1,column=2)
        Label(fr_header_on_fr_table, text='Action', width=33, relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1, column=3)
        Label(fr_header_on_fr_table, text='Input', width=22, relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1, column=4)
        Label(fr_header_on_fr_table, text='Output', width=22, relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1, column=5)
        Label(fr_header_on_fr_table, text='Exception Handle', width=15, relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1, column=6)

        frame=Frame(cn_on_fr_table)
        y_socrollbar=Scrollbar(cn_on_fr_table)
        y_socrollbar.pack(side=RIGHT,fill=Y)

        cn_on_fr_table.create_window(0, 0, anchor='nw', window=frame)
        cn_on_fr_table.update_idletasks()

        cn_on_fr_table.config(yscrollcommand=y_socrollbar.set)
        y_socrollbar.config(command=cn_on_fr_table.yview)

        self.process_tab_config_frame_gui(process_studio_process_tab,'',"","")

    def process_tab_config_frame_gui(self,ps_process_tab,cl_val,pr_val,pg_val):
        print('printing process childs')

        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        for each in fr_config.winfo_children():print(each)
        for each in fr_table.winfo_children(): print(each)


        children_windows = fr_config.winfo_children()

        loop_count=0
        for each in children_windows:
            loop_count+=1
            if loop_count>=1:
                each.destroy()
        lb_cluster = Label(fr_config, text="Cluster:", font=("Arial Bold", 10))
        lb_cluster.place(relx=0.018, rely=0.13, relwidth=0.07)

        var_cluster = StringVar()
        var_cluster.set(cl_val)
        choices_cluster = self.db.retrive_clusters()
        #var_cluster.set(cluster_val)
        om_cluster = OptionMenu(fr_config, var_cluster, *choices_cluster)
        om_cluster.place(relx=0.1, rely=0.085, relwidth=0.2)

        def create_new_cluster_om_call(*args): self.create_new_cluster_om_call(var_cluster, ps_process_tab)
        var_cluster.trace("w", create_new_cluster_om_call)

        lb_process = Label(fr_config, text="Process:", font=("Arial Bold", 10))
        lb_process.place(relx=0.33, rely=0.13, relwidth=0.07)

        var_process = StringVar()
        var_process.set(pr_val)
        choices_process =self.db.retrive_process(var_cluster.get())
        om_cluster = OptionMenu(fr_config, var_process, *choices_process)
        om_cluster.place(relx=0.43, rely=0.085, relwidth=0.2)

        def create_new_process_om_call(*args): self.create_new_process_om_call(var_process,var_cluster, ps_process_tab)
        var_process.trace("w", create_new_process_om_call)

        lb_page = Label(fr_config, text="Page:", font=("Arial Bold", 10))
        lb_page.place(relx=0.66, rely=0.13, relwidth=0.07)

        var_page = StringVar()
        var_page.set(pg_val)
        choices_page = self.db.retrive_process_page(var_process.get())
        om_page = OptionMenu(fr_config, var_page, *choices_page)
        om_page.place(relx=0.76, rely=0.085, relwidth=0.2)

        def create_new_page_om_call(*args): self.create_new_page_om_call(var_page,var_process,var_cluster, ps_process_tab)
        var_page.trace("w", create_new_page_om_call)

        bt_step = Button(fr_config, text="Step", font=("Arial Bold", 10))
        bt_step.place(relx=0.0, rely=0.8, relwidth=0.04)

        bt_run = Button(fr_config, text="Run", font=("Arial Bold", 10))
        bt_run.place(relx=0.04, rely=0.8, relwidth=0.04)


        bt_add_row = Button(fr_config, text="Add",command=lambda fr=ps_process_tab : self.add_row_button_call(fr), font=("Arial Bold", 10))
        bt_add_row.place(relx=0.92, rely=0.8, relwidth=0.04)

        bt_del_row = Button(fr_config, text="Del", font=("Arial Bold", 10),command=lambda fr=ps_process_tab : self.del_row_button_call(fr))
        bt_del_row.place(relx=0.96, rely=0.8, relwidth=0.04)

    def create_new_cluster_om_call(self,var,ps_process_tab):
        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]

        var_value=var.get()
        children_windows=fr_config.winfo_children()

        if var_value=="Create New Cluster":
            loop_count=0
            for each in children_windows:
                loop_count+=1
                if loop_count>2:
                    each.destroy()

            lb_new_cluster=Label(fr_config,text="New Cluster",bg='gray')
            lb_new_cluster.place(relx=0.018,rely=0.35,relwidth=0.07)

            var_cluster=StringVar()
            choices_cluster=['Create New Cluster']
            et_new_cluster=Entry(fr_config)
            et_new_cluster.place(relx=0.1, rely=0.37,relwidth=0.2)

            bt_new_cluster_save = Button(fr_config, text="Save", bg='gray',command=lambda ent=et_new_cluster,fr=fr_config :self.cluster_save_button_call(ent,fr))
            bt_new_cluster_save.place(relx=0.1, rely=0.58, relwidth=0.07)

            bt_new_cluster_cancel = Button(fr_config, text="Cancel", bg='gray',command=lambda fr=ps_process_tab,val=var_value :self.process_tab_config_frame_gui(fr,val,'',''))
            bt_new_cluster_cancel.place(relx=0.18, rely=0.58, relwidth=0.07)
        else:
            #var_value = var.get()
            self.process_tab_config_frame_gui(ps_process_tab,var_value,'','')

    def create_new_process_om_call(self,var_process,var_cluster,ps_process_tab):
        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        children_windows=fr_config.winfo_children()

        var_process_value=var_process.get()
        var_cluster_value=var_cluster.get()


        if var_process_value=="Create New Process":
            loop_count=0
            for each in children_windows:
                loop_count+=1
                if loop_count>4:
                    each.destroy()

            lb_new_process=Label(fr_config,text="New Process",bg='gray')
            #lb_new_cluster.place(relx=0.018,rely=0.35,relwidth=0.07)
            lb_new_process.place(relx=0.33, rely=0.35, relwidth=0.07)

            et_new_process=Entry(fr_config)
            et_new_process.place(relx=0.43, rely=0.37,relwidth=0.2)

            bt_new_process_save = Button(fr_config, text="Save", bg='gray',
                                         command=lambda ent=et_new_process,fr=fr_config,var1=var_process,var2=var_cluster :
                                         self.process_save_button_call(ent,fr,var1,var2))
            bt_new_process_save.place(relx=0.43, rely=0.58, relwidth=0.07)

            bt_new_process_cancel = Button(fr_config, text="Cancel", bg='gray',
                                           command=lambda fr=ps_process_tab,val1=var_cluster_value,
                                                          val2=var_process_value :self.process_tab_config_frame_gui(fr,val1,val2,''))
            bt_new_process_cancel.place(relx=0.52, rely=0.58, relwidth=0.07)

        else:
            # var_value = var.get()
            self.process_tab_config_frame_gui(ps_process_tab, var_cluster_value, var_process_value, '')

    def create_new_page_om_call(self,var_page,var_process,var_cluster,ps_process_tab):
        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        children_windows=fr_config.winfo_children()


        var_page_value=var_page.get()
        var_process_value=var_process.get()
        var_cluster_value=var_cluster.get()


        if var_page_value=="Create New Page":
            loop_count=0
            for each in children_windows:
                loop_count+=1
                if loop_count>6:
                    each.destroy()

            lb_new_page=Label(fr_config,text="New Page",bg='gray')
            lb_new_page.place(relx=0.66, rely=0.35, relwidth=0.07)

            et_new_page=Entry(fr_config)
            et_new_page.place(relx=0.76, rely=0.37,relwidth=0.2)

            bt_new_process_save = Button(fr_config, text="Save", bg='gray',command=lambda ent=et_new_page,
                                                                                          fr=fr_config,var2=var_process,var3=var_cluster,
                                                     var1=var_page :self.new_page_save_button_call(ent,fr,var1,var2,var3))
            bt_new_process_save.place(relx=0.76, rely=0.58, relwidth=0.07 )
            #new_page_save_button_call(self, ent, fr, var_page, var_process, var_cluster)
            bt_new_process_cancel = Button(fr_config, text="Cancel", bg='gray',
                                           command=lambda fr=ps_process_tab,val1=var_cluster_value,val2=var_process_value,
                                                          val3=var_page_value :self.process_tab_config_frame_gui(fr,val1,val2,val3))
            bt_new_process_cancel.place(relx=0.85, rely=0.58, relwidth=0.07)

    def cluster_save_button_call(self,ent,fr):
        clusters = self.db.retrive_clusters()
        print(clusters)
        new_cluster_value=ent.get()
        print(new_cluster_value)
        if new_cluster_value not in clusters:
            self.db.create_new_process_page_in_primary_databse(frame=fr,type='process',cluster=new_cluster_value,process='NA',
                                                               page='NA',handler='NA',action='NA',input='NA',output='NA',
                                                               exception='NA',status='NA')
            print('cluster updated')
            messagebox.showinfo("Success", 'Cluster created', parent=fr)
        else:
            messagebox.showerror("Error",'Cluster Already Exists',parent=fr)
            ent.delete(0,END)

    def process_save_button_call(self,ent,fr,var_process,var_cluster):
        val_var_process=var_process.get()
        val_var_cluster=var_cluster.get()
        process = self.db.retrive_process(val_var_cluster)
        print(process)
        new_process_value=ent.get()
        print(new_process_value)
        if new_process_value not in process:
            self.db.create_new_process_page_in_primary_databse(frame=fr,type='process',cluster=val_var_cluster,process=new_process_value,
                                                               page='NA',handler='NA',action='NA',input='NA',output='NA',
                                                               exception='NA',status='NA')
            print('cluster updated')
            messagebox.showinfo("Success", 'Process created', parent=fr)
        else:
            messagebox.showerror("Error",'Process Already Exists',parent=fr)
            ent.delete(0,END)

    def new_page_save_button_call(self,ent,fr,var_page,var_process,var_cluster):
        val_var_page=var_page.get()
        val_var_process=var_process.get()
        val_var_cluster=var_cluster.get()
        page = self.db.retrive_process_page(val_var_process)
        print(page)
        new_page_value=ent.get()
        print(new_page_value)
        if new_page_value not in page:
            self.db.create_new_process_page_in_primary_databse(frame=fr,type='process',cluster=val_var_cluster,process=val_var_process,
                                                               page=new_page_value,handler='NA',action='NA',input='NA',output='NA',
                                                               exception='NA',status='NA')
            print('cluster updated')
            messagebox.showinfo("Success", 'Page created', parent=fr)
        else:
            messagebox.showerror("Error",'Page Already Exists',parent=fr)
            ent.delete(0,END)

    def process_input_window(self,fr_table,handle_var,action_var,var_input,next_row):

        #derive widgets in output tab
        fr_config_output = (self.process_studio_output_tab.winfo_children())[0]
        fr_table_output = (((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table_output.update_idletasks()
        y_socrollbar_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0])
        children_windows_tbl_output=fr_table_output.winfo_children()

        # create TopLevel window for input
        input_window=Toplevel(self.process_studio_notebook)
        input_window.title('Input')
        input_window.geometry("800x400")

        # create table frame
        fr_input_table=Frame(input_window,bg='snow')
        fr_input_table.place(relx=.025, rely=.025, relwidth=.71, relheight=.9)

        # create listbox for output
        fr_output_var_listbox = Frame(input_window, bg='snow')
        fr_output_var_listbox.place(relx=.75, rely=.1, relwidth=.24, relheight=.75)

        # create optionMenu for variables
        var_output_option=StringVar()
        var_output_option.set('Output Variable')
        choices_output=['Output Variable','Application Moduler Variable','Global Variable']
        om_output_var_options=OptionMenu(input_window,var_output_option,*choices_output)
        om_output_var_options.place(relx=.75, rely=.025, relwidth=.24)

        cn_input_table=Canvas(fr_input_table) # create Canvas on table frame
        sb_input_table=Scrollbar(fr_input_table,orient="vertical",command=cn_input_table.yview) # create Scrollbar on table frame
        fr_cn_input_table=Frame(cn_input_table) # create frame on table Canvas

        # create header table for table frame
        lb_input_name=Label(fr_cn_input_table,text="Input Name", font=("Arial Bold", 10), bg='gray87', width=22,relief=GROOVE).grid(row=1,column=1)
        lb_input_value = Label(fr_cn_input_table, text="Input Value", font=("Arial Bold", 10), bg='gray87', width=43,relief=GROOVE).grid(row=1, column=2)
        lb_input_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=3)

        # format input to disply in input window
        input=str(var_input.get())
        if input!='Input':
            input,inputname,input_value=self.format_input(input)
        else:
            input, inputname, input_value = '','',''


        # place input name and value in window
        r=2
        loop_count=0
        for each in range(len(inputname)):
            var_input_name=StringVar()
            var_input_name.set(inputname[loop_count])
            lb_input_name_vale = Label(fr_cn_input_table, textvariable=var_input_name, font=("Arial", 10), bg='gray87', width=22).grid(row=r, column=1)
            var_ent=StringVar()
            var_ent.set(input_value[loop_count])
            et_input_value_val=Entry(fr_cn_input_table, width=58,textvariable=var_ent)

            et_input_value_val.grid(row=r, column=2)
            et_input_value_val.bind('<Button-3>', lambda var_ent=var_ent: self.update_input_value_entrybox(var_ent))
            #et_input_value_val.configure(command=lambda ent=et_input_value_val: self.update_input_value_entrybox(ent,var_ent))
            bt_input_validate = Button(fr_cn_input_table, text="", bg='gray87', width=1)
            bt_input_validate.grid(row=r, column=3)
            bt_input_validate.configure(command=lambda bt=bt_input_validate,ent=et_input_value_val,fr=fr_input_table, :self.input_row_validate_button_call(bt,ent,fr))
            r+=1
            loop_count+=1


        cn_input_table.create_window(0, 0, anchor = 'nw', window = fr_cn_input_table)
        cn_input_table.update_idletasks()

        # configure scrollbar
        cn_input_table.configure(scrollregion=cn_input_table.bbox('all'), yscrollcommand=sb_input_table.set)
        cn_input_table.pack(side='left', expand=True, fill='both')
        sb_input_table.pack(side='right', fill='both')
        sb_variable_listbox = Scrollbar(fr_output_var_listbox)
        sb_variable_listbox.pack(side=RIGHT, fill=Y)

        # Create listbox for variable
        lb_var = Listbox(fr_output_var_listbox)
        lb_var.pack(side='left',fill='both',expand=True)


        # read all the ourput variable name from output tab
        def update_listbox_for_output_variable(*args):
            if var_output_option.get()=='Output Variable':
                output_var=[]
                loop_count=0
                ent_box_count=0
                for each in children_windows_tbl_output:
                    print(each)
                    if each.winfo_class()=='Entry':
                        print(each.get())
                        ent_box_count+=1
                        if ent_box_count%2>0:
                            output_var.append(each.get())

                # insert all the output variable name into listbox
                lb_var.delete(0,END)
                for each in output_var:
                    lb_var.insert(END, each)
            else:
                lb_var.delete(0, END)

        update_listbox_for_output_variable() #when open output window first time, update the output variable names in listbox
        var_output_option.trace_variable('w',update_listbox_for_output_variable) #when the value is select as output variable in OptionMenu, update listbox



        # attach listbox to scrollbar
        lb_var.config(yscrollcommand=sb_variable_listbox.set)
        sb_variable_listbox.config(command=lb_var.yview)

        lb_var.bind('<<ListboxSelect>>', self.lb_onselect) #bind the item listbox to right click

        # place ok button which will update the input label in the table and close the output window
        bt_ok = Button(input_window, text='OK', command=lambda fr=fr_cn_input_table,var=var_input,win=input_window: self.ok_button_call_input_window(fr,var,win))
        bt_ok.place(relx=.86, rely=.878)

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


    def input_row_validate_button_call(self, button, input_value_entry, frame):
        print(button)
        print(input_value_entry)
        # print(input_value_entry.get())
        # str="print(input_value_entry.get())"
        try:
            text = input_value_entry.get()
            if len(text) > 0:
                print("value taken")
                value = str(eval(input_value_entry.get()))
            if len(text) == 0: value = 'None'
            string = "messagebox.showinfo('Input Value',message=value,parent=frame)"
            exec(string)
        except Exception as e:
            error = "Error: " + str(e)
            string = "messagebox.showerror('Input Value',message=error,parent=frame)"
            exec(string)

    def format_input(self,input):
        input_retrived = input

        input, input_name, input_value = list(), list(), list()
        for each_input in (input_retrived.split("\n")):
            if len(each_input) != 0:
                input_name_value_splitted = (each_input.replace("\t", "")).split("=")
                #print(input_name_value_splitted)
                input.append(each_input.replace("\t", ""))
                input_name.append(input_name_value_splitted[0])

                nums = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9,', '0']
                isNum = True

                x = 1 if len(input_name_value_splitted) > 1 else 0
                for each in input_name_value_splitted[x]:
                    if each not in nums: isNum = False
                if isNum == True:
                    if "." in input_name_value_splitted[1]: input_value.append(float(input_name_value_splitted[x]))
                    if "." not in input_name_value_splitted[1]: input_value.append(int(input_name_value_splitted[x]))

                else:

                    if input_name_value_splitted[x]!='str()':
                        input_value.append(input_name_value_splitted[x])
                    else:
                        input_value.append('')
                    # print(input_name_value_splitted[1])
        return input, input_name, input_value

    def ok_button_call_input_window(self,fr,var,win):
        input_name,input_value,input=list(),list(),''
        children_windows=fr.winfo_children()
        loop_count=0
        for each in children_windows:
            loop_count+=1
            #print(each.winfo_class)
            if each.winfo_class()=='Label' and loop_count>3:
                #print(each.cget("text"))
                input_name.append(each.cget("text")) if len(each.cget("text")) >0 else input_name.append(each.cget("text"))
                #input_name.append(each.cget("text"))
            if each.winfo_class() == 'Entry':
                if len(each.get()) > 0:
                    input_value.append(each.get())
                else:
                    input_value.append('str()')


        if len(input_name)>0:
            for each in range(len(input_name)):
                input= input + '\n\t' + input_name[each] + '=' + input_value[each]

        var.set(input)
        win.destroy()
        print(input)

    def ok_button_call_output_window(self, fr, var, win):
        output_name, output_value,storein, output = list(), list(),list(), ''
        children_windows = fr.winfo_children()
        loop_count = 0
        ent_count=0
        for each in children_windows:
            loop_count += 1
            # print(each.winfo_class)
            if each.winfo_class() == 'Label' and loop_count > 4:
                # print(each.cget("text"))
                output_name.append(each.cget("text"))
            if each.winfo_class() == 'Entry':
                ent_count+=1
                if ent_count%2>0:
                    if len(each.get())>0:storein.append(each.get())
                    if len(each.get()) == 0: storein.append('&dummy&')
                if ent_count % 2 == 0:
                    if len(each.get())>0:output_value.append(each.get())
                    if len(each.get()) == 0: output_value.append('str()')

        if len(output_name) > 0:
            for each in range(len(output_name)):
                output = output + '\n\t' + output_name[each] + '=' + storein[each]  + '=' +  output_value[each]

        var.set(output)
        win.destroy()
        print(output)


    def format_output(self,output_list):
        output_retrived = output_list
        print('input_retrived\n',output_retrived)
        output, output_name, output_value,storein = list(), list(), list(),list()
        # print(input_retrived.split("\n"))
        for each_output in (output_retrived.split("\n")):
            if len(each_output) != 0:
                output_name_value_splitted = (each_output.replace("\t", "")).split("=")
                print('output_name_value_splitted: ',output_name_value_splitted)
                output.append(each_output.replace("\t", ""))
                output_name.append(output_name_value_splitted[0])
                if len(output_name_value_splitted)>1:
                    if output_name_value_splitted[1]!='&dummy&':storein.append(output_name_value_splitted[1])
                    if output_name_value_splitted[1] == '&dummy&': storein.append('')


                nums = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9,', '0']
                isNum = True

                x = 2 if len(output_name_value_splitted) > 1 else 0 #derive the position of the output value
                if output_name_value_splitted[x].strip() !=None:
                    print("output value is not  ''")
                    for each in output_name_value_splitted[x]: # check whether the ourput value is a num of text
                        if each not in nums : isNum = False
                if isNum == True: # do below activity if the output value is number
                    if "." in output_name_value_splitted[x]: output_value.append(float(output_name_value_splitted[x])) # if output value consit of '.', the append it as a float
                    if "." not in output_name_value_splitted[x]: output_value.append(int(output_name_value_splitted[x])) # if output value doesnot consist of '.', the append it as a int

                else:
                    if output_name_value_splitted[x]!='str()':output_value.append(output_name_value_splitted[x]) # append output value as text
                    if output_name_value_splitted[x] == 'str()': output_value.append('')  # append output value as text
                    # print(input_name_value_splitted[1])
        return output, output_name, output_value,storein

    def process_output_window(self,fr_table,handle_var,action_var,var_output,next_row):
        #derive widgets in output tab
        fr_config_output = (self.process_studio_output_tab.winfo_children())[0]
        fr_table_output = (((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table_output.update_idletasks()
        y_socrollbar_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0])
        children_windows_tbl_output=fr_table_output.winfo_children()


        print('next row is',next_row)
        print("in toplevel window")
        input_window=Toplevel(self.process_studio_notebook)
        input_window.title('Output')
        input_window.geometry("800x400")



        fr_output_table=Frame(input_window,bg='snow')
        fr_output_table.place(relx=.025, rely=.025, relwidth=.71, relheight=.9)

        fr_output_var_listbox = Frame(input_window, bg='snow')
        fr_output_var_listbox.place(relx=.75, rely=.1, relwidth=.24, relheight=.75)

        var_output_option=StringVar()
        var_output_option.set('Output Variable')
        choices_output=['Output Variable','Application Moduler Variable','Global Variable']
        om_output_var_options=OptionMenu(input_window,var_output_option,*choices_output)
        om_output_var_options.place(relx=.75, rely=.025, relwidth=.24)



        cn_output_table=Canvas(fr_output_table)
        sb_output_table=Scrollbar(fr_output_table,orient="vertical",command=cn_output_table.yview)

        fr_cn_input_table=Frame(cn_output_table)


        lb_output_name=Label(fr_cn_input_table,text="Output Name", font=("Arial Bold", 10), bg='gray87', width=22,relief=GROOVE).grid(row=1,column=1)
        lb_output_storein = Label(fr_cn_input_table, text="Store In", font=("Arial Bold", 10), bg='gray87', width=18,relief=GROOVE).grid(row=1, column=2)
        #lb_output_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=3)
        lb_output_value = Label(fr_cn_input_table, text="Output Value", font=("Arial Bold", 10), bg='gray87', width=30,relief=GROOVE).grid(row=1, column=3)
        lb_output_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=4)

        #input=self.db.retrive_input_for_action(handle_var.get(),action_var.get())
        print('printing input\n',var_output.get())
        output=str(var_output.get())
        if output!='Output':
            output, output_name, output_value,storein=self.format_output(output)
        else:
            output, output_name, output_value, storein = '','','',''
        print(output, output_name, output_value,storein)

        r=2
        loop_count=0
        for each in range(len(output_name)):
            var_input_name=StringVar()
            var_input_name.set(output_name[loop_count])
            lb_input_name_vale = Label(fr_cn_input_table, textvariable=var_input_name, font=("Arial", 10), bg='gray87', width=22).grid(row=r, column=1)

            var_storein = StringVar()
            var_storein.set(storein[loop_count])
            #var_storein.set(input_value[loop_count])
            et_storein = Entry(fr_cn_input_table, width=24, textvariable=var_storein)
            et_storein.bind('<Button-3>', lambda var_ent=var_storein: self.update_input_value_entrybox(var_ent))
            et_storein.grid(row=r, column=2)

            var_ent=StringVar()
            var_ent.set(output_value[loop_count])
            et_input_value_val=Entry(fr_cn_input_table, width=40,textvariable=var_ent)
            et_input_value_val.grid(row=r, column=3)

            #et_input_value_val.configure(command=lambda ent=et_input_value_val: self.update_input_value_entrybox(ent,var_ent))
            bt_input_validate = Button(fr_cn_input_table, text="", bg='gray87', width=1)
            bt_input_validate.configure(command=lambda bt=bt_input_validate,ent=et_input_value_val,fr=cn_output_table, :self.input_row_validate_button_call(bt,ent,fr))
            bt_input_validate.grid(row=r, column=4)

            r+=1
            loop_count+=1

        cn_output_table.create_window(0, 0, anchor = 'nw', window = fr_cn_input_table)

        cn_output_table.update_idletasks()

        cn_output_table.configure(scrollregion=cn_output_table.bbox('all'), yscrollcommand=sb_output_table.set)
        cn_output_table.pack(side='left', expand=True, fill='both')
        cn_output_table.pack(side='right', fill='both')



        sb_variable_listbox = Scrollbar(fr_output_var_listbox)
        sb_variable_listbox.pack(side=RIGHT, fill=Y)

        lb_var = Listbox(fr_output_var_listbox)
        lb_var.pack(side='left',fill='both',expand=True)

        # read all the ourput variable name from output tab
        def update_listbox_for_output_variable(*args):
            if var_output_option.get() == 'Output Variable':
                output_var = []
                loop_count = 0
                ent_box_count = 0
                for each in children_windows_tbl_output:
                    print(each)
                    if each.winfo_class() == 'Entry':
                        print(each.get())
                        ent_box_count += 1
                        if ent_box_count % 2 > 0:
                            output_var.append(each.get())

                # insert all the output variable name into listbox
                lb_var.delete(0, END)
                for each in output_var:
                    lb_var.insert(END, each)
            else:
                lb_var.delete(0, END)

        update_listbox_for_output_variable()  # when open output window first time, update the output variable names in listbox
        var_output_option.trace_variable('w',
                                         update_listbox_for_output_variable)  # when the value is select as output variable in OptionMenu, update listbox

        '''output=[]
        current_row = next_row
        print('previous row' ,current_row-1)
        if current_row>1:
         loop_count=0
         output_wid_position=5
         for each_wid in fr_table.winfo_children():
             loop_count+=1
             if loop_count/7==current_row-1:
                 print('loop_countdiveded7',loop_count/7)
                 break
             if loop_count==output_wid_position:
                 output_wid_position+=7
                 output.append(each_wid.cget('text'))'''

        '''print(output)
        for i in range(100):
            lb_var.insert(END, i)'''

        # attach listbox to scrollbar
        lb_var.config(yscrollcommand=sb_variable_listbox.set)
        sb_variable_listbox.config(command=lb_var.yview)

        lb_var.bind('<<ListboxSelect>>', self.lb_onselect)

        bt_ok = Button(input_window, text='OK', command=lambda fr=fr_cn_input_table,var=var_output,win=input_window: self.ok_button_call_output_window(fr,var,win))
        bt_ok.place(relx=.86, rely=.878)

    def add_row_button_call(self, ps_process_tab):
        #define widgets in process tab

        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table.update_idletasks()
        y_socrollbar = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0])
        children_windows = fr_table.winfo_children()
        rows_tableframe = (len(children_windows)) / 7

        # whenever checkbutton is checked, instance dictionary-check_button_dict will be updated with rows and its value
        def get_checkbutton_value(cb, var):
            val = var.get()
            row = cb.grid_info()['row']
            #row += 1
            self.check_button_dict[row] = val
            print(self.check_button_dict)


        # call back function for handler variable change
        def refresh_handle_om(om_action, var_action, var_handler, var_input, var_output, lb_input):
            # Reset var and delete all old options
            menu = om_action['menu']
            var_action.set('')
            menu.delete(0, 'end')

            # retrive action list for handler
            actions_list = self.db.retrive_action_for_handles(var_handler.get())
            #print('action list\n',actions_list)

            # command for each menu in action opetion menu drop down
            def refresh_action_om(action, var_handler, var_action, var_input, var_output, lb_input):
                print("actions: ", action)
                var_action.set(action)
                handler = var_handler.get()
                input = self.db.retrive_input_for_action(handler, action)
                output = self.db.retrive_output_for_action(handler, action)
                var_input.set(input)
                var_output.set(output)

            # add menu in action OptionMenu for  each actuion in action list
            for actions in actions_list:
                menu.add_command(label=actions,
                                 command=lambda action=actions: refresh_action_om(action,
                                                                                  var_handler, var_action, var_input,
                                                                                  var_output, lb_input))

        # Find any checkbutton is checked and get the row checked
        checked=False
        checked_row=''
        for each in self.check_button_dict:
            if self.check_button_dict[each]==1:
                checked=True
                checked_row=each

        # perform below activity if any row is checked
        if checked==False:
            next_row = 1

            #  derive the next row considering current rumber of rows
            if rows_tableframe >= 1: next_row = int(rows_tableframe) + 1

            # create sequential label
            lb_input = Label(fr_table, text=next_row, fg='blue', underline=1, width=3, relief=FLAT)
            lb_input.grid(row=next_row, column=1)

            # create handle OptionMenu
            tem_var_list=[]
            var_handler1 = StringVar()
            chocices_handler = self.db.retrive_all_handles()
            om_handler1 = OptionMenu(fr_table, var_handler1, *chocices_handler)
            om_handler1.config(width=38)
            om_handler1.grid(row=next_row, column=2)
            tem_var_list.append(var_handler1)

            # create action OptionMenu
            var_action1 = StringVar()
            chocices_action = ['Dummy']
            om_action1 = OptionMenu(fr_table, var_action1, *chocices_action)
            om_action1.config(width=38)
            om_action1.grid(row=next_row, column=3)
            tem_var_list.append(var_action1)

            # create input label
            var_input1, var_input_name, var_input_value = StringVar(), list(), list()
            var_input1.set('Input')
            lb_input1 = Label(fr_table, text='Input', fg='blue', underline=1, width=24, relief=FLAT, textvariable=var_input1)
            lb_input1.grid(row=next_row, column=4)
            lb_input1.bind('<Button-1>',
                          lambda x: self.process_input_window(fr_table, var_handler1, var_action1, var_input1, next_row))

            tem_var_list.append(var_input1)

            # create output label
            var_output1 = StringVar()
            var_output1.set('Output')
            lb_output = Label(fr_table, text='Output', fg='blue', underline=1, width=25, relief=FLAT,
                              textvariable=var_output1)
            lb_output.grid(row=next_row, column=5)
            lb_output.bind('<Button-1>',
                           lambda x: self.process_output_window(fr_table, var_handler1, var_action1, var_output1, next_row))
            tem_var_list.append(var_output1)

            # create exception label
            var_exception1 = StringVar()
            lb_exception_handle = Label(fr_table, text='Exception Handle', fg='blue', underline=1, width=18, relief=FLAT,textvariable=var_exception1)
            lb_exception_handle.grid(row=next_row, column=6)
            tem_var_list.append(var_exception1)
            self.var_table.append(tem_var_list)

            # create CheckButton
            var_row_select = IntVar()
            cbt_tbl = Checkbutton(fr_table, text="", variable=var_row_select, onvalue=1, offvalue=0, width=2)
            cbt_tbl.configure(command=lambda cb=cbt_tbl, var=var_row_select: get_checkbutton_value(cb, var))
            cbt_tbl.grid(row=next_row, column=7)

            # configure scrollbar
            cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
            y_socrollbar.config(command=cn_on_fr_table.yview)
            y_socrollbar.pack(side=RIGHT, fill=Y)


            # trace handler varibale
            var_handler1.trace('w',
                              lambda x, y, z: refresh_handle_om(om_action1, var_action1, var_handler1, var_input1, var_output1,
                                                                lb_input1))


            #print('var table:\n',self.var_table)

        # preform the below activity if checked
        if checked == True:
            # read all the rows and store in var_value list
            var_values=[]
            loop_count=0
            for each_row in self.var_table:
                loop_count+=1
                var_value_temp = []
                var_value_temp.append((each_row[0]).get())
                var_value_temp.append((each_row[1]).get())
                var_value_temp.append((each_row[2]).get())
                var_value_temp.append((each_row[3]).get())
                var_value_temp.append((each_row[4]).get())
                var_values.append(var_value_temp)

                if loop_count==checked_row:
                    var_value_temp = []
                    var_value_temp.append('')
                    var_value_temp.append('')
                    var_value_temp.append('Input')
                    var_value_temp.append('Output')
                    var_value_temp.append('Exception Handle')
                    var_values.append(var_value_temp)
            print('var_values\n',var_values)


            self.var_table=[]

            # destory all the widgets in table
            for each in children_windows:
                each.destroy()

            # place the widgets for var_values
            loop_count=0
            next_row=0
            for each in var_values:
                loop_count+=1
                next_row+=1

                # create label for sequence
                lb_input = Label(fr_table, text=loop_count, fg='blue', underline=1, width=3, relief=FLAT)
                lb_input.grid(row=next_row, column=1)

                # create OptionMenu for handler
                tem_var_list = []
                var_handler = StringVar()
                var_handler.set(each[0])
                chocices_handler = self.db.retrive_all_handles()
                om_handler = OptionMenu(fr_table, var_handler , *chocices_handler)
                om_handler.config(width=38)
                om_handler.grid(row=next_row, column=2)
                tem_var_list.append(var_handler )

                # create OptionMenu for action
                var_action = StringVar()
                var_action.set(each[1])
                chocices_action = ['Dummy']
                om_action = OptionMenu(fr_table, var_action, *chocices_action)
                om_action .config(width=38)
                om_action .grid(row=next_row, column=3)
                # self.var_table.append(var_action)
                tem_var_list.append(var_action)
                #print('om_action: ',om_action )

                # create label for input
                var_input, var_input_name, var_input_value = StringVar(), list(), list()
                var_input.set(each[2])
                lb_input = Label(fr_table, text='Input', fg='blue', underline=1, width=24, relief=FLAT,
                                 textvariable=var_input)
                lb_input.grid(row=next_row, column=4)
                lb_input.bind('<Button-1>',
                              lambda fr_table=fr_table, var_handler=var_handler,
                                     var_action=var_action, var_input=var_input,
                                     next_row=next_row: self.process_input_window(fr_table, var_handler, var_action, var_input,
                                                                  next_row))

                tem_var_list.append(var_input)

                # create label for output
                var_output = StringVar()
                var_output.set(each[3])
                lb_output = Label(fr_table, text='Output', fg='blue', underline=1, width=25, relief=FLAT,
                                  textvariable=var_output)
                lb_output.grid(row=next_row, column=5)
                lb_output.bind('<Button-1>',
                               lambda fr_table=fr_table,var_handler=var_handler,
                                      var_action=var_action,
                                      var_output=var_output,next_row=next_row: self.process_output_window(fr_table, var_handler, var_action, var_output,
                                                                    next_row))
                tem_var_list.append(var_output)

                # create label for exception
                var_exception = StringVar()
                var_exception.set(each[4])
                lb_exception_handle = Label(fr_table, text='Exception Handle', fg='blue', underline=1, width=18,
                                            relief=FLAT, textvariable=var_exception)
                lb_exception_handle.grid(row=next_row, column=6)
                tem_var_list.append(var_exception)
                self.var_table.append(tem_var_list)

                # create CheckButton
                var_row_select = IntVar()
                cbt_tbl = Checkbutton(fr_table, text="", variable=var_row_select, onvalue=1, offvalue=0, width=2)
                cbt_tbl.configure(command=lambda cb=cbt_tbl, var=var_row_select: get_checkbutton_value(cb, var))
                cbt_tbl.grid(row=next_row, column=7)

                # configure scrollbar
                cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
                y_socrollbar.config(command=cn_on_fr_table.yview)
                y_socrollbar.pack(side=RIGHT, fill=Y)

                # trace handler
                var_handler.trace_variable('w',lambda m,n,o,x=om_action, y=var_action, z=var_handler, a=var_input,b=var_output,c=lb_input:refresh_handle_om(x,y,z,a,b,c))
                print('var table:\n', self.var_table)

        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0

    def del_row_button_call(self, ps_process_tab):

        #define frames and widgets
        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table.update_idletasks()
        y_socrollbar = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0])
        children_windows = fr_table.winfo_children()
        rows_tableframe = (len(children_windows)) / 7

        # whenever checkbutton is checked, instance dictionary-check_button_dict will be updated with rows and its value
        def get_checkbutton_value(cb, var):
            val = var.get()
            row = cb.grid_info()['row']
            #row += 1
            self.check_button_dict[row] = val
            #print(self.check_button_dict)

        # call function for change in handler value
        def refresh_handle_om(om_action, var_action, var_handler, var_input, var_output, lb_input):
            # Reset var and delete all old options
            menu = om_action['menu']
            var_action.set('')
            menu.delete(0, 'end')

            actions_list = self.db.retrive_action_for_handles(var_handler.get())

            def refresh_action_om(action, var_handler, var_action, var_input, var_output, lb_input):
                print("actions: ", action)
                var_action.set(action)
                handler = var_handler.get()
                input = self.db.retrive_input_for_action(handler, action)
                output = self.db.retrive_output_for_action(handler, action)
                var_input.set(input)
                var_output.set(output)

            for actions in actions_list:
                menu.add_command(label=actions,
                                 command=lambda action=actions: refresh_action_om(action,
                                                                                  var_handler, var_action, var_input,
                                                                                  var_output, lb_input))

        # Find any checkbutton is checked and store in checked row
        checked=False
        checked_row=''
        for each in self.check_button_dict:
            if self.check_button_dict[each]==1:
                checked=True
                checked_row=each

        # perform the bewlo activity if any row is checked
        if checked == True:
            var_values=[]
            loop_count=0

            # read all the rows except to the row checked
            for each_row in self.var_table:
                loop_count+=1
                if loop_count==checked_row:
                    continue
                else:
                    var_value_temp = []
                    var_value_temp.append((each_row[0]).get())
                    var_value_temp.append((each_row[1]).get())
                    var_value_temp.append((each_row[2]).get())
                    var_value_temp.append((each_row[3]).get())
                    var_value_temp.append((each_row[4]).get())
                    var_values.append(var_value_temp)

            #print('var_values\n',var_values)

            self.var_table=[]

            # destory all the widgets in the table
            for each in children_windows:
                each.destroy()

            # place all the widgets for the values read in var_vales
            loop_count=0
            next_row=0
            for each in var_values:
                loop_count+=1
                next_row+=1

                lb_input = Label(fr_table, text=loop_count, fg='blue', underline=1, width=3, relief=FLAT)
                lb_input.grid(row=next_row, column=1)

                tem_var_list = []
                var_handler = StringVar()
                var_handler.set(each[0])
                chocices_handler = self.db.retrive_all_handles()
                om_handler = OptionMenu(fr_table, var_handler , *chocices_handler)
                om_handler.config(width=38)
                om_handler.grid(row=next_row, column=2)
                tem_var_list.append(var_handler )

                var_action = StringVar()
                var_action.set(each[1])
                chocices_action = ['Dummy']
                om_action = OptionMenu(fr_table, var_action, *chocices_action)
                om_action .config(width=38)
                om_action .grid(row=next_row, column=3)
                # self.var_table.append(var_action)
                tem_var_list.append(var_action)
                print('om_action: ',om_action )

                var_input, var_input_name, var_input_value = StringVar(), list(), list()
                var_input.set(each[2])
                lb_input = Label(fr_table, text='Input', fg='blue', underline=1, width=24, relief=FLAT,
                                 textvariable=var_input)
                lb_input.grid(row=next_row, column=4)
                # lb_input.bind('<Button-1>',lambda x: messagebox.showinfo('input'))
                lb_input.bind('<Button-1>',
                              lambda x: self.process_input_window(fr_table, var_handler, var_action, var_input,
                                                                  next_row))

                tem_var_list.append(var_input)

                var_output = StringVar()
                var_output.set(each[3])
                lb_output = Label(fr_table, text='Output', fg='blue', underline=1, width=25, relief=FLAT,
                                  textvariable=var_output)
                lb_output.grid(row=next_row, column=5)
                lb_output.bind('<Button-1>',
                               lambda x: self.process_output_window(fr_table, var_handler, var_action, var_output,
                                                                    next_row))
                # self.var_table.append(var_output)
                tem_var_list.append(var_output)

                var_exception = StringVar()
                var_exception.set(each[4])
                lb_exception_handle = Label(fr_table, text='Exception Handle', fg='blue', underline=1, width=18,
                                            relief=FLAT, textvariable=var_exception)
                lb_exception_handle.grid(row=next_row, column=6)

                tem_var_list.append(var_exception)
                self.var_table.append(tem_var_list)

                var_row_select = IntVar()
                cbt_tbl = Checkbutton(fr_table, text="", variable=var_row_select, onvalue=1, offvalue=0, width=2)
                cbt_tbl.configure(command=lambda cb=cbt_tbl, var=var_row_select: get_checkbutton_value(cb, var))
                cbt_tbl.grid(row=next_row, column=7)

                cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
                y_socrollbar.config(command=cn_on_fr_table.yview)
                y_socrollbar.pack(side=RIGHT, fill=Y)


                var_handler.trace_variable('w',lambda m,n,o,x=om_action, y=var_action, z=var_handler, a=var_input,b=var_output,c=lb_input:refresh_handle_om(x,y,z,a,b,c))
                #print('var table:\n', self.var_table)

        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0

class ProcessStudioOutputTab:

    def __init__(self,process_studio_notebook,database):
        self.process_studio_notebook=process_studio_notebook
        self.db=database
        self.check_button_dict = {}
        self.var_table = []

    def output_tab(self,process_studio_process_tab):
        fr_config=Frame(process_studio_process_tab,bd=0)
        fr_config.place(relx=0.015,rely=0.015,relheight=0.04,relwidth=0.97)

        fr_table=Frame(process_studio_process_tab,bd=0,relief=FLAT,highlightthickness=0)
        fr_table.place(relx=0.015, rely=0.058, relheight=0.75, relwidth=0.97)

        cn_on_fr_table=Canvas(fr_table,bd=0,relief=FLAT,highlightthickness=0)
        cn_on_fr_table.pack(side=BOTTOM,fill=BOTH,expand=True)

        fr_header_on_fr_table=Canvas(fr_table,height=1,bd=0,relief=GROOVE,highlightthickness=0)
        fr_header_on_fr_table.pack(side=TOP,fill=X)

        #Label(fr_header_on_fr_table, text='', width=4, relief=RAISED,bg='gray87').grid(row=1, column=1)
        Label(fr_header_on_fr_table, text='     ', relief=GROOVE, bg='gray87').grid(row=1, column=1)
        Label(fr_header_on_fr_table,text='Variable',width=43,relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1,column=2)
        Label(fr_header_on_fr_table, text='Value', width=88, relief=GROOVE,bg='gray87', font=("Arial Bold", 10)).grid(row=1, column=3)
        #Label(fr_header_on_fr_table, text='Input', width=20, relief=RAISED,bg='gray87').grid(row=1, column=4)
        #Label(fr_header_on_fr_table, text='Output', width=20, relief=RAISED,bg='gray87').grid(row=1, column=5)
        #Label(fr_header_on_fr_table, text='Exception Handle', width=20, relief=RAISED,bg='gray87').grid(row=1, column=6)

        frame=Frame(cn_on_fr_table,bd=0,relief=FLAT,takefocus = 0)
        y_socrollbar=Scrollbar(cn_on_fr_table)
        y_socrollbar.pack(side=RIGHT,fill=Y)

        cn_on_fr_table.create_window(0, 0, anchor='nw', window=frame)
        cn_on_fr_table.update_idletasks()

        cn_on_fr_table.config(yscrollcommand=y_socrollbar.set)
        y_socrollbar.config(command=cn_on_fr_table.yview)


        bt_add = Button(fr_config, text="Add",command=lambda :self.add_row_button_call(process_studio_process_tab))
        #bt_add.place(relx=0.2, rely=0.5, relwidth=0.035)
        bt_add.grid(row=1,column=1)

        bt_del = Button(fr_config, text="Del", command=lambda :self.del_row_button_call(process_studio_process_tab))
        #bt_del.place(relx=0.235, rely=0.5, relwidth=0.035)
        bt_del.grid(row=1, column=2)

        bt_Save = Button(fr_config, text="Save")
        #bt_del.place(relx=0.235, rely=0.5, relwidth=0.035)
        bt_Save.grid(row=1, column=3)

        #self.process_tab_config_frame_gui(process_studio_process_tab,'',"","")

    def del_row_button_call(self, ps_process_tab):

        #define frames and widgets
        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table.update_idletasks()
        y_socrollbar = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0])
        children_windows = fr_table.winfo_children()
        rows_tableframe = (len(children_windows)) / 7

        # whenever checkbutton is checked, instance dictionary-check_button_dict will be updated with rows and its value
        def get_checkbutton_value(cb, var):
            val = var.get()
            row = cb.grid_info()['row']
            #row += 1
            self.check_button_dict[row] = val
            #print(self.check_button_dict)

        # call function for change in handler value
        def refresh_handle_om(om_action, var_action, var_handler, var_input, var_output, lb_input):
            # Reset var and delete all old options
            menu = om_action['menu']
            var_action.set('')
            menu.delete(0, 'end')

            actions_list = self.db.retrive_action_for_handles(var_handler.get())

            def refresh_action_om(action, var_handler, var_action, var_input, var_output, lb_input):
                print("actions: ", action)
                var_action.set(action)
                handler = var_handler.get()
                input = self.db.retrive_input_for_action(handler, action)
                output = self.db.retrive_output_for_action(handler, action)
                var_input.set(input)
                var_output.set(output)

            for actions in actions_list:
                menu.add_command(label=actions,
                                 command=lambda action=actions: refresh_action_om(action,
                                                                                  var_handler, var_action, var_input,
                                                                                  var_output, lb_input))

        # Find any checkbutton is checked and store in checked row
        checked=False
        checked_row=''
        for each in self.check_button_dict:
            if self.check_button_dict[each]==1:
                checked=True
                checked_row=each

        # perform the bewlo activity if any row is checked
        if checked == True:
            var_values=[]
            loop_count=0

            # read all the rows except to the row checked
            for each_row in self.var_table:
                loop_count+=1
                if loop_count==checked_row:
                    continue
                else:
                    var_value_temp = []
                    var_value_temp.append((each_row[0]).get())
                    var_value_temp.append((each_row[1]).get())

                    var_values.append(var_value_temp)

           # print('var_values\n',var_values)

            self.var_table=[]

            # destory all the widgets in the table
            for each in children_windows:
                each.destroy()

            # place all the widgets for the values read in var_vales
            loop_count=0
            next_row=0
            for each in var_values:
                loop_count+=1
                next_row+=1
                tem_var_list = []

                Label(fr_table, text=next_row, relief=FLAT, bg='gray87').grid(row=next_row, column=1)

                # create Entrybox for variablename
                var_variable_name = StringVar()
                var_variable_name.set(each[0])
                ent_variable = Entry(fr_table, bg='snow', width=58, textvariable=var_variable_name)
                ent_variable.grid(row=next_row, column=2)
                #print('row for new var name: ', ent_variable.grid_info()['row'])
                tem_var_list.append(var_variable_name)

                # create Entrybox for variable value
                var_variable_value = StringVar()
                var_variable_value.set(each[1])
                ent_variable = Entry(fr_table, bg='snow', width=118, textvariable=var_variable_value)
                ent_variable.grid(row=next_row, column=3)
                tem_var_list.append(var_variable_value)

                self.var_table.append(tem_var_list)

                # create CheckButton for selecting row
                var_row_select = IntVar()
                cb_row_select = Checkbutton(fr_table, variable=var_row_select)
                cb_row_select.configure(
                    command=lambda cb=cb_row_select, var=var_row_select: get_checkbutton_value(cb, var))
                cb_row_select.grid(row=next_row, column=4)


        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0


    def add_row_button_call(self, ps_process_tab):
        #define widgets in process tab

        fr_config = (ps_process_tab.winfo_children())[0]
        fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table.update_idletasks()
        y_socrollbar = (((ps_process_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table = (((ps_process_tab.winfo_children())[1]).winfo_children()[0])
        children_windows = fr_table.winfo_children()
        rows_tableframe = (len(children_windows)) / 4

        # whenever checkbutton is checked, instance dictionary-check_button_dict will be updated with rows and its value
        def get_checkbutton_value(cb, var):
            val = var.get()
            row = cb.grid_info()['row']
            #row += 1
            self.check_button_dict[row] = val
            print(self.check_button_dict)


        # call back function for handler variable change
        def refresh_handle_om(om_action, var_action, var_handler, var_input, var_output, lb_input):
            # Reset var and delete all old options
            menu = om_action['menu']
            var_action.set('')
            menu.delete(0, 'end')

            # retrive action list for handler
            actions_list = self.db.retrive_action_for_handles(var_handler.get())
            #print('action list\n',actions_list)

            # command for each menu in action opetion menu drop down
            def refresh_action_om(action, var_handler, var_action, var_input, var_output, lb_input):
                print("actions: ", action)
                var_action.set(action)
                handler = var_handler.get()
                input = self.db.retrive_input_for_action(handler, action)
                output = self.db.retrive_output_for_action(handler, action)
                var_input.set(input)
                var_output.set(output)

            # add menu in action OptionMenu for  each actuion in action list
            for actions in actions_list:
                menu.add_command(label=actions,
                                 command=lambda action=actions: refresh_action_om(action,
                                                                                  var_handler, var_action, var_input,
                                                                                  var_output, lb_input))

        # Find any checkbutton is checked and get the row checked
        checked=False
        checked_row=''
        for each in self.check_button_dict:
            if self.check_button_dict[each]==1:
                checked=True
                checked_row=each
                print('checked_row: ',checked_row)

        # perform below activity if any row is checked
        if checked==False:
            next_row = 1
            tem_var_list = []

            #  derive the next row considering current rumber of rows
            if rows_tableframe >= 1: next_row = int(rows_tableframe) + 1

            print('next row',next_row)
            Label(fr_table, text=next_row, relief=FLAT, bg='gray87').grid(row=next_row, column=1)

            # create Entrybox for variablename
            var_variable_name=StringVar()
            ent_variable = Entry(fr_table, bg='snow', width=58,textvariable=var_variable_name)
            ent_variable.grid(row=next_row, column=2)
            print('row for new var name: ', ent_variable.grid_info()['row'])
            tem_var_list.append(var_variable_name)

            # create Entrybox for variable value
            var_variable_value = StringVar()
            ent_variable = Entry(fr_table, bg='snow', width=118,textvariable=var_variable_value)
            ent_variable.grid(row=next_row, column=3)
            tem_var_list.append(var_variable_value)

            self.var_table.append(tem_var_list)

            # create CheckButton for selecting row
            var_row_select = IntVar()
            cb_row_select = Checkbutton(fr_table, variable=var_row_select)
            cb_row_select.configure(command=lambda cb=cb_row_select, var=var_row_select: get_checkbutton_value(cb, var))
            cb_row_select.grid(row=next_row, column=4)



            # create sequential label
            '''lb_input = Label(fr_table, text=next_row, fg='blue', underline=1, width=3, relief=FLAT)
            lb_input.grid(row=next_row, column=1)

            # create handle OptionMenu
            tem_var_list=[]
            var_handler1 = StringVar()
            chocices_handler = self.db.retrive_all_handles()
            om_handler1 = OptionMenu(fr_table, var_handler1, *chocices_handler)
            om_handler1.config(width=38)
            om_handler1.grid(row=next_row, column=2)
            tem_var_list.append(var_handler1)

            # create action OptionMenu
            var_action1 = StringVar()
            chocices_action = ['Dummy']
            om_action1 = OptionMenu(fr_table, var_action1, *chocices_action)
            om_action1.config(width=38)
            om_action1.grid(row=next_row, column=3)
            tem_var_list.append(var_action1)

            # create input label
            var_input1, var_input_name, var_input_value = StringVar(), list(), list()
            var_input1.set('Input')
            lb_input1 = Label(fr_table, text='Input', fg='blue', underline=1, width=24, relief=FLAT, textvariable=var_input1)
            lb_input1.grid(row=next_row, column=4)
            lb_input1.bind('<Button-1>',
                          lambda x: self.process_input_window(fr_table, var_handler1, var_action1, var_input1, next_row))

            tem_var_list.append(var_input1)

            # create output label
            var_output1 = StringVar()
            var_output1.set('Output')
            lb_output = Label(fr_table, text='Output', fg='blue', underline=1, width=25, relief=FLAT,
                              textvariable=var_output1)
            lb_output.grid(row=next_row, column=5)
            lb_output.bind('<Button-1>',
                           lambda x: self.process_output_window(fr_table, var_handler1, var_action1, var_input1, next_row))
            tem_var_list.append(var_output1)

            # create exception label
            var_exception1 = StringVar()
            lb_exception_handle = Label(fr_table, text='Exception Handle', fg='blue', underline=1, width=18, relief=FLAT,textvariable=var_exception1)
            lb_exception_handle.grid(row=next_row, column=6)
            tem_var_list.append(var_exception1)
            self.var_table.append(tem_var_list)

            # create CheckButton
            var_row_select = IntVar()
            cbt_tbl = Checkbutton(fr_table, text="", variable=var_row_select, onvalue=1, offvalue=0, width=2)
            cbt_tbl.configure(command=lambda cb=cbt_tbl, var=var_row_select: get_checkbutton_value(cb, var))
            cbt_tbl.grid(row=next_row, column=7)

            # configure scrollbar
            cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
            y_socrollbar.config(command=cn_on_fr_table.yview)
            y_socrollbar.pack(side=RIGHT, fill=Y)


            # trace handler varibale
            var_handler1.trace('w',
                              lambda x, y, z: refresh_handle_om(om_action1, var_action1, var_handler1, var_input1, var_output1,
                                                                lb_input1))


            #print('var table:\n',self.var_table)'''

        # preform the below activity if checked
        if checked == True:
            # read all the rows and store in var_value list
            var_values=[]
            loop_count=0
            for each_row in self.var_table:
                loop_count+=1
                var_value_temp = []
                var_value_temp.append((each_row[0]).get())
                var_value_temp.append((each_row[1]).get())
                var_values.append(var_value_temp)

                if loop_count==checked_row:
                    var_value_temp = []
                    var_value_temp.append('')
                    var_value_temp.append('')

                    var_values.append(var_value_temp)
            #print('var_values\n',var_values)

            self.var_table=[]

            # destory all the widgets in table
            for each in children_windows:
                each.destroy()

            # place the widgets for var_values
            loop_count=0
            next_row=0
            for each in var_values:
                loop_count+=1
                next_row+=1
                tem_var_list = []

                Label(fr_table, text=next_row, relief=FLAT, bg='gray87').grid(row=next_row, column=1)

                # create Entrybox for variablename
                var_variable_name = StringVar()
                var_variable_name.set(each[0])
                ent_variable = Entry(fr_table, bg='snow', width=58, textvariable=var_variable_name)
                ent_variable.grid(row=next_row, column=2)
                #print('row for new var name: ', ent_variable.grid_info()['row'])
                tem_var_list.append(var_variable_name)

                # create Entrybox for variable value
                var_variable_value = StringVar()
                var_variable_value.set(each[1])
                ent_variable = Entry(fr_table, bg='snow', width=118, textvariable=var_variable_value)
                ent_variable.grid(row=next_row, column=3)
                tem_var_list.append(var_variable_value)

                self.var_table.append(tem_var_list)

                # create CheckButton for selecting row
                var_row_select = IntVar()
                cb_row_select = Checkbutton(fr_table, variable=var_row_select)
                cb_row_select.configure(
                    command=lambda cb=cb_row_select, var=var_row_select: get_checkbutton_value(cb, var))
                cb_row_select.grid(row=next_row, column=4)

        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0
