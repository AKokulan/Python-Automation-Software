from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
import os,shutil
from datetime import datetime
import tkinter
import re
import json

import Database_Del
import GuiGloballVariable
import  Database

class ProcessStudio:
    def __init__(self,process_studio_notebook,primary_db_path,secondary_db_path):
        self.process_studio_notebook=process_studio_notebook
        self.primary_db_path=primary_db_path
        self.secondary_db_path=secondary_db_path
        self.db=Database.database(self.primary_db_path,self.secondary_db_path)
        self.root=100
        self.process_table_var_dict={} #store the variable of the table by rows

        self.test={}
        self.storein_output_dict = {}
        self.process_val_dict = {}

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




        output_tab=ProcessStudioOutputTab(self.process_studio_notebook,process_studio_output_tab,self.primary_db_path,self.secondary_db_path)
        output_tab_table_frame=output_tab.output_tab(process_studio_output_tab)

        process_tab=ProcessStudioProcessTab(self.process_studio_notebook,process_studio_output_tab,output_tab_table_frame,self.primary_db_path,self.secondary_db_path)
        process_tab.process_tab(process_studio_process_tab)
        '''def callback_process_studio_output_tab():
            print("clciked on process tab")
            process_tab = ProcessStudioProcessTab(self.process_studio_notebook, self.db, process_studio_output_tab)
            process_tab.process_tab(process_studio_process_tab)
            print("clciked on process tab")

        process_studio_process_tab.bind("<Button-1>", callback_process_studio_output_tab)'''



class ProcessStudioProcessTab(ProcessStudio):

    def __init__(self,process_studio_notebook,process_studio_output_tab,outputtab_table_frame,primary_db_path,secondary_db_path):
        super().__init__(process_studio_notebook,primary_db_path,secondary_db_path)
        self.primary_db_path=primary_db_path
        self.secondary_db_path=secondary_db_path
        self.process_studio_notebook=process_studio_notebook
        self.db=Database.database(self.primary_db_path,self.secondary_db_path)
        #self.root=100
        self.process_studio_output_tab=process_studio_output_tab
        self.outputtab_table_frame=outputtab_table_frame
        #self.process_tab=ProcessStudioOutputTab(process_studio_notebook,database)


        self.check_button_dict = {} # #create dictionary to store rownumber as o/1 for whther row is selected or not in table
        self.var_table=[] # creare list to store all the variabeles from table as a list

        self.step_output_dict={} # output value dictonary for step. Dic will be cleared with refresh button call

        #  1. create dictionary to store the strein key and value when click step button
        #  2. called in step button call to retrive the value for input and update the result output value
        #  3. called in refresh button call to clear the value
        self.step_button_call_storein_dict={}

        self.cluster_om_var_val="" #store value selected in cluster option menu with --create_new_cluster_om_call
        self.process_om_var_val = "" #store value selected in process option menu with --create_new_process_om_call
        self.page_om_var_val = "" #store value selected in page option menu with --create_new_page_om_call

        #create dictionary to store all the needed widgets in proces stab
        self.process_wids_dict ={'ConfigureFrame':'','TableFrame':'','TableCanvas':'','TableScrollBar':'',
                                 'ClusetrLabel':'','ClusterOptionmenu':"",'ClusterOptionmenuVar':'' ,
                                 'NewClusterLbel':'','NewClusterEntry':'','NewClusterSaveButton':'','NewClusterCancelButton':'',
                                 'ProcessLabel':'','ProcessOptionmenu':'', 'ProcessOptionmenuVar':'',
                                 'NewProcessLabel':'','NewProcessEntry':'','NewProcessSaveButton':'','NewProcessCancelButton':'',
                                 'PageLabel':'','PageOptionmenu':'', 'PageOptionmenuVar':'',
                                 'NewPageLabel':'','NewPageEntry':'','NewPageSaveButton':'','NewPageCancelButton':'',
                                 'PageIndexLabel':'','PageIndexSpinbox':'','PageIndexVar':'',
                                 'StepButton':'','AddButton':'','SaveButton':'','DeleteButton':'','RunButton':''}

        self.process_table_var_dict = {}  # store the variable of the table by rows ex: {1:{'handle':xx,'Action'
        self.process_table_val_dict = {}  # store the variable of the table by rows ex: {1:{'handle':xx,'Action'

        # store all the variable releated to a process in dict. From this value can be obtained to update the database
        self.process_var_dict = {'Cluster': self.process_wids_dict['ClusterOptionmenuVar'],
                                 'Process': self.process_wids_dict['ProcessOptionmenuVar'],
                                 'Page': self.process_wids_dict['PageOptionmenuVar'],
                                 'PageIndex': self.process_wids_dict['PageIndexVar'],
                                 'Table': self.process_table_var_dict, 'Output': ''}

        # store all the values to a process in dict. this dictonary can be used to
        self.process_val_dict = {'Cluster': '',
                                 'Process': '',
                                 'Page': '',
                                 'PageIndex': '',
                                 'Table': '', 'Output': ''}


        #store dictionaries of storein key and values by page .Ex: {'Page1':{'outputname':xx,'storeinkey'}};
        self.storein_output_dict={}

    def process_tab(self,process_studio_process_tab):
        main_frame=Frame(process_studio_process_tab,bg='snow')
        main_frame.place(relx=0.015, rely=0.015, height=650, width=1120)

        fr_config=Frame(main_frame)
        #fr_config.place(relx=0.015,rely=0.015,relheight=0.2,relwidth=0.97)
        fr_config.place(relx=0.0001, rely=0.015, relheight=0.17, relwidth=0.99)

        fr_table=Frame(main_frame)
        #fr_table.place(relx=0.015, rely=0.219, relheight=0.75, relwidth=0.97)
        fr_table.place(relx=0.0001, rely=0.195, relheight=0.75, relwidth=0.99)

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

        #update session dictionary for widgets
        self.process_wids_dict['ConfigureFrame']=fr_config
        self.process_wids_dict['TableFrame'] = frame
        self.process_wids_dict['TableCanvas'] = cn_on_fr_table
        self.process_wids_dict['TableScrollBar'] = y_socrollbar



        self.process_tab_config_frame_gui()

    def process_tab_config_frame_gui(self):
        fr_config=self.process_wids_dict['ConfigureFrame']
        fr_table=self.process_wids_dict['TableFrame']

        children_windows = fr_config.winfo_children() # Store all the children widgets of frame confiration frame in a list

        # Destory all the widgets configuration frame
        loop_count=0
        for each in children_windows:
            loop_count+=1
            if loop_count>=1:
                each.destroy()

        #Create lable for cluster
        lb_cluster = Label(fr_config, text="Cluster:", font=("Arial Bold", 10))
        lb_cluster.place(relx=0.018, rely=0.13, relwidth=0.07)
        self.process_wids_dict['ClusetrLabel']=lb_cluster

        # Create option menu for cluster
        var_cluster = StringVar() #Create string variable to store the selected cluster value
        if self.cluster_om_var_val.strip() == "Create New Cluster": # Check whether the selected cluster value is ""Create New Cluster". note:self.cluster_om_var_val hold the selected cluster value
            var_cluster.set("") # Set cluster as empty
        else:
            var_cluster.set(self.cluster_om_var_val) # Set cluster as per the value selected
        choices_cluster = self.db.retrive_clusters()
        #var_cluster.set(cluster_val)
        om_cluster = OptionMenu(fr_config, var_cluster, *choices_cluster)
        om_cluster.place(relx=0.1, rely=0.085, relwidth=0.2)
        om_cluster.configure(bg='Snow')
        self.process_wids_dict['ClusterOptionmenu'] = om_cluster
        self.process_wids_dict['ClusterOptionmenuVar'] = var_cluster

        def create_new_cluster_om_call(*args): self.create_new_cluster_om_call( )
        var_cluster.trace("w", create_new_cluster_om_call)

        lb_process = Label(fr_config, text="Process:", font=("Arial Bold", 10))
        lb_process.place(relx=0.33, rely=0.13, relwidth=0.07)
        self.process_wids_dict['ProcessLabel'] = lb_process

        var_process = StringVar()
        if self.process_om_var_val.strip() == "Create New Process":
            var_process.set("")
        else:
            var_process.set(self.process_om_var_val)

        choices_process =self.db.retrive_process(var_cluster.get())
        om_process = OptionMenu(fr_config, var_process, *choices_process)
        om_process.configure(bg='Snow')
        om_process.place(relx=0.43, rely=0.085, relwidth=0.2)
        self.process_wids_dict['ProcessOptionmenu'] = om_process
        self.process_wids_dict['ProcessOptionmenuVar'] = var_process

        def create_new_process_om_call(*args): self.create_new_process_om_call()
        var_process.trace("w", create_new_process_om_call)

        lb_page = Label(fr_config, text="Page:", font=("Arial Bold", 10))
        lb_page.place(relx=0.66, rely=0.13, relwidth=0.07)
        self.process_wids_dict['PageLabel'] = lb_page

        var_page = StringVar()
        if self.page_om_var_val.strip() == "Create New Page":
            var_page.set("")
        else:
            var_page.set(self.page_om_var_val)

        choices_page = self.db.retrive_process_page(var_process.get())
        om_page = OptionMenu(fr_config, var_page, *choices_page)
        om_page.configure(bg='Snow')
        om_page.place(relx=0.76, rely=0.085, relwidth=0.2)
        self.process_wids_dict['PageOptionmenu'] = om_page
        self.process_wids_dict['PageOptionmenuVar'] = var_page

        def create_new_page_om_call(*args): self.create_new_page_om_call()
        var_page.trace("w", create_new_page_om_call)

        #def update_output_tab_on_page_change(*args): self.update_output_tab_on_page_change()
        #var_page.trace("w", update_output_tab_on_page_change)


        bt_step = Button(fr_config, text="Step", font=("Arial Bold", 10), command=lambda f : self.step_button_call())
        bt_step.place(relx=0.0, rely=0.76, relwidth=0.04)
        self.process_wids_dict['StepButton'] = bt_step

        bt_run = Button(fr_config, text="Run", font=("Arial Bold", 10),command= lambda : self.run_button_call())
        bt_run.place(relx=0.04, rely=0.76, relwidth=0.04)
        self.process_wids_dict['RunButton'] = bt_step

        bt_refresh = Button(fr_config, text="Refresh", font=("Arial Bold", 10), command=lambda: self.refresh_button_call())
        bt_refresh.place(relx=0.12, rely=0.76, relwidth=0.05)
        self.process_wids_dict['RefreshButton'] = bt_refresh


        bt_add_row = Button(fr_config, text="Add",command=lambda  : self.add_row_button_call(), font=("Arial Bold", 10))
        bt_add_row.place(relx=0.92, rely=0.76, relwidth=0.04)
        self.process_wids_dict['AddButton'] = bt_add_row

        bt_del_row = Button(fr_config, text="Del", font=("Arial Bold", 10),command=lambda  : self.del_row_button_call())
        bt_del_row.place(relx=0.96, rely=0.76, relwidth=0.04)
        self.process_wids_dict['AddButton'] = bt_add_row


        lb_new_page = Label(fr_config, text="Page Index:",font=("Arial Bold", 10),anchor="w")
        lb_new_page.place(relx=0.66, rely=0.35, relwidth=0.07)
        self.process_wids_dict['NewPageLabel'] = lb_new_page

        #et_new_page = Entry(fr_config)
        #et_new_page.place(relx=0.76, rely=0.37, relwidth=0.2)

        var_page_index=IntVar()
        sb_index = Spinbox(fr_config, from_=1, to=500,validate="all",textvariable=var_page_index)
        sb_index.place(relx=0.76, rely=0.37, width=40)
        def trace_page_index(*args): self.trace_page_index()
        var_page_index.trace("w", trace_page_index)
        self.process_wids_dict['PageIndexVar'] = var_page_index

        # Create save button to create/update the document in database
        bt_save = Button(fr_config, text="Save", font=("Arial Bold", 10), command=lambda : self.save_document_button_call())
        bt_save.place(relx=0.08, rely=0.76, relwidth=0.04)
        self.process_wids_dict['SaveButton'] = bt_save

        #def retrive_page(*args):self.retrive_page_doc()
        #var_page.trace("w", retrive_page)

    #**
    def create_new_cluster_om_call(self):
        # drive widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']

        cluster_val=cluster_var.get()

        print("cluster value in --create_new_cluster_om_call:  ", self.cluster_om_var_val)

        #ask question whether user want to create cluster
        if cluster_val!="" and  cluster_val.strip() != "Create New Cluster":
            MsgBox = messagebox.askquestion('Warning', 'Are you sure you want to exit from current cluster? Unsaved values will be lost!',
                                            icon='warning', parent=fr_config)
            if MsgBox == 'no':
                cluster_var.set(self.cluster_om_var_val)
                return

        self.cluster_om_var_val=cluster_val

        #delete all widgets in table frame
        children_windows_fr_tbl = fr_table.winfo_children()
        for each in children_windows_fr_tbl:
            each.destroy()

        var_value=cluster_var.get()# store  cluster value

        # perform below activity if the cluster value value is Create New Cluster
        if var_value=="Create New Cluster":
            # delete all the widgets in configuration frame except to cluster label and cluster option menu
            self.destory_widgets_for_new_cluster_call()

            #label for new cluster
            lb_new_cluster=Label(fr_config,text="New Cluster:")
            lb_new_cluster.place(relx=0.018,rely=0.35,relwidth=0.07)

            # entry for new cluster
            et_new_cluster=Entry(fr_config)
            et_new_cluster.place(relx=0.1, rely=0.37,relwidth=0.2)

            # save button for new cluster
            bt_new_cluster_save = Button(fr_config, text="Save",command=lambda  :self.cluster_save_button_call())
            bt_new_cluster_save.place(relx=0.1, rely=0.58, relwidth=0.07)

            #cancel button for new cluster
            bt_new_cluster_cancel = Button(fr_config, text="Cancel",command=lambda  :self.process_tab_config_frame_gui())
            bt_new_cluster_cancel.place(relx=0.18, rely=0.58, relwidth=0.07)

            # store widgets in instance dictionary
            self.process_wids_dict['NewClusterLbel'] = lb_new_cluster
            self.process_wids_dict['NewClusterEntry'] = et_new_cluster
            self.process_wids_dict['NewClusterSaveButton'] = bt_new_cluster_save
            self.process_wids_dict['NewClusterCancelButton'] = bt_new_cluster_cancel
        else:
            self.process_tab_config_frame_gui()

    #**
    def destory_widgets_for_new_cluster_call(self):

        fr_config = self.process_wids_dict['ConfigureFrame']
        children_windows = fr_config.winfo_children() #store all the widgets from configuration frame into a list

        #delete all the widgets in configuration frame except to cluster label and cluster option menu
        loop_count = 0
        for each in children_windows:
            loop_count += 1
            if loop_count > 2: # because first two widgets in configuration frame are cluster label and cluster option menu
                each.destroy()


        # update dictionary for session widgets
        self.process_wids_dict['NewClusterLbel'] = ''
        self.process_wids_dict['NewClusterEntry'] = ''
        self.process_wids_dict['NewClusterSaveButton'] = ''
        self.process_wids_dict['NewClusterCancelButton'] = ''
        self.process_wids_dict['ProcessLabel']=''
        self.process_wids_dict['ProcessOptionmenu'] = ''
        self.process_wids_dict['ProcessOptionmenuVar'] = ''
        self.process_wids_dict['NewProcessLabel'] = ''
        self.process_wids_dict['NewProcessEntry'] = ''
        self.process_wids_dict['NewProcessSaveButton'] = ''
        self.process_wids_dict['NewProcessCancelButton'] = ''
        self.process_wids_dict['PageLabel'] = ''
        self.process_wids_dict['PageOptionmenu'] = ''
        self.process_wids_dict['PageOptionmenuVar'] = ''
        self.process_wids_dict['NewPageLabel'] = ''
        self.process_wids_dict['NewPageEntry'] = ''
        self.process_wids_dict['NewPageSaveButton'] = ''
        self.process_wids_dict['NewPageCancelButton'] = ''
        self.process_wids_dict['PageIndexLabel'] = ''
        self.process_wids_dict['PageIndexSpinbox'] = ''
        self.process_wids_dict['PageIndexVar'] = ''
        self.process_wids_dict['StepButton'] = ''
        self.process_wids_dict['AddButton'] = ''
        self.process_wids_dict['SaveButton'] = ''
        self.process_wids_dict['DeleteButton'] = ''
        self.process_wids_dict['RunButton'] = ''


    def create_new_process_om_call(self):

        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']

        #store cluster and process value
        cluster_val=cluster_var.get()
        process_val=process_var.get()

        # check value selected in cluster and show message if not selected
        if cluster_val=="" or cluster_val=='Create New Cluster':
            messagebox.showerror("Error","Slelect Cluster Before Process..",parent=fr_config)
            process_var.set("")
            return

        #ask for users confirmation to change the value for process
        if process_val != "" and process_val != "Create New Process":
            MsgBox = messagebox.askquestion('Warning', 'Are you sure you want to exit from current process? Unsaved values will be lost!',
                                            icon='warning', parent=fr_config)
            if MsgBox == 'no':
                process_var.set(self.process_om_var_val) # if no slected, reinstate the process value as previous value
                return

        self.process_om_var_val = process_var.get()

        #destory all the widgets in table frame
        children_windows_fr_tbl = fr_table.winfo_children()
        for each in children_windows_fr_tbl:
            each.destroy()

        if process_val=="Create New Process":
            self.destory_widgets_for_new_process_call()

            # new process label
            lb_new_process=Label(fr_config,text="New Process")
            lb_new_process.place(relx=0.33, rely=0.35, relwidth=0.07)

            # entry for new page
            et_new_process=Entry(fr_config)
            et_new_process.place(relx=0.43, rely=0.37,relwidth=0.2)

            #button for new process save
            bt_new_process_save = Button(fr_config, text="Save",command=lambda :self.process_save_button_call())
            bt_new_process_save.place(relx=0.43, rely=0.58, relwidth=0.07)

            # button new process cancel
            bt_new_process_cancel = Button(fr_config, text="Cancel",command=lambda :self.process_tab_config_frame_gui())
            bt_new_process_cancel.place(relx=0.52, rely=0.58, relwidth=0.07)

            # store widgets in instance dictionary
            self.process_wids_dict['NewProcessLabel'] = lb_new_process
            self.process_wids_dict['NewProcessEntry'] = et_new_process
            self.process_wids_dict['NewProcessSaveButton'] = bt_new_process_save
            self.process_wids_dict['NewProcessCancelButton'] = bt_new_process_cancel

        else:
            self.process_tab_config_frame_gui()

    # **
    def destory_widgets_for_new_process_call(self):

        fr_config = self.process_wids_dict['ConfigureFrame']
        children_windows = fr_config.winfo_children()  # store all the widgets from configuration frame into a list

        # delete all the widgets in configuration frame except to cluster label and cluster option menu
        loop_count = 0
        for each in children_windows:
            loop_count += 1
            # because first four widgets in configuration frame are cluster label and cluster option menu,process labe and process option menu
            if loop_count > 4:
                each.destroy()

        # update dictionary for session widgets
        self.process_wids_dict['NewClusterLbel'] = ''
        self.process_wids_dict['NewClusterEntry'] = ''
        self.process_wids_dict['NewClusterSaveButton'] = ''
        self.process_wids_dict['NewClusterCancelButton'] = ''
        self.process_wids_dict['NewProcessLabel'] = ''
        self.process_wids_dict['NewProcessEntry'] = ''
        self.process_wids_dict['NewProcessSaveButton'] = ''
        self.process_wids_dict['NewProcessCancelButton'] = ''
        self.process_wids_dict['PageLabel'] = ''
        self.process_wids_dict['PageOptionmenu'] = ''
        self.process_wids_dict['PageOptionmenuVar'] = ''
        self.process_wids_dict['NewPageLabel'] = ''
        self.process_wids_dict['NewPageEntry'] = ''
        self.process_wids_dict['NewPageSaveButton'] = ''
        self.process_wids_dict['NewPageCancelButton'] = ''
        self.process_wids_dict['PageIndexLabel'] = ''
        self.process_wids_dict['PageIndexSpinbox'] = ''
        self.process_wids_dict['PageIndexVar'] = ''
        self.process_wids_dict['StepButton'] = ''
        self.process_wids_dict['AddButton'] = ''
        self.process_wids_dict['SaveButton'] = ''
        self.process_wids_dict['DeleteButton'] = ''
        self.process_wids_dict['RunButton'] = ''


    #**
    def create_new_page_om_call(self):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']
        page_var= self.process_wids_dict['PageOptionmenuVar']

        page_val=page_var.get()

        # ensure process is selected before page
        if process_var.get()=="" or process_var.get()=="Create New Process":
            messagebox.showerror("Error","Slelect Process Before Page..",parent=fr_config)
            page_var.set("")
            return

        print('self.page_om_var_val: ',self.page_om_var_val)
        if self.page_om_var_val != "" and self.page_om_var_val != "Create New Page":
            MsgBox = messagebox.askquestion('Warning',
                                            'Are you sure you want to exit from current page? Unsaved values will be lost!',
                                            icon='warning', parent=fr_config)
            if MsgBox == 'no':
                page_var.set(self.page_om_var_val)
                return

        # destory all the widgets in table frame
        children_windows_fr_tbl = fr_table.winfo_children()
        for each in children_windows_fr_tbl:
            each.destroy()

        self.page_om_var_val = page_val
        children_windows=fr_config.winfo_children()
        if page_val=="Create New Page":
            self.destory_widgets_for_new_page_call()

            #new page label
            lb_new_page=Label(fr_config,text="New Page")
            lb_new_page.place(relx=0.66, rely=0.35, relwidth=0.07)

            #new page entry
            et_new_page=Entry(fr_config)
            et_new_page.place(relx=0.76, rely=0.37,relwidth=0.2)

            #new process save button
            bt_new_process_save = Button(fr_config, text="Save",command=lambda  :self.new_page_save_button_call())
            bt_new_process_save.place(relx=0.76, rely=0.58, relwidth=0.07 )

            #new process cancel button
            bt_new_process_cancel = Button(fr_config, text="Cancel", command=lambda :self.process_tab_config_frame_gui())
            bt_new_process_cancel.place(relx=0.85, rely=0.58, relwidth=0.07)

            # store widgets in instance dictionary
            self.process_wids_dict['NewPageLabel'] = lb_new_page
            self.process_wids_dict['NewPageEntry'] = et_new_page
            self.process_wids_dict['NewPageSaveButton'] = bt_new_process_save
            self.process_wids_dict['NewPageCancelButton'] = bt_new_process_cancel

        else:
            self.var_table=[]
            self.retrive_page_doc()
            # var_value = var.get()
            #self.process_tab_config_frame_gui()
            storein_dict = {}

        print("variables list for the widgets added in process table in --create_new_page_om_call: ", self.var_table)

    # **
    def destory_widgets_for_new_page_call(self):

        fr_config = self.process_wids_dict['ConfigureFrame']
        children_windows = fr_config.winfo_children()  # store all the widgets from configuration frame into a list

        # delete all the widgets in configuration frame except to cluster label and cluster option menu
        loop_count = 0
        for each in children_windows:
            loop_count += 1
            # because first six widgets in configuration frame are cluster label and cluster option menu,process labe and process option menu
            if loop_count > 6:
                each.destroy()

        # update dictionary for session widgets
        self.process_wids_dict['NewClusterLbel'] = ''
        self.process_wids_dict['NewClusterEntry'] = ''
        self.process_wids_dict['NewClusterSaveButton'] = ''
        self.process_wids_dict['NewClusterCancelButton'] = ''
        self.process_wids_dict['NewProcessLabel'] = ''
        self.process_wids_dict['NewProcessEntry'] = ''
        self.process_wids_dict['NewProcessSaveButton'] = ''
        self.process_wids_dict['NewProcessCancelButton'] = ''
        self.process_wids_dict['NewPageLabel'] = ''
        self.process_wids_dict['NewPageEntry'] = ''
        self.process_wids_dict['NewPageSaveButton'] = ''
        self.process_wids_dict['NewPageCancelButton'] = ''
        self.process_wids_dict['PageIndexLabel'] = ''
        self.process_wids_dict['PageIndexSpinbox'] = ''
        self.process_wids_dict['PageIndexVar'] = ''
        self.process_wids_dict['StepButton'] = ''
        self.process_wids_dict['AddButton'] = ''
        self.process_wids_dict['SaveButton'] = ''
        self.process_wids_dict['DeleteButton'] = ''
        self.process_wids_dict['RunButton'] = ''

    # **
    def cluster_save_button_call(self):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        new_cluster_entry = self.process_wids_dict['NewClusterEntry']

        self.cluster_om_var_val = cluster_var.get() # set the cluster value in instance variable
        clusters = self.db.retrive_clusters() #retrive all the clusters
        new_cluster_value=new_cluster_entry.get() # get the value for new cluster from new cluster entry box


        #check if the cluster already exists and if not exist perform the below activity
        if new_cluster_value not in clusters:
            result,message=self.db.create_new_process_page_in_primary_databse(type='process',cluster=new_cluster_value,process='#NA',
                                                               page='#NA',pageindex=1,table="#NA",output="#NA")

            if result=='Error':
                messagebox.showerror(result,message,parent=fr_config)
            else:
                messagebox.showinfo(result, message, parent=fr_config)
                cluster_var.set(new_cluster_value)
                self.cluster_om_var_val = cluster_var.get()
                #self.process_wids_dict['ClusterOptionmenuVar']=cluster_var.get()

        #IF THE CLUSTER ALREADY EXIST, SHOW THE BELOW MESSAGE
        else:
            messagebox.showerror("Error",'Cluster Already Exists',parent=fr_config)
            new_cluster_entry.delete(0,END)

    # **
    def process_save_button_call(self):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']
        new_process_entry = self.process_wids_dict['NewProcessEntry']


        self.process_om_var_val=process_var.get() # set instance variabel for process value as current process value
        cluster_val=cluster_var.get() #get cluster value
        process = self.db.retrive_process(cluster_val) #retrive all processes

        new_process_value=new_process_entry.get() #get new process value

        # check if the process already exists and if not exist perform the below activity
        if new_process_value not in process:
            result, message = self.db.create_new_process_page_in_primary_databse(type='process',
                                                                                 cluster=cluster_val,
                                                                                 process=new_process_value,
                                                                                 page='#NA', pageindex=1, table="#NA",
                                                                                 output="#NA")

            if result == 'Error':
                messagebox.showerror(result, message, parent=fr_config)
            else:
                messagebox.showinfo(result, message, parent=fr_config)
                process_var.set(new_process_value)
                self.process_om_var_val = new_process_value
        # IF THE CLUSTER ALREADY EXIST, SHOW THE BELOW MESSAGE
        else:
            messagebox.showerror("Error",'Process Already Exists',parent=fr_config)
            new_process_entry.delete(0,END)

    # **
    def new_page_save_button_call(self):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']
        new_process_entry = self.process_wids_dict['NewProcessEntry']
        page_var = self.process_wids_dict['PageOptionmenuVar']
        new_page_entry = self.process_wids_dict['NewPageEntry']


        self.page_om_var_val = page_var.get() #set the instance variable for page with current page value
        val_var_process=process_var.get() #store process value
        val_var_cluster=cluster_var.get() #store cluster value
        page = self.db.retrive_process_page(val_var_process) #retrive all the pages
        print('pages: ',page)
        new_page_value=new_page_entry.get() #store the new page value

        # check if the process already exists and if not exist perform the below activity
        if new_page_value not in page:
            result, message = self.db.create_new_process_page_in_primary_databse(type='process',
                                                                                 cluster=val_var_cluster,
                                                                                 process=val_var_process,
                                                                                 page=new_page_value, pageindex=1, table="#NA",
                                                                                 output="#NA")

            if result == 'Error':
                messagebox.showerror(result, message, parent=fr_config)
            else:
                messagebox.showinfo(result, message, parent=fr_config)
                page_var.set(new_page_value)
                self.page_om_var_val = new_page_value
        # IF THE CLUSTER ALREADY EXIST, SHOW THE BELOW MESSAGE
        else:
            messagebox.showerror("Error",'Page Already Exists',parent=fr_config)
            new_page_entry.delete(0,END)

    #**
    def refresh_button_call(self):
        process=self.process_wids_dict['ProcessOptionmenuVar'].get() #store the process name
        children_windows=self.outputtab_table_frame.winfo_children() #children widgets from output tab table frame
        loop_count=0
        active_row=True
        row=1
        table_dict={}
        #loop all the widgets in output tab table frame and add ther rows in self.storein_output_dict
        for each in children_windows:
            if active_row==True:
                table_dict[row] = {'Key':children_windows[loop_count+1].get(),'Value':children_windows[loop_count+2].get()}

            #active_row=True if loop_count%2==0 else False
            loop_count+=1

            if loop_count !=0 and loop_count % 4 == 0:
                active_row = True
                row+=1
            else:
                active_row = False

        self.storein_output_dict={'Process':process,'Table':table_dict} # create dictionary for run time output dictionary

        global storein_output_dict
        storein_output_dict=self.storein_output_dict

        #create dictionary of all the values from process table
        print("self.process_table_var_dict in refresh button call: ",self.process_table_var_dict)
        self.process_table_val_dict={}
        for each_row in self.process_table_var_dict:
            print('rows in process_table_var_dict with refresh button call: ',each_row)
            self.process_table_val_dict[each_row]={'Handle': self.process_table_var_dict[each_row]['Handle'].get(),
                                              'Action': self.process_table_var_dict[each_row]['Action'].get(),
                                              'Input': self.process_table_var_dict[each_row]['Input'].get(),
                                              'Output': self.process_table_var_dict[each_row]['Output'].get(),
                                              'Exception': self.process_table_var_dict[each_row]['Exception'].get(),
                                              'RowSelect': self.process_table_var_dict[each_row]['RowSelect'].get()}

        # create final dictionary wich can be used to update in database

        self.process_val_dict = {'Cluster': self.process_wids_dict['ClusterOptionmenuVar'].get(),
                                 'Process': self.process_wids_dict['ProcessOptionmenuVar'].get(),
                                 'Page': self.process_wids_dict['PageOptionmenuVar'].get(),
                                 'PageIndex': self.process_wids_dict['PageIndexVar'].get(),
                                 'Table': self.process_table_val_dict, 'Output': self.storein_output_dict}

        print("Final page dictionary with refresh call: ", self.process_val_dict)
        return self.process_val_dict


            # **

    def add_row_button_call(self):

        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        y_socrollbar = self.process_wids_dict['TableScrollBar']
        cn_on_fr_table = self.process_wids_dict['TableCanvas']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']

        process_val = process_var.get()
        if process_val == '' or process_val == "Create New Process":
            messagebox.showerror('Error', 'Select Process Before Adding Row', parent=fr_config)
            return

        fr_table.update_idletasks()  # update table if any widgets it stuck

        children_windows = fr_table.winfo_children()  # store the children widgets from table frame
        rows_tableframe = (len(
            children_windows)) / 7  # store the number of rows in table frame (each widgets consist of 7 widgets

        # whenever checkbutton is checked, instance dictionary-check_button_dict will be updated with rows and its value
        def get_checkbutton_value(cb, var):
            val = var.get()
            row = cb.grid_info()['row']
            # row += 1
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

            # print('action list\n',actions_list)

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
        checked = False
        checked_row = ''
        for each in self.check_button_dict:
            if self.check_button_dict[each] == 1:
                checked = True
                checked_row = each

        # perform below activity if any row is checked
        if checked == False:
            next_row = 1

            #  derive the next row considering current rumber of rows
            if rows_tableframe >= 1: next_row = int(rows_tableframe) + 1

            # create sequential label
            lb_input = Label(fr_table, text=next_row, fg='black', underline=1, width=3, relief=FLAT)
            lb_input.grid(row=next_row, column=1)
            # self.process_table_var_dict['row']=next_row

            # create handle OptionMenu
            tem_var_list = []
            var_handler1 = StringVar()
            chocices_handler = self.db.retrive_all_handles()
            om_handler1 = OptionMenu(fr_table, var_handler1, *chocices_handler)
            om_handler1.config(width=38, bg='snow')
            om_handler1.grid(row=next_row, column=2)
            tem_var_list.append(var_handler1)

            # create action OptionMenu
            var_action1 = StringVar()
            chocices_action = ['Dummy']
            om_action1 = OptionMenu(fr_table, var_action1, *chocices_action)
            om_action1.config(width=38, bg='snow')
            om_action1.grid(row=next_row, column=3)
            tem_var_list.append(var_action1)

            # create input label
            var_input1, var_input_name, var_input_value = StringVar(), list(), list()
            var_input1.set('Input')
            lb_input1 = Label(fr_table, text='Input', fg='blue', underline=1, width=24, relief=FLAT,
                              textvariable=var_input1)
            lb_input1.grid(row=next_row, column=4)
            lb_input1.bind('<Button-1>',lambda x, row=next_row: self.process_input_window(row))

            tem_var_list.append(var_input1)

            # create output label
            var_output1 = StringVar()
            var_output1.set('Output')
            lb_output = Label(fr_table, text='Output', fg='blue', underline=1, width=25, relief=FLAT,
                              textvariable=var_output1)
            lb_output.grid(row=next_row, column=5)
            lb_output.bind('<Button-1>',lambda x,row=next_row: self.process_output_window(row))
            tem_var_list.append(var_output1)

            # create exception label
            var_exception1 = StringVar()
            lb_exception_handle = Label(fr_table, text='Exception Handle', fg='blue', underline=1, width=18,
                                        relief=FLAT, textvariable=var_exception1)
            lb_exception_handle.grid(row=next_row, column=6)
            tem_var_list.append(var_exception1)
            self.var_table.append(tem_var_list)

            # create CheckButton
            var_row_select = IntVar()
            cbt_tbl = Checkbutton(fr_table, text="", variable=var_row_select, onvalue=1, offvalue=0, width=2)
            cbt_tbl.configure(command=lambda cb=cbt_tbl, var=var_row_select: get_checkbutton_value(cb, var))
            cbt_tbl.grid(row=next_row, column=7)

            self.process_table_var_dict[next_row] = {'Handle': var_handler1, 'Action': var_action1,
                                                     'Input': var_input1, 'Output': var_output1,
                                                     'Exception': var_exception1, 'RowSelect': var_row_select}

            # configure scrollbar
            cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
            y_socrollbar.config(command=cn_on_fr_table.yview)
            y_socrollbar.pack(side=RIGHT, fill=Y)

            # trace handler varibale
            var_handler1.trace('w',
                               lambda x, y, z: refresh_handle_om(om_action1, var_action1, var_handler1, var_input1,
                                                                 var_output1,
                                                                 lb_input1))

            # print('var table:\n',self.var_table)

        # preform the below activity if checked
        if checked == True:
            # read all the rows and store in var_value list
           # self.var_table = []
            var_values=[]
            loop_count = 0
            for each_row in self.var_table:
                loop_count += 1
                var_value_temp = []
                var_value_temp.append((each_row[0]).get())
                var_value_temp.append((each_row[1]).get())
                var_value_temp.append((each_row[2]).get())
                var_value_temp.append((each_row[3]).get())
                var_value_temp.append((each_row[4]).get())
                var_values.append(var_value_temp)

                if loop_count == checked_row:
                    var_value_temp = []
                    var_value_temp.append('')
                    var_value_temp.append('')
                    var_value_temp.append('Input')
                    var_value_temp.append('Output')
                    var_value_temp.append('Exception Handle')
                    var_values.append(var_value_temp)
            print('var_values\n', var_values)

            self.var_table = []  # store variables of the row as list
            self.process_table_var_dict = {}  # store variables of the row by rows

            # destory all the widgets in table
            for each in children_windows:
                each.destroy()

            # place the widgets for var_values
            loop_count = 0
            next_row = 0
            for each in var_values:
                loop_count += 1
                next_row += 1

                # create label for sequence
                lb_input = Label(fr_table, text=loop_count, fg='black', underline=1, width=3, relief=FLAT)
                lb_input.grid(row=next_row, column=1)

                # create OptionMenu for handler
                tem_var_list = []
                var_handler = StringVar()
                var_handler.set(each[0])
                chocices_handler = self.db.retrive_all_handles()
                om_handler = OptionMenu(fr_table, var_handler, *chocices_handler)
                om_handler.config(width=38, bg='snow')
                om_handler.grid(row=next_row, column=2)
                tem_var_list.append(var_handler)

                # create OptionMenu for action
                var_action = StringVar()
                var_action.set(each[1])
                chocices_action = ['Dummy']
                om_action = OptionMenu(fr_table, var_action, *chocices_action)
                om_action.config(width=38, bg='snow')
                om_action.grid(row=next_row, column=3)
                # self.var_table.append(var_action)
                tem_var_list.append(var_action)
                # print('om_action: ',om_action )

                # create label for input
                var_input, var_input_name, var_input_value = StringVar(), list(), list()
                var_input.set(each[2])
                lb_input = Label(fr_table, text='Input', fg='blue', underline=1, width=24, relief=FLAT,
                                 textvariable=var_input)
                lb_input.grid(row=next_row, column=4)
                lb_input.bind('<Button-1>',lambda x, row=next_row: self.process_input_window(row))

                tem_var_list.append(var_input)

                # create label for output
                var_output = StringVar()
                var_output.set(each[3])
                lb_output = Label(fr_table, text='Output', fg='blue', underline=1, width=25, relief=FLAT,
                                  textvariable=var_output)
                lb_output.grid(row=next_row, column=5)
                lb_output.bind('<Button-1>', lambda x, row=next_row: self.process_output_window(row))

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

                # store variables of the row by rows
                self.process_table_var_dict[next_row] = {'Handle': var_handler, 'Action': var_action,
                                                         'Input': var_input, 'Output': var_output,
                                                         'Exception': var_exception, 'RowSelect': var_row_select}

                # configure scrollbar
                cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
                y_socrollbar.config(command=cn_on_fr_table.yview)
                y_socrollbar.pack(side=RIGHT, fill=Y)

                # trace handler
                var_handler.trace_variable('w', lambda m, n, o, x=om_action, y=var_action, z=var_handler, a=var_input,
                                                       b=var_output, c=lb_input: refresh_handle_om(x, y, z, a, b, c))

        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0

        print('var table:\n', self.var_table)
        print('var table dictionary:\n', self.process_table_var_dict)
        print('var process dictionary:\n', self.process_var_dict)


    # **
    def del_row_button_call(self):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        y_socrollbar = self.process_wids_dict['TableScrollBar']
        cn_on_fr_table = self.process_wids_dict['TableCanvas']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']

        children_windows = fr_table.winfo_children()
        rows_tableframe = (len(children_windows)) / 7

        # whenever checkbutton is checked, instance dictionary-check_button_dict will be updated with rows and its value
        def get_checkbutton_value(cb, var):
            val = var.get()
            row = cb.grid_info()['row']
            # row += 1
            self.check_button_dict[row] = val
            # print(self.check_button_dict)

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
        checked = False
        checked_row = ''
        for each in self.check_button_dict:
            if self.check_button_dict[each] == 1:
                checked = True
                checked_row = each

        # perform the bewlo activity if any row is checked
        if checked == True:
            var_values = []
            loop_count = 0

            # read all the rows except to the row checked
            for each_row in self.var_table:
                loop_count += 1
                if loop_count == checked_row:
                    continue
                else:
                    var_value_temp = []
                    var_value_temp.append((each_row[0]).get())
                    var_value_temp.append((each_row[1]).get())
                    var_value_temp.append((each_row[2]).get())
                    var_value_temp.append((each_row[3]).get())
                    var_value_temp.append((each_row[4]).get())
                    var_values.append(var_value_temp)

            # print('var_values\n',var_values)

            self.var_table = []
            self.process_table_var_dict = {}

            # destory all the widgets in the table
            for each in children_windows:
                each.destroy()

            # place all the widgets for the values read in var_vales
            loop_count = 0
            next_row = 0
            for each in var_values:
                loop_count += 1
                next_row += 1

                lb_input = Label(fr_table, text=loop_count, fg='blue', underline=1, width=3, relief=FLAT)
                lb_input.grid(row=next_row, column=1)

                tem_var_list = []
                var_handler = StringVar()
                var_handler.set(each[0])
                chocices_handler = self.db.retrive_all_handles()
                om_handler = OptionMenu(fr_table, var_handler, *chocices_handler)
                om_handler.config(width=38)
                om_handler.grid(row=next_row, column=2)
                tem_var_list.append(var_handler)

                var_action = StringVar()
                var_action.set(each[1])
                chocices_action = ['Dummy']
                om_action = OptionMenu(fr_table, var_action, *chocices_action)
                om_action.config(width=38)
                om_action.grid(row=next_row, column=3)
                # self.var_table.append(var_action)
                tem_var_list.append(var_action)
                print('om_action: ', om_action)

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

                # store variables of the row by rows
                self.process_table_var_dict[next_row] = {'Handle': var_handler, 'Action': var_action,
                                                         'Input': var_input, 'Output': var_output,
                                                         'Exception': var_exception, 'RowSelect': var_row_select}

                cn_on_fr_table.config(scrollregion=cn_on_fr_table.bbox('all'), yscrollcommand=y_socrollbar.set)
                y_socrollbar.config(command=cn_on_fr_table.yview)
                y_socrollbar.pack(side=RIGHT, fill=Y)

                var_handler.trace_variable('w', lambda m, n, o, x=om_action, y=var_action, z=var_handler, a=var_input,
                                                       b=var_output, c=lb_input: refresh_handle_om(x, y, z, a, b, c))
                # print('var table:\n', self.var_table)

        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0

        print('process_table_var_dict in delete table button call : ', self.process_table_var_dict)

    def process_input_window(self,row):

        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        y_socrollbar = self.process_wids_dict['TableScrollBar']
        cn_on_fr_table = self.process_wids_dict['TableCanvas']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']

        ''''#derive widgets in output tab
        fr_config_output = (self.process_studio_output_tab.winfo_children())[0]
        fr_table_output = (((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[0]
        fr_table_output.update_idletasks()
        y_socrollbar_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0])
        children_windows_tbl_output=fr_table_output.winfo_children()'''

        # create TopLevel window for input
        input_window=Toplevel(self.process_studio_notebook)
        input_window.title('Input')
        input_window.geometry("800x400")

        # create table frame
        fr_input_table=Frame(input_window,bg='snow',highlightthickness=0)
        fr_input_table.place(relx=.025, rely=.025, relwidth=.71, relheight=.9)

        # create listbox for output
        fr_output_var_listbox = Frame(input_window, bg='snow',highlightthickness=0)
        fr_output_var_listbox.place(relx=.75, rely=.1, relwidth=.24, relheight=.75)

        # create optionMenu for variables
        var_output_option=StringVar()
        var_output_option.set('Output Variable')
        choices_output=['Output Variable','Application Moduler Variable','Global Variable']
        om_output_var_options=OptionMenu(input_window,var_output_option,*choices_output)
        om_output_var_options.place(relx=.75, rely=.025, relwidth=.24)

        cn_input_table=Canvas(fr_input_table,highlightthickness=0) # create Canvas on table frame
        sb_input_table=Scrollbar(fr_input_table,orient="vertical",command=cn_input_table.yview) # create Scrollbar on table frame
        fr_cn_input_table=Frame(cn_input_table) # create frame on table Canvas

        # create header table for table frame
        lb_input_name=Label(fr_cn_input_table,text="Input Name", font=("Arial Bold", 10), bg='gray87', width=22,relief=GROOVE).grid(row=1,column=1)
        lb_input_value = Label(fr_cn_input_table, text="Input Value", font=("Arial Bold", 10), bg='gray87', width=43,relief=GROOVE).grid(row=1, column=2)
        lb_input_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=3)


        #row number

        input=(self.process_table_var_dict[row]['Input']).get()
        input=eval(input)

        # place input name and value in window
        r=2
        loop_count=0
        for each in input:
            print('each is : ',each)
            var_input_name=StringVar()
            InputName=(input[each])['InputName']
            #print(InputName)
            var_input_name.set(InputName)
            lb_input_name_vale = Label(fr_cn_input_table, textvariable=var_input_name, font=("Arial", 10), bg='gray87', width=22).grid(row=r, column=1)
            var_ent=StringVar()
            InputValue = (input[each])['InputValue']
            if str(InputValue)=='str()':InputValue==''
            var_ent.set(InputValue)
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
        '''def update_listbox_for_output_variable(*args):
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
                lb_var.delete(0, END)'''

        #update_listbox_for_output_variable() #when open output window first time, update the output variable names in listbox
        #var_output_option.trace_variable('w',update_listbox_for_output_variable) #when the value is select as output variable in OptionMenu, update listbox



        # attach listbox to scrollbar
        lb_var.config(yscrollcommand=sb_variable_listbox.set)
        sb_variable_listbox.config(command=lb_var.yview)

        lb_var.bind('<<ListboxSelect>>', self.lb_onselect) #bind the item listbox to right click

        # place ok button which will update the input label in the table and close the output window
        var=self.process_table_var_dict[row]['Input']
        bt_ok = Button(input_window, text='OK', command=lambda fr=fr_cn_input_table,var=var,win=input_window: self.ok_button_call_input_window(fr,var,win))
        bt_ok.place(relx=.86, rely=.878)

    def ok_button_call_input_window(self, fr, var, win):

        children_windows = fr.winfo_children() #store all widgets in input frame into a list
        input={} #create input dictionary
        loop_count = 0
        row=0
        row_active=False
        for each in children_windows:
            loop_count += 1

            if row_active==True:
                input_name=children_windows[loop_count-1].cget("text")
                input_value = children_windows[loop_count].get()
                #if input_value=='':
                   # input_value='str()'
                input[row]={'InputName':input_name,'InputValue':input_value}

            if  loop_count%3==0:
                row+=1
                row_active=True
            else:
                row_active=False

        var.set(input)
        win.destroy()
        print(input)


    def lb_onselect(self,evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        global input_lb_selected_value
        input_lb_selected_value = (w.get(index))
        print('You selected item %d: "%s"' % (index, input_lb_selected_value))

    def update_input_value_entrybox(self,var_ent):
        print(var_ent)
        var_evt=var_ent.widget
        len_val=(len(var_evt.get()))+2

        #var_evt.delete(0,END)
        text="&" + str(input_lb_selected_value) + "&"
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

    def process_output_window(self,row):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        y_socrollbar = self.process_wids_dict['TableScrollBar']
        cn_on_fr_table = self.process_wids_dict['TableCanvas']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']
        y_socrollbar_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0]).winfo_children()[1]
        cn_on_fr_table_output=(((self.process_studio_output_tab.winfo_children())[1]).winfo_children()[0])
        #children_windows_tbl_output=fr_table_output.winfo_children()


        #print('next row is',next_row)
        #print("in toplevel window")
        output_window=Toplevel(self.process_studio_notebook)
        output_window.title('Output')
        output_window.geometry("800x400")



        fr_output_table=Frame(output_window,bg='snow',highlightthickness=0)
        fr_output_table.place(relx=.025, rely=.025, relwidth=.71, relheight=.9)

        fr_output_var_listbox = Frame(output_window, bg='snow',highlightthickness=0)
        fr_output_var_listbox.place(relx=.75, rely=.1, relwidth=.24, relheight=.75)

        var_output_option=StringVar()
        var_output_option.set('Output Variable')
        choices_output=['Output Variable','Application Moduler Variable','Global Variable']
        om_output_var_options=OptionMenu(output_window,var_output_option,*choices_output)
        om_output_var_options.place(relx=.75, rely=.025, relwidth=.24)



        cn_output_table=Canvas(fr_output_table,highlightthickness=0)
        sb_output_table=Scrollbar(fr_output_table,orient="vertical",command=cn_output_table.yview)

        fr_cn_input_table=Frame(cn_output_table)


        lb_output_name=Label(fr_cn_input_table,text="Output Name", font=("Arial Bold", 10), bg='gray87', width=22,relief=GROOVE).grid(row=1,column=1)
        lb_output_storein = Label(fr_cn_input_table, text="Store In", font=("Arial Bold", 10), bg='gray87', width=18,relief=GROOVE).grid(row=1, column=2)
        #lb_output_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=3)
        lb_output_value = Label(fr_cn_input_table, text="Output Value", font=("Arial Bold", 10), bg='gray87', width=30,relief=GROOVE).grid(row=1, column=3)
        lb_output_validate = Label(fr_cn_input_table, text="", font=("Arial Bold", 10), bg='gray87', width=1,relief=GROOVE).grid(row=1, column=4)

        output = (self.process_table_var_dict[row]['Output']).get()
        output = eval(output)

        r=2
        loop_count=0
        for each in output:
            var_output_name=StringVar()
            var_output_name.set(output[each]['OutputName'])
            lb_input_name_vale = Label(fr_cn_input_table, textvariable=var_output_name, font=("Arial", 10), bg='gray87', width=22).grid(row=r, column=1)

            var_storein = StringVar()
            #var_storein.set(storein[loop_count])
            #var_storein.set(input_value[loop_count])
            if 'StoreIn' in output[each]:
                var_storein.set(output[each]['StoreIn'])
            et_storein = Entry(fr_cn_input_table, width=24, textvariable=var_storein)
            et_storein.bind('<Button-3>', lambda var_ent=var_storein: self.update_input_value_entrybox(var_ent))
            et_storein.grid(row=r, column=2)

            var_ent=StringVar()
            var_ent.set(output[each]['OutputValue'])
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
        '''def update_listbox_for_output_variable(*args):
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
                                         update_listbox_for_output_variable)  # when the value is select as output variable in OptionMenu, update listbox'''

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
        '''lb_var.config(yscrollcommand=sb_variable_listbox.set)
        sb_variable_listbox.config(command=lb_var.yview)

        lb_var.bind('<<ListboxSelect>>', self.lb_onselect)'''
        var = self.process_table_var_dict[row]['Output']
        bt_ok = Button(output_window, text='OK', command=lambda fr=fr_cn_input_table,var=var,win=output_window: self.ok_button_call_output_window(fr,var,win))
        bt_ok.place(relx=.86, rely=.878)

    def ok_button_call_output_window(self, fr, var, win):
        output_name, output_value,storein, output = list(), list(),list(), ''
        children_windows = fr.winfo_children()
        loop_count = 0
        ent_count=0
        children_windows = fr.winfo_children() #store all widgets in input frame into a list
        output={} #create input dictionary
        loop_count = 0
        row=0
        row_active=False
        for each in children_windows:
            loop_count += 1

            if row_active==True:
                output_name=children_windows[loop_count-1].cget("text")
                storein_value = children_windows[loop_count].get()
                output_value = children_windows[loop_count+1].get()
                #if input_value=='':
                   # input_value='str()'
                output[row]={'OutputName':output_name,'StoreIn':storein_value ,'OutputValue':output_value}

            if  loop_count%4==0:
                row+=1
                row_active=True
            else:
                row_active=False


        #for each in children_windows:
            #loop_count += 1
             #print(each.winfo_class)
            '''if each.winfo_class() == 'Label' and loop_count > 4:
                # print(each.cget("text"))
                output_name.append(each.cget("text"))
            if each.winfo_class() == 'Entry':
                ent_count+=1
                if ent_count%2>0:
                    if len(each.get())>0:storein.append(each.get())
                    if len(each.get()) == 0: storein.append('&dummy&')
                if ent_count % 2 == 0:
                    if len(each.get())>0:output_value.append(each.get())
                    if len(each.get()) == 0: output_value.append('str()')'''



        var.set(output)
        win.destroy()
        print(output)

    def step_button_call(self,fr_table):
        print('printing var tabl in step button call: ',self.var_table)

        #Collect all the row values for the rows in table
        var_val=[] #create a list in which all the value for the vars for widgets in table will be stored
        temp_var_val=[] # create a temporary list to store the values in each row
        #loop_count=0
        if len(self.var_table)>0: # if there are rows in table, peform the below activity
            for each_row in self.var_table: # loop throgh each row in table
                temp_var_val = [] # when loop each new row, clear values in tem_var_val list
                for each_val in each_row: # loop in each value in in each row
                    temp_var_val.append(each_val.get()) # append the each value into tem_var_val list
                var_val.append(temp_var_val) #apend the tem_var_val list var_val list
                #loop_count += 1
        print(var_val)

        # find the selected row and find the row the value for the selected row
        row_selected=[] # create list store the selected row
        for each in self.check_button_dict: # loop through check_button_dict which is updated whenever CheckButton in each row is selected
            if self.check_button_dict[each]==1: # Find whether the check button is checked. (Checked -->1 , unchecked-->0)
                row_selected.append(each) # if the check button is checked, take that row into row_selected
        print(' row selected in step button call :', row_selected)
        row_selected.sort()  # sort the selected row numbers in to ascending order
        row=var_val[row_selected[0]-1] # store the values for the row selected into row
        print('row in step button call : ', row)

        handler=row[0] #Extract handlndler detail
        action=row[1] # Extract action detail

        #create list for output, output name , output value and store in variable
        output_list, output_name_list, output_value_list, storein_list = self.format_output(row[3])
        # Crate comma separated outputname string..Ex: o1,o2,o3
        output_name = ''  # Create output name comma separated variable
        loop_count = 1
        for each in output_name_list:
            if each != '' and loop_count > 1: output_name = output_name + ',' + each  # only add if output name is not an empty string and add comma if more bthan one output name found
            if each != '' and loop_count == 1: output_name = each  # #only add if output name is not an empty string
            loop_count += 1


        # create list for input, input name , input value
        input_list, input_name_list, input_value_list = self.format_input(row[2])
        print('printing input_value_list in step button call: ', input_value_list)
        print('printing input_name_list in step button call: ', input_name_list)

        #create a input string
        input='' #Create input variable
        loop_count=0
        for each_name in input_name_list:
            storein_key=""
            if "&" in str(input_value_list[loop_count]): #Find input value consist of & key - which indicate that input value taken from the storein key value
                storein_key=(input_value_list[loop_count]) # Stroe store in key
                # Create input string
                #1. storein dict is updated in runtime
                #2. get the value from storein dict and repplace
                input= "\n\t" + input + "\n\t" + each_name +"=" + str(self.step_button_call_storein_dict[storein_key])

            else:
                #create input string assign it value
                input =  input  + "\n\t" + each_name + "=" + str(input_value_list[loop_count])

            loop_count+=1
        print('printing input in step button call: ', input)



        output = row[3].replace("&","") # replace & in output string
        code=self.db.retrive_code_for_action(handler,action) # retrive code string

        # retrieve and format modules
        module_retrived=self.db.retrive_module_for_handler(handler) # retruive module string
        module_list=module_retrived.split('\n') #create list by splitting "\n"
        module='' # Create module string
        for each in module_list:
            if each!='':
                module =module + '\nimport ' + each # add "import"  infront of each module and create module string
        print(module)

        #create a function with the ablove formatted each string
        #1. Output will be stored in a tupple named as "Outcome"
        function = module + "\n" + "def action():" + str(input) + str(output) + "\n" + code + "\n\t" + "return " + str(output_name) + "\n" + "global outcome" + "\n" + "outcome=action()" + "\n" + "print(outcome)"
        print(function)

        output_dict={} # Create dictionary to store output name and value
        output_formatted=[] # Create a 2D list to store each output..Ex: [['o1', '&a&', 25], ['o2', '&b&', 8515545]]
        output_formatted_temp = []
        try:
            exec(function) # Execute the above function

            print('printing outcome in step button call: ',outcome)
            print('printing output names list in step button call: ', output_name_list)
            loop_count = 0
            for each_name in output_name_list:
                output_formatted_temp = [] # Create a list to store output name storein and value. This list will be appended into output_formatted
                output_dict[each_name]=outcome[loop_count] # From outcome tupple get the value for each output name and add it into output_dict
                output_formatted_temp.append(each_name) # Append output name in output_formatted_temp list
                output_formatted_temp.append(storein_list[loop_count]) #Append storein key in output_formatted_temp list
                output_formatted_temp.append(outcome[loop_count]) #Append output value in output_formatted_temp list
                output_formatted.append(output_formatted_temp) # Append output_formatted_temp list into output_formatted 2D list
                self.step_button_call_storein_dict[storein_list[loop_count]]=outcome[loop_count] # Upodate step_button_call_storein_dict with the output value
                loop_count+=1

            print("output_dict in step button call: ", output_dict)
            print("output_formatted in step button call: ", output_formatted)
            print("step_button_call_storein_dict in step button call: ", self.step_button_call_storein_dict)


            # Crete Output result string from output_formatted list to update the output label
            output_result='' # Crete Output result string
            for each in output_formatted:
                if each[1]!="": # If strein key in any row in output_formatted list is not empty, add the value
                    output_result=output_result+ "\n\t" + str(each[0]) + "=" + str(each[1])+ "=" +str(each[2])
                else:# If store in key in any row in output_formatted list is  empty, add the store in key as "&dummy&"
                    output_result = output_result + "\n\t" + str(each[0]) + "=" + "&dummy&" + "=" + str(each[2])
            print("output result(to update in label) in step button call: ", output_result)

            # Update varibale that hold the value for output label
            (self.var_table[row_selected[0]-1][3]).set(output_result)

        except Exception as e:
            messagebox.showerror('Error','Error in running the step as: ' + str(e), parent=self.process_studio_notebook)

    def save_document_button_call(self):
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']

        self.refresh_button_call()

        '''self.process_val_dict = {'Cluster': self.process_wids_dict['ClusterOptionmenuVar'].get(),
                                 'Process': self.process_wids_dict['ProcessOptionmenuVar'].get(),
                                 'Page': self.process_wids_dict['PageOptionmenuVar'].get(),
                                 'PageIndex': self.process_wids_dict['PageIndexVar'].get(),
                                 'Table': self.process_table_val_dict, 'Output': self.storein_output_dict}'''


        result, message = self.db.create_new_process_page_in_primary_databse(type='process',
                                                                             cluster=self.process_val_dict['Cluster'],
                                                                             process=self.process_val_dict['Process'],
                                                                             page=self.process_val_dict['Page'],
                                                                             pageindex=self.process_val_dict['PageIndex'],
                                                                             table=self.process_val_dict['Table'],
                                                                             output=self.process_val_dict['Output'])

        if result == 'Error':
            messagebox.showerror(result, message, parent=fr_config)
        else:
            messagebox.showinfo(result, 'Process saved', parent=fr_config)

        print('process_val_dict in save button call: ',self.process_val_dict)

    def retrive_page_doc(self):

        self.test['Test']='Test is added'
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        fr_table = self.process_wids_dict['TableFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']
        page_var = self.process_wids_dict['PageOptionmenuVar']
        page_index_var = self.process_wids_dict['PageIndexVar']

        cluster=cluster_var.get()
        process=process_var.get()
        page=page_var.get()

        latest_page_doc = self.db.retrive_latest_page_doc(cluster=cluster,process=process,page=page)
        print('latest_page_doc: ', latest_page_doc)

        page_index=latest_page_doc['pageindex']
        page_index_var.set(page_index)
        page_table_dict=latest_page_doc['table']
        output_table_dict=latest_page_doc['output']['Table']
        global storein_output_dict
        storein_output_dict=output_table_dict=latest_page_doc['output'] #this is a global variable


        rows_in_page_table=len(page_table_dict)
        for each in range(rows_in_page_table):self.add_row_button_call()

        row=1
        for each_row in page_table_dict:
            handle=page_table_dict[each_row]['Handle']
            action = page_table_dict[each_row]['Action']
            input = page_table_dict[each_row]['Input']
            output = page_table_dict[each_row]['Output']
            exception = page_table_dict[each_row]['Exception']

            self.process_table_var_dict[row]['Handle'].set(handle)
            self.process_table_var_dict[row]['Action'].set(action)
            self.process_table_var_dict[row]['Input'].set(input)
            self.process_table_var_dict[row]['Output'].set(output)
            self.process_table_var_dict[row]['Exception'].set(exception)

            row+=1

        children_windows = self.outputtab_table_frame.winfo_children()
        for each in children_windows:
            each.destroy()

        output_tab=ProcessStudioOutputTab(self.process_studio_notebook,self.db,self.process_studio_output_tab)
        output_tab.refresh_table()
        #self.refresh_button_call()
        #output_table_dict

    def refresh_table(self):
        children_widgets=self.outputtab_table_frame.winfo_children() #children widgets from output tab table frame

        #child_widgets = table_frame.winfo_children()  # Store all chidlren widgets in output tab table frame
        # destoy all the chidren widgets
        for each in children_widgets:
            each.destroy()

        output_tab_table_dict=self.storein_output_dict['Table']

    def run_button_call(self):
        x = 100
        output_store=self.derive_run_script()
        print("output store in run button call: ", output_store)

    def derive_run_script(self):
        fr_config = self.process_wids_dict['ConfigureFrame']
        self.db = Database.database(self.primary_db_path, self.secondary_db_path)  # create db object
        # store all the pages for the slected process sorted as per page index in a list ( each page doc inside the list is a dictionary)
        latest_pages_doc=self.retrive_latest_indexed_pages_doc()

        output_store={}
        #output_store = {'page1': {'x': 100}}
        module_list=[]
        module_script=''
        script=''

        function_script=''
        outcome_script,outcome_script_try,outcome_script_except='','',''
        function_name,outcome_name='',''
        #loop table dictionary in
        for each_page_doc in latest_pages_doc: #loop pages in pages doc list
            table=each_page_doc['table'] #store table dictionary in the page doc
            page_index=each_page_doc['pageindex'] #store the page index
            page_output_store=each_page_doc['output']['Table'] #store the output store for page
            page=each_page_doc['page'] # store ethe page name
            output_store[page]=page_output_store # store the


            action_loops=0

            for each_row_index in table: #loop each row in the table dictionary of the each page doc dictionary

                function_name='function_' + str(page_index) + "_" + str(each_row_index)
                outcome_name = 'outcome_' + str(page_index) + "_" + str(each_row_index)


                input_script,output_script,code_script = '',"",""

                handle=table[each_row_index]['Handle'] #store handle string
                action=table[each_row_index]['Action'] #store action string
                input_dict = table[each_row_index]['Input']  # store input dictionary
                output_dict = table[each_row_index]['Output']  # store output dictionary
                exception_dict = table[each_row_index]['Exception']  # store exception dictionary
                action_doc=self.db.retrive_latest_action_doc(handler=handle,action=action)
                code_dict=action_doc[0]['code']

                zero_tab="\n"
                one_tab = '\n\t'
                two_tabs = '\n\t\t'
                three_tabs = '\n\t\t\t'
                four_tabs='\n\t\t\t\t'
                if action=='Loop-Start':
                    action_loops=action_loops+1
                elif action=='Loop-End':
                    action_loops = action_loops - 1

                for each in range(action_loops-1):
                    one_tab = one_tab + "\t"
                    two_tabs = two_tabs + "\t"
                    three_tabs = three_tabs + "\t"
                    four_tabs = four_tabs + "\t"

                for each in range(action_loops-1):
                    zero_tab = zero_tab + "\t"


                # derive module script
                page_module_dict = action_doc[0]['module']
                for each_row in page_module_dict:
                    module_name = page_module_dict[each_row]['ModuleName']
                    if module_name not in module_list:
                        module_list.append(module_name)
                        module_script = module_script + '\n\timport ' + module_name

                print("input dict in run button call: ",input_dict)

                # create input script
                input_dict=eval(input_dict)
                for each_row in input_dict:
                    print(each_row)
                    InputValue=input_dict[each_row]['InputValue']
                    InputName=input_dict[each_row]['InputName']

                    if InputValue == '':
                        InputValue = 'str()'
                    elif '#' in InputValue[0]:
                        index=InputValue.replace('#','')
                        #InputValue= "eval('output_store' + InputValue.replace('#',''))"
                        #InputValue = "eval(" + 'output_store' + index + ") "
                        InputValue = str(output_store) + index
                    else:
                        InputValue = InputValue

                    print('input value in run: ',InputValue)
                    input_script = input_script + '\n\t\t' + InputName + "=" + InputValue

                # create output script
                output_dict=eval(output_dict)
                for each_row in output_dict:
                    OutputName=output_dict[each_row]['OutputName']
                    OutputValue=output_dict[each_row]['OutputValue']

                    if OutputValue == "":
                        OutputValue = 'str()'
                    else:
                        OutputValue = OutputValue
                    output_script = output_script + '\n\t\t' + OutputName + "=" + OutputValue

                # create code script
                #code_dict=eval(code_dict)
                print("code dict in run button call: ",code_dict)
                for each_row in code_dict:
                    code_line=code_dict[each_row]
                    code_script = code_script + '\n\t\t' + code_line

                # create function combining module,input,output and code script
                if action!='Loop-Start' and action!='Loop-End' :
                    #function_script = function_script + "\n\tdef "+ function_name + "():\n\n\t\t#input" + input_script + "\n\n\t\t#output" + output_script + "\n\n\t\t#code" + code_script
                    function_script = function_script + "\n\tdef " + function_name + "():\n\n\t\t#input" + input_script + "\n\n\t\t#output" + output_script +  "\n\n\t\t#output_dict\n\n\t\toutput_dict=" + str(output_dict) +    "\n\n\t\t#code" + code_script #output_dict

                    if action_loops == 0:
                        print('output dict: ',output_dict)

                        '''outcome_script_try = "\ntry:\n\t" + outcome_name + "= " + function_name + "()\n\tloop_count=0" \
                                             "\n\tfor each in" + outcome_name  + ":\n\t\toutput_store['" + page + "']['"+ "output_dict[loop_count]['StoreIn']" + "'] = " + outcome_name + "[loop_count]" \
                                             "\n\t\tloop_count+=1"'''

                        #outcome_script_try = "\ntry:\n\t" + outcome_name + "=" + function_name + "()\n\tif len(str(" + outcome_name + "))>0:\n\t\tif 'int' in  str(type(" + outcome_name + "))  or 'str' in  str(type(" + outcome_name + ")):\n\t\t\t" + outcome_name + "=[" + outcome_name + "]\n\tloop_count = 0 \n\tfor each in " + outcome_name + ":\n\t\toutput_store['" + page + "'][" + "output_dict[loop_count]['StoreIn']" + "] = " + outcome_name + "[loop_count]"                                                                                                                                                                                                                                                                                                                                                                                                                                   "\n\t\tloop_count+=1"

                        outcome_script_try = "\ntry:\n\t" + outcome_name + "=" + function_name + "()\n\tprint('outcome before making list: '," + outcome_name + ")\n\tif len(str(" + outcome_name + "))>0:\n\t\tif 'int' in  str(type(" + outcome_name + "))  or 'str' in  str(type(" + outcome_name + ")):\n\t\t\t" + outcome_name + "=[" + outcome_name + "]\n\tprint('outcome: '," + outcome_name + ")" + "\n\toutput_dict=" + str(output_dict) +"\n\tloop_count = 1 \n\tfor each in " + outcome_name + ":\n\t\tprint(output_dict[loop_count]['StoreIn'])\n\t\toutput_store['" + page + "'][ (output_dict)[loop_count]['StoreIn'] ] = " + "each\n\t\tprint(output_dict[loop_count]['StoreIn'])"                                                                                                                                                                                                                                                                                                                                                                                                                                   "\n\t\tloop_count+=1"

                        #outcome_script_try = "\ntry:\n\t" + outcome_name + "=" + function_name + "()\n\tprint(" + outcome_name + ")\n\tif len(str(" + outcome_name + "))>0:\n\t\tif 'int' in  str(type(" + outcome_name + "))  or 'str' in  str(type(" + outcome_name + ")):\n\t\t\t" + outcome_name + "=[" + outcome_name + "]\n\tprint('outcome: '," + outcome_name + ")\n\tloop_count = 0 \n\tfor each in " + outcome_name + ":\n\t\toutput_store['" + page + "'][ output_dict[loop_count]['StoreIn'] ] = " + outcome_name + "[loop_count]\n\t\tprint(output_dict[loop_count]['StoreIn'])"                                                                                                                                                                                                                                                                                                                                                                                                                                   "\n\t\tloop_count+=1"

                        outcome_script_except = "\nexcept Exception as e:\n\terror='Error: Error in running the action in row:" + each_row_index + "in page: " + page +  " as: '" + '+ str(e)' + "\n\tmessagebox.showerror('Error',error,parent=fr_config)"

                        outcome_script=outcome_script + outcome_script_try+outcome_script_except

                    else:
                        #outcome_script_try = one_tab+"try:" + two_tabs + outcome_name + "=" + function_name + "()" + two_tabs + "loop_count=0" + two_tabs + "for each in" + outcome_name + ":" + three_tabs + "toutput_store[" + page + "][" + "output_dict[loop_count]['StoreIn']" + "] =" +  outcome_name + "[loop_count]" + three_tabs + "loop_count+=1"
                        #outcome_script_try = "\ntry:" + two_tabs + outcome_name +"=function()" + two_tabs + "loop_count=0" + two_tabs + "for each in outcome_dict:" + three_tabs + "outcome_dict[each] = outcome[loop_count]"  + three_tabs + "loop_count+=1"
                        outcome_script_try = one_tab + "try:" + two_tabs + outcome_name + "=" + function_name + "()" + two_tabs + "if len(str(" + outcome_name + "))>0:" + three_tabs + "if 'int' in  str(type(" + outcome_name + "))  or 'str' in  str(type(" + outcome_name + ")):" + four_tabs+ outcome_name + "=[" + outcome_name + "]" + two_tabs + "loop_count = 0" + two_tabs + "for each in " + outcome_name + ":" + three_tabs + "output_store[" + page + "][" + "eval(output_dict[loop_count]['StoreIn'])" + "] = " + outcome_name + "[loop_count]" + three_tabs  + "loop_count+=1"

                        outcome_script_except = one_tab+"except Exception as e:" + two_tabs + "error='Error: Error in running the action in row: " + each_row_index + " in page: " + page + " as: '" + '+ str(e)' + two_tabs + "messagebox.showerror('Error',error,parent=fr_config)"
                        #outcome_script = outcome_script + outcome_script_try + outcome_script_except
                        outcome_script = outcome_script_try + outcome_script_except
                if action == 'Loop-Start':
                    loop_string=zero_tab + "for each in " + InputValue + ":"
                    outcome_script = outcome_script + loop_string



        # add try and excpet portion in function script
        function_script="\ntry:" +module_script +function_script + "\nexcept Exception as e:\n\terror='Error: Error in creating the function script as:'" + '+ str(e)' \
                                "\n\tmessagebox.showerror('Error',error,parent=fr_config)"


        #print("function script in run button call: ",function_script)
        #print("outcome script in run button call: ", outcome_script)

        script=function_script+outcome_script
        print(" script in run button call: ", script)

        exec(script)
        return output_store






    #all the latest page for the given process is retrived and sorted as per page index
    def retrive_latest_indexed_pages_doc(self):
        self.db = Database.database(self.primary_db_path, self.secondary_db_path) #create db object
        # get widgets
        fr_config = self.process_wids_dict['ConfigureFrame']
        cluster_var = self.process_wids_dict['ClusterOptionmenuVar']
        process_var = self.process_wids_dict['ProcessOptionmenuVar']
        page_var = self.process_wids_dict['PageOptionmenuVar']

        cluster = cluster_var.get() #store selected cluster
        process = process_var.get() #store sleected process

        # retrive name of all the pages for the selected process
        pages_name_list = self.db.retrive_all_page_names_for_process(cluster, process)


        latest_page_doc_list_unindexed = [] # create list to store all the pages for slected process
        latest_page_doc_list_indexed = [] # create a list to store all the pages for the selcted process in an indexed order

        # retrive pages and add it into  latest_page_doc_list_unindexed
        for each_page_name in pages_name_list:
            if each_page_name != "#NA":
                pages_name_list = self.db.retrive_latest_page_doc(cluster, process, each_page_name)
                latest_page_doc_list_unindexed.append(pages_name_list)

        #s sort all the retrived pages as per page index
        for each_index in range(500):
            for each_page_doc in latest_page_doc_list_unindexed:
                if each_page_doc['pageindex'] == each_index:
                    latest_page_doc_list_indexed.append(each_page_doc)

        print('latest_page_doc_list in --derive_run_script', latest_page_doc_list_indexed)
        return latest_page_doc_list_indexed


class ProcessStudioOutputTab(ProcessStudio):

    def __init__(self,process_studio_notebook,process_studio_output_tab,primary_db_path,secondary_db_path):
        super().__init__(process_studio_notebook, primary_db_path,secondary_db_path)
        self.primary_db_path = primary_db_path
        self.secondary_db_path = secondary_db_path
        self.db = Database.database(self.primary_db_path, self.secondary_db_path)

        self.process_studio_notebook=process_studio_notebook
        self.process_studio_output_tab=process_studio_output_tab
        self.check_button_dict = {}
        self.var_table = []
        self.storein_dict={}
        self.var_table_dict={} #store all the variable fo the row by rows

        self.output_var_dict={'ConfigurationFrame':'','TableCanvas':'' ,'TableFrame':'','AddButton':'','DeleteButton':'','RefreshButton':''}

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

        bt_refresh = Button(fr_config, text="Refresh", command=lambda :self.refresh_table())
        #bt_del.place(relx=0.235, rely=0.5, relwidth=0.035)
        bt_refresh.grid(row=1, column=3)

        #self.process_tab_config_frame_gui(process_studio_process_tab,'',"","")
        children_windows=frame.winfo_children()
        print(children_windows)
        loop_count=0
        active_row=True
        row=1
        for each in children_windows:
            print(each)

        self.output_var_dict = {'ConfigurationFrame': fr_config, 'TableCanvas': cn_on_fr_table, 'TableFrame': frame, 'AddButton': bt_add,
                                'DeleteButton': bt_del, 'RefreshButton': bt_refresh}
        return frame

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

            self.var_table_dict[next_row]={'VariableName':var_variable_name,'VariableValue':var_variable_value}

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
            self.var_table_dict={}

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
                self.var_table_dict[next_row] = {'VariableName': var_variable_name, 'VariableValue': var_variable_value}

                # create CheckButton for selecting row
                var_row_select = IntVar()
                cb_row_select = Checkbutton(fr_table, variable=var_row_select)
                cb_row_select.configure(
                    command=lambda cb=cb_row_select, var=var_row_select: get_checkbutton_value(cb, var))
                cb_row_select.grid(row=next_row, column=4)

        # mark all the checkbutton values btaken to dictionary as 0
        for each in self.check_button_dict:
            self.check_button_dict[each] = 0


    def get_table_values(self):
        val_table={} # Create dictionary to store variable values of table
        row_num=1
        # Get the value from variable to dictionary
        for each_row in self.var_table:
            val_table[each_row[0].get()]=each_row[1].get()

        return val_table

    def destory_all_widgets_in_output_tab(self):
        child_widgets=self.process_studio_output_tab.winfo_children() #Store all chidlren widgets in output tab(these are frames)
        #destoy all the chidren widgets
        for each in child_widgets:
            each.destroy()
        self.var_table = [] # Set the variable list as empty


    def refresh_table(self):
        table_frame=self.output_var_dict['TableFrame']

        child_widgets = table_frame.winfo_children()  # Store all chidlren widgets in output tab table frame
        # destoy all the chidren widgets
        for each in child_widgets:
            each.destroy()

        print('print storein_output_dict: ',storein_output_dict)

        #print('1L: ',self.storein_output_dict)
        rows=len(storein_output_dict['Table'])
        table_dict=storein_output_dict['Table']
        #self.storein_output_dict

        print(self.var_table_dict)
        loop_count=1
        for each in range(rows):
            self.add_row_button_call(self.process_studio_output_tab)
            self.var_table_dict[loop_count]['VariableName'].set(table_dict[str(loop_count)]['Key'])
            self.var_table_dict[loop_count]['VariableValue'].set(table_dict[str(loop_count)]['Value'])

            loop_count+=1


