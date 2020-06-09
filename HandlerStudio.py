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

class MainWindow:

    def __init__(self, primary_db,secondary_db):
        self.num_rows = 4
        self.primary_db = primary_db
        self.secondary_db = secondary_db
        self.studio_window = ''
        self.root=''

    def main_frame(self):
        root = Tk()
        root.title('Studio')
        self.root=root
        #self.root.geometry("200x200")
        #self.root.resizable(0, 0)
        w=600
        h=400
        # get screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        button1 = Button(root, text="open new window", command=lambda x=root: self.studio_windowx(x))

        button1.place(x=50, y=25, width=100, height=25)
        root.mainloop()

    def studio_windowx(self,root):  # new window definition
        print('test')
        self.studio_window = Toplevel(root)
        self.studio_window.title('New Window')
        #newwin.geometry("200x100")
        #newwin.resizable(0, 0)`
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

        handler_studio_notebook = ttk.Notebook(object_studio_frame_tab)
        handler_studio_notebook.place(relx=0.01,rely=0.01,relheight=0.98,relwidth =0.98)

        code=Code(handler_studio_notebook)
        code.handler_studio()
        code.module_tab_gui()
        code.input_tab_gui()
        code.output_tab_gui()
        code.code_tab_gui()

        '''process_studio_notebook = ttk.Notebook(process_studio_frame_tab)
        process_studio_notebook.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

        os=ObjectStudio(self.root,db,object_studio_notebook)
        os.object_studio()

        ps=ProcessStudio.ProcessStudio(process_studio_notebook,self.database)
        ps.process_studio()

        #return object_studio_notebook,process_studio_notebook

        #self.object_studio(object_studio_notebook)'''

class HandlerStudio(MainWindow):

    def __init__(self,handler_studio_notebook):
        self.x=100
        self.handler_studio_notebook=handler_studio_notebook
        self.hs_tab_wids_dict = {'ModuleTab': '', 'InputTab': '', 'OutputTab': '','CodeTab': ''} # store all the tabs widgets into a session variable

        #create a dictionary of widgets in module tab
        self.module_wids_dict={'ParameterFrame':'','HandleLabel':'','HandleOptionMenu':'','HandleVar':'',
                               'NewHandleLabel':'','NewHandleEntry':'','NewActionLabel':'','NewActionEntry':'',
                               'ActionLabel':'','ActionOptionMenu':'','ActionVar':'',
                               'TableFrame':'','TableCanvas':'','TableScrollBar':'',
                               'AddTableRowButton':'','DelTableRowButton':'','ValidateTableRowButton':''}

        # create a dictionary of widgets in input tab
        self.input_wids_dict = {'ParameterFrame': '', 'HandleLabel': '','HandleLabelValue': '',
                                 'ActionLabel': '', 'ActionLabelValue': '','HandleVar':'','ActionlVar':'',
                                 'TableFrame': '', 'TableCanvas': '', 'TableScrollBar': '',
                                 'AddTableRowButton': '', 'DelTableRowButton': '', 'ValidateTableRowButton': ''}

        # create a dictionary of widgets in output tab
        self.output_wids_dict = {'ParameterFrame': '', 'HandleLabel': '', 'HandleLabelValue': '',
                                'ActionLabel': '', 'ActionLabelValue': '','HandleVar':'','ActionVar':'',
                                'TableFrame': '', 'TableCanvas': '', 'TableScrollBar': '',
                                'AddTableRowButton': '', 'DelTableRowButton': '', 'ValidateTableRowButton': ''}

        # create a dictionary of widgets in output tab
        self.code_wids_dict={'CodeTextbox':'','CodeTextVar':'' , 'DebugButton':'','RunButton':'','SaveButton':''}

    def handler_studio(self):
        # Make the  tab
        module_tab = Frame(self.handler_studio_notebook,bd=0,bg="snow")
        input_tab = Frame(self.handler_studio_notebook, bd=0, bg="snow")
        output_tab = Frame(self.handler_studio_notebook, bd=0, bg="snow")
        code_tab = Frame(self.handler_studio_notebook, bd=0, bg="snow")

        # Add the tabs
        self.handler_studio_notebook.add(module_tab, text="Module")
        self.handler_studio_notebook.add(input_tab, text="Input")
        self.handler_studio_notebook.add(output_tab, text="Output")
        self.handler_studio_notebook.add(code_tab, text="Code")

        self.hs_tab_wids_dict={'ModuleTab':module_tab,'InputTab':input_tab,'OutputTab':output_tab,'CodeTab':code_tab} # store all the tabs widgets into a session variable

        '''self.os_module_tab(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)
        self.os_input_tab(object_studio_input_tab)
        self.os_output_tab(object_studio_output_tab)
        self.os_code_tab(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)
        self.os_run_tab(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab,object_studio_run_tab)'''


class Module(HandlerStudio):

    def __init__(self,handler_studio_notebook):
        super().__init__(handler_studio_notebook)
        self.row_num_in_module_tbl=1
        print("x is : ",self.x)
        primary_db = r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
        secondary_db = r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
        self.db_m = Database.database(primary_db, secondary_db)

    def module_tab_gui(self):
        hs_tab_wids_dict=self.hs_tab_wids_dict # store tabs widgets inherited from HandlerStudio Class
        module_tab=hs_tab_wids_dict['ModuleTab'] #store module tab widget

        main_frame=Frame(module_tab,bg='snow')
        main_frame.place(relx=0.2, rely=0.15, height=400, width=710)

        #create parent frame in module tab
        #parent = Frame(module_tab)
        #parent.place(relx=0.2, rely=0.31, relheight=.4, relwidth=0.501)
        #parent.place(relx=0.2, rely=0.31, relheight=.4, width=624)
        parent = Frame(main_frame)
        parent.place(relx=0.001, rely=0.29, relheight=.68, width=624)

        canvas = Canvas(parent,bd=0,highlightthickness=0) #create canvas on parent frame of module
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview) #create scroolbar on parent frame of module

        frame = Frame(canvas,bd=0) # create frame on Canvas

        # create header and 2 rows in module table
        for i in range(3):
            if self.row_num_in_module_tbl==1:
                Label(frame, text="Module Name", font=("Arial Bold", 10), bg='gray87', width=30,
                                            relief=GROOVE).grid(column=0,row=self.row_num_in_module_tbl)
                Label(frame, text="Module Path", font=("Arial Bold", 10), bg='gray87',width=44,
                                            relief=GROOVE).grid(column=2, row=self.row_num_in_module_tbl,sticky=E,columnspan=10)
            else:
                Entry(frame, width=40).grid(column=0,row=self.row_num_in_module_tbl,sticky=NW)
                Entry(frame,width=59 ).grid(column=1, row=self.row_num_in_module_tbl,sticky=NW,columnspan=10)
            self.row_num_in_module_tbl+=1


        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)    # creare a window in canvas in put thee child frame
        canvas.update_idletasks()   # make sure everything is displayed before configuring the scrollregion
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set) #configure canvas for scrrol region and command
        canvas.pack(fill='both', expand=True, side='left') #pack canvass
        scroll_y.pack(fill='y', side='right') #pack scrollbar


        # Create buttons to add rows ,delete rows and validate the values in table
        add_button = Button(main_frame, text='Add',command=lambda:self.module_add_button_call())
        add_button.place(x=635, rely=.29,height=20,width=70)
        remove_button = Button(main_frame, text='Remove',command=lambda:self.module_remove_button_call())
        remove_button.place(x=635, rely=.35, height=20, width=70)
        validate_button = Button(main_frame, text='Validate',command=lambda:self.module_validate_button_call())
        validate_button.place(x=635, rely=.41, height=20, width=70)

        #create frame for parameters to place the widgets such as ahndle and action

        fr_parameter = Frame(main_frame)
        fr_parameter.place(relx=0.001, rely=0.001, relheight=.28, width=624)

        #create handle label on parameter frame
        handle_label = Label(fr_parameter, text="Handle:",font=("Arial Bold", 9))
        handle_label.place(relx=0.05, rely=0.2, relheight=.18, relwidth=0.2)

        # create option menue for handles on parameter5 frame
        handle_var = StringVar(fr_parameter)
        #choices = ["Create New Handle",'#NA']
        choices = self.db_m.retrive_all_handles()
        handle_option_menus = OptionMenu(fr_parameter, handle_var, *choices)
        handle_option_menus.configure(bg='snow')
        handle_option_menus.place(relx=0.25, rely=0.15,relwidth=0.5)

        # load handle options
        #self.load_os_module_handle_optionmenu()

        # trace the value change for handle
        def module_handle_refresh_call(*args):self.module_handle_refresh_call()
        handle_var.trace("w",module_handle_refresh_call)

        # Create action label
        action_label = Label(fr_parameter, text="Action:", font=("Arial Bold", 9))
        action_label.place(relx=0.05,rely=0.5,relheight=.18,relwidth=0.2)

        # create action option menu
        action_var = StringVar(fr_parameter)
        action_choices = ["Create New Action",'#NA']
        action_menu = OptionMenu(fr_parameter, action_var, *action_choices)
        action_menu.configure(bg='snow')
        action_menu.place(relx=0.25, rely=0.45,relwidth=0.5)

        # trace the value change for action
        def module_action_refresh_call(*args):self.module_action_refresh_call()
        action_var.trace("w", module_action_refresh_call)




        self.module_wids_dict={'ParameterFrame':fr_parameter,'HandleLabel':handle_label,'HandleOptionMenu':handle_option_menus,'HandleVar':handle_var,
                               'NewHandleLabel':'','NewHandleEntry':'','NewActionLabel':'','NewActionEntry':'',
                               'ActionLabel':action_label,'ActionOptionMenu':action_menu,'ActionVar':action_var,
                               'TableFrame':frame,'TableCanvas':canvas,'TableScrollBar':scroll_y,
                               'AddTableRowButton':add_button,'DelTableRowButton':remove_button,'ValidateTableRowButton':validate_button}

    def module_add_button_call(self):
        # store table widgets
        frame=self.module_wids_dict['TableFrame']
        canvas = self.module_wids_dict['TableCanvas']
        scroll_y = self.module_wids_dict['TableScrollBar']

        #add rows
        self.row_num_in_module_tbl += 1
        Entry(frame, width=40).grid(column=0, row=self.row_num_in_module_tbl, sticky=NW)
        Entry(frame, width=59).grid(column=1, row=self.row_num_in_module_tbl, sticky=NW, columnspan=10)

        # configure canvas for newly added rows
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)
        #canvas.pack(fill='both', expand=True, side='left')
        #scroll_y.pack(fill='y', side='right')
        print("Total grids after clicking add button - module tab -frame: ",len(frame.grid_slaves()))

    def module_remove_button_call(self):
        # store table widgets
        frame = self.module_wids_dict['TableFrame']

        # create list to store all entry widgets in table(because only entry widegets from the table should be deleted)
        entry_widgets_list=list()
        children_widgets = frame.winfo_children() #store all the widgets in the frame(widgets include header labels and entry wwidgets)

        #Loop all the widgets in the table frame and store entry widgets in entry_widgets_list
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                entry_widgets_list.append(child_widget)

        # delete rows from the last row
        if len(entry_widgets_list)>1:
            entry_widgets_list[len(entry_widgets_list)-1].destroy() # delete module path entry widget
            entry_widgets_list[len(entry_widgets_list) - 2].destroy() # delete module name entry widget

    def module_validate_button_call(self):
        # store table widgets
        frame = self.module_wids_dict['TableFrame']
        # call validate module table function
        result,error_list=self.validate_module_table()
        if result=='Error':
            messagebox.showerror("Error", "Moduels are not available: " + ','.join(error_list), parent=frame)
        else:
            messagebox.showinfo('Success', 'All modules successfuly validated', parent=frame)

    def module_handle_refresh_call(self):
        self.db_m = Database.database(primary_db, secondary_db)
        parameter_frame=self.module_wids_dict['ParameterFrame']
        handle_var = self.module_wids_dict['HandleVar']
        #value=handle_var.get()

        children_widgets = parameter_frame.winfo_children() #store all the widhets in table frame

        #destory all the entry widgets in paremeter frame
        loop_count = 0
        for child_widget in children_widgets:
            loop_count += 1
            if loop_count > 3: # first 2 widgets are handler label and handler option menu , so destory widegts from 3rd widget
                child_widget.destroy()
        #clear values in module_wids_dict for the destroyed widgets
        self.module_wids_dict['ActionLabel']=''
        self.module_wids_dict['ActionOptionMenu'] = ''
        self.module_wids_dict['ActionVar'] = ''
        self.module_wids_dict['NewHandleLabel'] = ''
        self.module_wids_dict['NewHandleEntry'] = ''
        self.module_wids_dict['NewActionLabel'] = ''
        self.module_wids_dict['NewActionEntry'] = ''

        option_value = handle_var.get() # get the current value selected for handle

        # if the value selected in handle is 'Create New Handle'perform the below actions
        if option_value == 'Create New Handle':

            # create new handle label
            new_handle_label = Label(parameter_frame, text="New Handle:", font=("Arial Bold", 9))
            new_handle_label.place(relx=0.05, rely=0.48,relheight=.18, relwidth=0.2)
            self.module_wids_dict['NewHandleLabel'] = new_handle_label

            #create new handle entry
            new_handle_entry = Entry(parameter_frame)
            new_handle_entry.place(relx=0.25, rely=0.45, relheight=.20, relwidth=0.5)
            self.module_wids_dict['NewHandleEntry'] = new_handle_entry

            # create new action label
            new_action_label = Label(parameter_frame, text="New Action:", font=("Arial Bold", 9))
            new_action_label.place(relx=0.05, rely=0.67,relheight=.18,relwidth=0.2)
            self.module_wids_dict['NewActionLabel'] = new_action_label

            new_action_entry = Entry(parameter_frame)
            new_action_entry.place(relx=0.25, rely=0.67, relheight=.20, relwidth=0.5)
            self.module_wids_dict['NewActionEntry'] = new_action_entry

        # if any other value selected, refresh action dropdown listing all the action of the selcted handler
        else:
            #create handle label(because all the widgets excep handle lable and option menu delted before)
            action_label = Label(parameter_frame, text="Action:", font=("Arial Bold", 9))
            action_label.place(relx=0.05, rely=0.5, relheight=.18, relwidth=0.2)
            self.module_wids_dict['ActionLabel'] = action_label

            #create action option menu
            action_value_var = StringVar(parameter_frame)
            action_choices = self.db_m.retrive_actions_for_handle(option_value)
            action_menu = OptionMenu(parameter_frame, action_value_var, *action_choices)
            action_menu.configure(bg='snow')
            #action_menu.place(relx=0.25, rely=0.45,relheight=.24, relwidth=0.5)
            action_menu.place(relx=0.25, rely=0.45, relwidth=0.5)
            self.module_wids_dict['ActionOptionMenu'] = action_menu
            self.module_wids_dict['ActionVar'] = action_value_var

            # trace the value change for action
            def module_action_refresh_call(*args):self.module_action_refresh_call()
            action_value_var.trace("w", module_action_refresh_call)

        self.clear_table()

    def module_action_refresh_call(self):
        self.db_m = Database.database(primary_db, secondary_db)
        #store widgets in module
        parameter_frame = self.module_wids_dict['ParameterFrame']
        action_var = self.module_wids_dict['ActionVar']
        handle_var = self.module_wids_dict['HandleVar']
        action_value = action_var.get()
        handle_value=handle_var.get()

        # perform below activity if the action is 'Create New Action'
        if action_value == 'Create New Action':

            #create new action label
            new_action_label = Label(parameter_frame, text="New Action:", font=("Arial Bold", 9))
            new_action_label.place(relx=0.05, rely=0.74,relheight=.18,relwidth=0.2)
            self.module_wids_dict['NewActionLabel'] = new_action_label

            #create new action entry
            new_action_entry = Entry(parameter_frame)
            new_action_entry.place(relx=0.25, rely=0.74,  relwidth=0.5)
            self.module_wids_dict['NewActionEntry'] = new_action_entry
            self.clear_table()

        # destory NewActionLabel and NewActionEntry widgets , if the other value is selected in action
        else:
            if self.module_wids_dict['NewActionLabel']!='':self.module_wids_dict['NewActionLabel'].destroy()
            self.module_wids_dict['NewActionLabel'] = ''
            if self.module_wids_dict['NewActionEntry'] != '': self.module_wids_dict['NewActionEntry'].destroy()
            self.module_wids_dict['NewActionEntry'] = ''

            self.clear_table()

            self.load_action_document_in_tabs(handle_value,action_value)

    def validate_module_table(self):
        # store table widgets
        frame = self.module_wids_dict['TableFrame']

        # creare list to store module name, path and validation error
        text_list, modue_name_list, module_path_list, validation_error_list = list(), list(), list(), list()

        loop_count = 0
        children_widgets = frame.winfo_children()  # store all the widgets in the frame(widgets include header labels and entry wwidgets)

        # Loop widgets in table frame and the widget is entry, get the value to append in module name and path list
        for child_widget in children_widgets:
            loop_count += 1
            if child_widget.winfo_class() == 'Entry':
                text = child_widget.get()  # get the value from entry box
                if loop_count % 2 != 0 : modue_name_list.append(text)  # if the entry widget in odd position, it is a module name
                if loop_count % 2 == 0 and len(text) > 0: module_path_list.append(
                    text)  # if the entry widget in even position, it is a module name
                # if len(text)>0:text_list.append(text)

        # validation for module path will be used in future. Find the validation
        '''if len(module_path_list)>len(modue_name_list):validation_error_list.append("Module name missing for a given module path")
        for each in module_path_list:
            if os.path.exists(each)==False:validation_error_list.append("Module path not exist: " + each )
        if len(validation_error_list)>0:messagebox.showerror("Error",validation_error_list,parent=frame)'''

        # validate module name and if the module is not available , add it to validation_error_list
        for each in modue_name_list:
            if each=='':
                validation_error_list.append('Blank Rows in Module Name')
                return 'Error', ", ".join(validation_error_list)

            else:
                script = "try:\n\timport " + each + "\nexcept Exception as e:\n\tvalidation_error_list.append('Module Tab: ' + str(e))"
            # below code depreciated
            # script="try:\n\timport " + each  + "\n\tmessagebox.showinfo('Success','All modules successfuly validated',parent=frame)" +"\nexcept:\n\tmessagebox.showerror('Error'," + "'"+ "Module is not available: " + each + "'," + "parent=frame)  "
            exec(script)

        # show the error if there error in validation_error_list, else show succes message
        if len(validation_error_list) > 0:
            #return 'Error',validation_error_list
            return 'Error', ", ".join(validation_error_list)

        else:

            #return 'Success',validation_error_list
            return 'Success', ", ".join(validation_error_list)

    def clear_table(self):
        #get widgets
        module_table_frame = self.module_wids_dict['TableFrame']
        module_handle_var = self.module_wids_dict['HandleVar']
        module_action_var = self.module_wids_dict['ActionVar']
        input_table_frame = self.input_wids_dict['TableFrame']
        output_table_frame = self.output_wids_dict['TableFrame']
        code_textbox= self.code_wids_dict['CodeTextbox']
        input_handle_var=self.input_wids_dict['HandleVar']
        input_action_var = self.input_wids_dict['ActionVar']
        output_handle_var = self.output_wids_dict['HandleVar']
        output_action_var = self.output_wids_dict['ActionVar']

        #set input handle and action values
        if module_handle_var !='':  input_handle_var.set(module_handle_var.get())
        if module_action_var !='':input_action_var.set(module_action_var.get())

        #set output handle and action values
        if module_handle_var !='':output_handle_var.set(module_handle_var.get())
        if module_action_var !='':output_action_var.set(module_action_var.get())

        # clear text in module tab table
        child_widgets_table_frame = module_table_frame.winfo_children()
        for each in child_widgets_table_frame:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        # clear text in input tab table
        child_widgets_table_frame = input_table_frame.winfo_children()
        for each in child_widgets_table_frame:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        # clear text in input tab table
        child_widgets_table_frame = output_table_frame.winfo_children()
        for each in child_widgets_table_frame:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        #clear code text box
        code_textbox.delete('1.0', END)

    def load_action_document_in_tabs(self,handler,action):
        #self.db_m = Database.database(primary_db, secondary_db)
        action_doc=self.db_m.retrive_latest_action_doc(handler,action)
        print('action_doc in --load_action_document_in_tabs: ', action_doc)

        module_table=self.module_wids_dict['TableFrame']
        input_table=self.input_wids_dict['TableFrame']
        output_table=self.output_wids_dict['TableFrame']
        code_textbox = self.code_wids_dict['CodeTextbox']
        #code_text_var = self.code_wids_dict['CodeTextVar']

        child_m_table=module_table.winfo_children()#children widows in tmodule table
        child_i_table=input_table.winfo_children()#children widows in input table
        child_o_table = output_table.winfo_children()  # children widows in output table

        #dleete all entry widgets in module table
        for each in child_m_table:
            if each.winfo_class() == 'Entry':
                each.destroy()

        # dleete all entry widgets in input table
        for each in child_i_table:
            if each.winfo_class() != 'Label':
                each.destroy()

        # dleete all entry widgets in output table
        for each in child_o_table:
            if each.winfo_class() != 'Label':
                each.destroy()

        # clear code textbox
        code_textbox.delete('1.0',END)


        #add rows in module table
        module_dict=action_doc[0]['module']
        row=2
        for each in module_dict:
            name_var=StringVar()
            name=Entry(module_table, width=40,textvariable=name_var)
            name_var.set(module_dict[each]['ModuleName'])
            name.grid(column=0, row=row, sticky=NW)

            path_var = StringVar()
            path=Entry(module_table, width=59,textvariable=path_var)
            path_var.set(module_dict[each]['ModulePath'])
            path.grid(column=1, row=row, sticky=NW, columnspan=10)
            row+=1

        # add rows in input table
        input_dict = action_doc[0]['input']
        row = 2
        for each in input_dict:
            name_var = StringVar()
            name = Entry(input_table, width=40, textvariable=name_var)
            name_var.set(input_dict[each]['InputName'])
            name.grid(column=0, row=row, sticky=NW)

            val_var = StringVar()
            value = Entry(input_table, width=59, textvariable=val_var)
            val_var.set(input_dict[each]['InputValue'])
            value.grid(column=1, row=row, sticky=NW, columnspan=10)
            row += 1

        # add rows in output table
        output_dict = action_doc[0]['output']
        row = 2
        for each in output_dict:
            name_var = StringVar()
            name = Entry(output_table, width=40, textvariable=name_var)
            name_var.set(output_dict[each]['OutputName'])
            name.grid(column=0, row=row, sticky=NW)

            val_var = StringVar()
            value = Entry(output_table, width=59, textvariable=val_var)
            val_var.set(output_dict[each]['OutputValue'])
            value.grid(column=1, row=row, sticky=NW, columnspan=10)
            row += 1

        # add rows in code textbox
        code_text=''
        code_dict = action_doc[0]['code']
        row=1
        for each in code_dict:
            if row==1:
                code_text=code_dict[each]
            else:
                code_text=code_text+ '\n'  + code_dict[each]
            row+=1
        code_textbox.insert('insert',code_text)


class Input(Module):

    def __init__(self,handler_studio_notebook):
        super().__init__(handler_studio_notebook)
        self.row_num_in_input_tbl=1
        print("x is : ",self.x)


    def input_tab_gui(self):
        hs_tab_wids_dict=self.hs_tab_wids_dict # store tabs widgets inherited from HandlerStudio Class
        input_tab=hs_tab_wids_dict['InputTab'] #store module tab widget

        # create main frame
        main_frame = Frame(input_tab, bg='snow')
        main_frame.place(relx=0.2, rely=0.15, height=400, width=710)

        # cerate parent frame
        parent = Frame(main_frame)
        parent.place(relx=0.001, rely=0.29, relheight=.68, width=624)

        #parent = Frame(input_tab)
        #parent.place(relx=0.2, rely=0.26, relheight=.4, relwidth=0.5)

        # create canvas and scrollbar on parent frame for tabale frame
        canvas = Canvas(parent, bd=0, highlightthickness=0)
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview)

        frame = Frame(canvas, bd=0) # create table frame

        input_name_entry_obejct_list,input_value_entry_obejct_list,input_validate_button_obejct_list=list(),list(),list()

        for i in range(3):
            #if row number is 1, create name and value widget
            if self.row_num_in_input_tbl == 1:
                input_name_header_label = Label(frame, text="Input Name", font=("Arial Bold", 10), bg='gray87',width=30,relief=GROOVE)
                input_name_header_label.grid(column=0, row=self.row_num_in_input_tbl)

                input_val_header_label = Label(frame, text="Input Value", font=("Arial Bold", 10), bg='gray87',width=44,relief=GROOVE)
                input_val_header_label.grid(column=1, row=self.row_num_in_input_tbl, sticky=E, columnspan=10)


                #module_header_label = Label(frame, text="", font=("Arial Bold", 10), bg='gray87',width=2,relief=GROOVE).grid(column=2, row=r, sticky=E, columnspan=10)
            # if row number is more than 1, create entry widgets
            else:
                name_entry='name_entry'+str(i)

                #create entry widget for input name
                input_name_entry = Entry(frame, width=40)
                input_name_entry.grid(column=0, row=self.row_num_in_input_tbl, sticky=NW)

                # create entry widget for input value
                input_value_entry = Entry(frame,width=57)
                input_value_entry.grid(column=1, row=self.row_num_in_input_tbl, sticky=NW, columnspan=1)

                # create validate button widget for input value
                input_validate_button = Button(frame,height=1)
                input_validate_button.configure(command=lambda input_value_entry=input_value_entry: self.input_row_validate_button_call(input_value_entry))
                input_validate_button.grid(column=2, row=self.row_num_in_input_tbl, sticky=NW, columnspan=1)



            self.row_num_in_input_tbl += 1

        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set) # configure canvas for added widgets in table
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        # create button add ,remove and validate rows in table
        add_button = Button(main_frame, text='Add',command=lambda: self.input_add_button_call())
        add_button.place(x=635, rely=.29, height=20, width=70)

        remove_button = Button(main_frame, text='Remove',command=lambda: self.input_remove_button_call())
        remove_button.place(x=635, rely=.35, height=20, width=70)

        validate_button = Button(main_frame, text='Validate',command=lambda: self.input_validate_button_call())
        validate_button.place(x=635, rely=.41, height=20, width=70)

        #create parameter frame to place handle and action
        fr_parameter = Frame(main_frame)
        fr_parameter.place(relx=0.001, rely=0.001, relheight=.28, width=624)

        # create handle label
        handle_label = Label(fr_parameter, text="Handle:",font=("Arial Bold", 9))
        handle_label.place(relx=0.05, rely=0.32, relheight=.18,relwidth=0.2)

        # create label to store the value for handle
        handle_label_var=StringVar()
        handle_label_val = Label(fr_parameter, textvariable=handle_label_var, bg="azure",font=("Arial Bold", 9))
        handle_label_val.place(relx=0.25, rely=0.32, relheight=.18,relwidth=0.5)

        # create label for action
        action_label = Label(fr_parameter, text="Action:", font=("Arial Bold", 9))
        action_label.place(relx=0.05,rely=0.6,relheight=.18,relwidth=0.2)

        # create lable top store action value
        action_label_var=StringVar()
        action_label_val = Label(fr_parameter, textvariable=action_label_var, bg="azure", font=("Arial Bold", 9))
        action_label_val.place(relx=0.25, rely=0.6,relheight=.18,relwidth=0.5)

        # store all the widgets from input tab in a dictionary
        self.input_wids_dict = {'ParameterFrame': fr_parameter, 'HandleLabel': handle_label,'HandleLabelValue': handle_label_val,
                                 'ActionLabel': action_label, 'ActionLabelValue': action_label_val,'HandleVar':handle_label_var,'ActionVar':action_label_var,
                                 'TableFrame': frame, 'TableCanvas': canvas, 'TableScrollBar': scroll_y,
                                 'AddTableRowButton': add_button, 'DelTableRowButton': remove_button, 'ValidateTableRowButton': validate_button}


    def input_add_button_call(self):
        # store table widgets
        frame=self.input_wids_dict['TableFrame']
        canvas = self.input_wids_dict['TableCanvas']
        scroll_y = self.input_wids_dict['TableScrollBar']

        #add rows
        self.row_num_in_input_tbl += 1
        Entry(frame, width=40).grid(column=0, row=self.row_num_in_input_tbl, sticky=NW)

        ent_input_val=Entry(frame, width=57)
        ent_input_val.grid(column=1, row=self.row_num_in_input_tbl, sticky=NW)

        input_validate_button = Button(frame, height=1)
        input_validate_button.configure(command=lambda ent_input_val=ent_input_val: self.input_row_validate_button_call(ent_input_val))
        input_validate_button.grid(column=2, row=self.row_num_in_input_tbl, sticky=NW, columnspan=1)

        # configure canvas for newly added rows
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)
        #canvas.pack(fill='both', expand=True, side='left')
        #scroll_y.pack(fill='y', side='right')
        print("Total grids after clicking add button - input tab -frame: ",len(frame.grid_slaves()))


    def input_remove_button_call(self):
        # store table widgets
        frame = self.input_wids_dict['TableFrame']

        # create list to store all  widgets in table except to labels(because label widets are header widgets)
        widgets_list=list()
        children_widgets = frame.winfo_children() #store all the widgets in the frame(widgets include header labels and entry wwidgets)

        #Loop all the widgets in the table frame and store all the widgets except to label widget
        for child_widget in children_widgets:
            if child_widget.winfo_class() != 'Label':
                widgets_list.append(child_widget)

        # delete rows from the last row
        if len(widgets_list)>1:
            widgets_list[len(widgets_list)-1].destroy() # delete input validate button widget
            widgets_list[len(widgets_list) - 2].destroy() # delete input value entry widget
            widgets_list[len(widgets_list) - 3].destroy()  # delete input name widget

    def input_row_validate_button_call(self,input_value_entry_wid):
        frame = self.input_wids_dict['TableFrame']
        try:
            text=input_value_entry_wid.get()
            if len(text)>0:
                print("value taken")
                value=str(eval(input_value_entry_wid.get())) #evaluvate the value and store the result in value
            if len(text)==0:
                value='None'
            string="messagebox.showinfo('Input Value',message=value,parent=frame)" # show the message if the validation is succesful
            exec(string)
        except Exception as e:
            error="Error: " + str(e)
            string = "messagebox.showerror('Input Value',message=error,parent=frame)" # show the message if the eveluvation is with error
            exec(string)


    def input_validate_button_call(self):
        frame = self.input_wids_dict['TableFrame']

        #call validate input table function
        result,error_list=self.validate_input_table()
        if result=='Error':
            messagebox.showerror('Error', message='Input' + " tab: " + error_list, parent=frame)
        else:
            messagebox.showinfo('Success', message='Input' + " tab: " + "Successfully validated", parent=frame)

    def validate_input_table(self):
        frame = self.input_wids_dict['TableFrame']
        #create list to store input name value and validation error
        text_list,input_name_list,input_value_list,validation_error_list = list(),list(),list(),list()

        loop_count = 0
        children_widgets = frame.winfo_children()

        #loop all the widgets in table and store the name and value entry widgets
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                loop_count += 1
                text = child_widget.get()
                if loop_count % 2 != 0 : input_name_list.append(text) # name widgets is in odd position of the entry widgets
                if loop_count % 2 == 0 : input_value_list.append(text) # value widgets is in even position of the entry widgets
                if len(text) > 0: text_list.append(text)

        # Loop all the values and if any error found , store it in validation_error_list
        for each in input_value_list:
            try:
                text=str(each)
                if len(each)>0:
                    value = str(eval(text))
                    code="value = str(eval(text))"
                    exec(code)
            except Exception as e:
                error = "Error: " + str(e)
                validation_error_list.append(error)


        # validate input name
        loop_count=0
        for each in input_name_list:
            loop_count+=1
            # check name is missing in any row
            if len(each)==0:
                validation_error_list.append('Input' + ' name Missing in line: ' + str(loop_count) )

            # check any name is duplicated
            if input_name_list.count(each) > 1:
                validation_error_list.append('Input' + " name Duplicated in line "+ str(loop_count))
                #messagebox.showinfo('Error', message="Input/Output Name Duplicated: "+each, parent=frame)
                #break

        # check the errors in validation_error_list and show the message
        if len(validation_error_list)>0:
            return 'Error',", ".join(validation_error_list)
        else:
            return 'Success',", ".join(validation_error_list)


class Output(Input):

    def __init__(self,handler_studio_notebook):
        super().__init__(handler_studio_notebook)
        self.row_num_in_output_tbl=1
        print("x is : ",self.x)


    def output_tab_gui(self):
        hs_tab_wids_dict=self.hs_tab_wids_dict # store tabs widgets inherited from HandlerStudio Class
        output_tab=hs_tab_wids_dict['OutputTab'] #store module tab widget

        # create main frame
        main_frame = Frame(output_tab, bg='snow')
        main_frame.place(relx=0.2, rely=0.15, height=400, width=710)

        # cerate parent frame
        parent = Frame(main_frame)
        parent.place(relx=0.001, rely=0.29, relheight=.68, width=624)

        #parent = Frame(input_tab)
        #parent.place(relx=0.2, rely=0.26, relheight=.4, relwidth=0.5)

        # create canvas and scrollbar on parent frame for tabale frame
        canvas = Canvas(parent, bd=0, highlightthickness=0)
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview)

        frame = Frame(canvas, bd=0) # create table frame

        input_name_entry_obejct_list,input_value_entry_obejct_list,input_validate_button_obejct_list=list(),list(),list()

        for i in range(3):
            #if row number is 1, create name and value widget
            if self.row_num_in_output_tbl == 1:
                output_name_header_label = Label(frame, text="Output Name", font=("Arial Bold", 10), bg='gray87',width=30,relief=GROOVE)
                output_name_header_label.grid(column=0, row=self.row_num_in_output_tbl)

                output_val_header_label = Label(frame, text="Output Value", font=("Arial Bold", 10), bg='gray87',width=44,relief=GROOVE)
                output_val_header_label.grid(column=1, row=self.row_num_in_output_tbl, sticky=E, columnspan=10)


                #module_header_label = Label(frame, text="", font=("Arial Bold", 10), bg='gray87',width=2,relief=GROOVE).grid(column=2, row=r, sticky=E, columnspan=10)
            # if row number is more than 1, create entry widgets
            else:
                name_entry='name_entry'+str(i)

                #create entry widget for input name
                output_name_entry = Entry(frame, width=40)
                output_name_entry.grid(column=0, row=self.row_num_in_output_tbl, sticky=NW)

                # create entry widget for input value
                output_value_entry = Entry(frame,width=57)
                output_value_entry.grid(column=1, row=self.row_num_in_output_tbl, sticky=NW, columnspan=1)

                # create validate button widget for input value
                output_validate_button = Button(frame,height=1)
                output_validate_button.configure(command=lambda output_value_entry=output_value_entry: self.output_row_validate_button_call(output_value_entry))
                output_validate_button.grid(column=2, row=self.row_num_in_output_tbl, sticky=NW, columnspan=1)



            self.row_num_in_output_tbl += 1

        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set) # configure canvas for added widgets in table
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        # create button add ,remove and validate rows in table
        add_button = Button(main_frame, text='Add',command=lambda: self.output_add_button_call())
        add_button.place(x=635, rely=.29, height=20, width=70)

        remove_button = Button(main_frame, text='Remove',command=lambda: self.output_remove_button_call())
        remove_button.place(x=635, rely=.35, height=20, width=70)

        validate_button = Button(main_frame, text='Validate',command=lambda: self.output_validate_button_call())
        validate_button.place(x=635, rely=.41, height=20, width=70)

        #create parameter frame to place handle and action
        fr_parameter = Frame(main_frame)
        fr_parameter.place(relx=0.001, rely=0.001, relheight=.28, width=624)

        # create handle label
        handle_label = Label(fr_parameter, text="Handle:",font=("Arial Bold", 9))
        handle_label.place(relx=0.05, rely=0.32, relheight=.18,relwidth=0.2)

        # create label to store the value for handle
        handle_label_var=StringVar()
        handle_label_val = Label(fr_parameter, textvariable=handle_label_var, bg="azure",font=("Arial Bold", 9))
        handle_label_val.place(relx=0.25, rely=0.32, relheight=.18,relwidth=0.5)

        # create label for action
        action_label = Label(fr_parameter, text="Action:", font=("Arial Bold", 9))
        action_label.place(relx=0.05,rely=0.6,relheight=.18,relwidth=0.2)

        # create lable top store action value
        action_label_var=StringVar()
        action_label_val = Label(fr_parameter, textvariable=action_label_var, bg="azure", font=("Arial Bold", 9))
        action_label_val.place(relx=0.25, rely=0.6,relheight=.18,relwidth=0.5)

        # store all the widgets from input tab in a dictionary
        self.output_wids_dict = {'ParameterFrame': fr_parameter, 'HandleLabel': handle_label,'HandleLabelValue': handle_label_val,
                                 'ActionLabel': action_label, 'ActionLabelValue': action_label_val,'HandleVar':handle_label_var,'ActionVar':action_label_var,
                                 'TableFrame': frame, 'TableCanvas': canvas, 'TableScrollBar': scroll_y,
                                 'AddTableRowButton': add_button, 'DelTableRowButton': remove_button, 'ValidateTableRowButton': validate_button}


    def output_add_button_call(self):
        # store table widgets
        frame=self.output_wids_dict['TableFrame']
        canvas = self.output_wids_dict['TableCanvas']
        scroll_y = self.output_wids_dict['TableScrollBar']

        #add rows
        self.row_num_in_output_tbl += 1
        Entry(frame, width=40).grid(column=0, row=self.row_num_in_output_tbl, sticky=NW)

        ent_output_val=Entry(frame, width=57)
        ent_output_val.grid(column=1, row=self.row_num_in_output_tbl, sticky=NW)

        output_validate_button = Button(frame, height=1)
        output_validate_button.configure(command=lambda ent_output_val=ent_output_val: self.input_row_validate_button_call(ent_output_val))
        output_validate_button.grid(column=2, row=self.row_num_in_output_tbl, sticky=NW, columnspan=1)

        # configure canvas for newly added rows
        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)
        #canvas.pack(fill='both', expand=True, side='left')
        #scroll_y.pack(fill='y', side='right')
        print("Total grids after clicking add button - output tab -frame: ",len(frame.grid_slaves()))


    def output_remove_button_call(self):
        # store table widgets
        frame = self.output_wids_dict['TableFrame']

        # create list to store all  widgets in table except to labels(because label widets are header widgets)
        widgets_list=list()
        children_widgets = frame.winfo_children() #store all the widgets in the frame(widgets include header labels and entry wwidgets)

        #Loop all the widgets in the table frame and store all the widgets except to label widget
        for child_widget in children_widgets:
            if child_widget.winfo_class() != 'Label':
                widgets_list.append(child_widget)

        # delete rows from the last row
        if len(widgets_list)>1:
            widgets_list[len(widgets_list)-1].destroy() # delete input validate button widget
            widgets_list[len(widgets_list) - 2].destroy() # delete input value entry widget
            widgets_list[len(widgets_list) - 3].destroy()  # delete input name widget

    def output_row_validate_button_call(self,output_value_entry_wid):
        frame = self.output_wids_dict['TableFrame']
        try:
            text=output_value_entry_wid.get()
            if len(text)>0:
                value=str(eval(output_value_entry_wid.get())) #evaluvate the value and store the result in value
            if len(text)==0:
                value='None'
            string="messagebox.showinfo('Input Value',message=value,parent=frame)" # show the message if the validation is succesful
            exec(string)
        except Exception as e:
            error="Error: " + str(e)
            string = "messagebox.showerror('Input Value',message=error,parent=frame)" # show the message if the eveluvation is with error
            exec(string)

    def output_validate_button_call(self):
        frame = self.output_wids_dict['TableFrame']

        #call validate output table function
        result,error_list=self.validate_output_table()
        if result=='Error':
            messagebox.showerror('Error', message='Output' + " tab: " + error_list, parent=frame)
        else:
            messagebox.showinfo('Success', message='Output' + " tab: " + "Successfully validated", parent=frame)

    def validate_output_table(self):
        frame = self.output_wids_dict['TableFrame']

        # create list to store output name value and validation error
        text_list, output_name_list, output_value_list, validation_error_list = list(), list(), list(), list()

        loop_count = 0
        children_widgets = frame.winfo_children()

        # loop all the widgets in table and store the name and value entry widgets
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                loop_count += 1
                text = child_widget.get()
                if loop_count % 2 != 0 and len(text) >= 0: output_name_list.append(
                    text)  # name widgets is in odd position of the entry widgets
                if loop_count % 2 == 0 and len(text) >= 0: output_value_list.append(
                    text)  # value widgets is in even position of the entry widgets
                if len(text) > 0: text_list.append(text)

        # Loop all the values and if any error found , store it in validation_error_list
        for each in output_value_list:
            try:
                text = str(each)
                if len(each) > 0:
                    value = str(eval(text))
                    code = "value = str(eval(text))"
                    exec(code)
            except Exception as e:
                error = "Error: " + str(e)
                validation_error_list.append(error)

        # validate input name
        loop_count = 0
        for each in output_name_list:
            loop_count += 1
            # check name is missing in any row
            if len(each) == 0:
                validation_error_list.append('Output' + ' name Missing in line: ' + str(loop_count))

            # check any name is duplicated
            if output_name_list.count(each) > 1:
                validation_error_list.append('Output' + " name Duplicated in line " + str(loop_count))
                # messagebox.showinfo('Error', message="Input/Output Name Duplicated: "+each, parent=frame)
                # break

        # check the errors in validation_error_list and show the message
        if len(validation_error_list) > 0:
            return 'Error',", ".join(validation_error_list)
        else:
            return 'Success', ", ".join(validation_error_list)


class Code(Output):

    def __init__(self,handler_studio_notebook):
        super().__init__(handler_studio_notebook)
        #self.db=self.database
        primary_db = r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
        secondary_db = r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
        db = Database.database(primary_db, secondary_db)

    def code_tab_gui(self):
        hs_tab_wids_dict=self.hs_tab_wids_dict # store tabs widgets inherited from HandlerStudio Class
        code_tab=hs_tab_wids_dict['CodeTab'] #store code tab widget

        #create main frame
        main_frame = Frame(code_tab,bg='snow')
        main_frame.place(relx=0.15, rely=0.1, height=500, width=800)

        #create text box
        txt = scrolledtext.ScrolledText(main_frame, undo=True,)
        txt['font'] = ('consolas', '12')
        txt.place(relx=.005, rely=.05, relheight=.9, relwidth=.9)

        # create debug button
        debug_button = Button(main_frame, text="Debug", width=7,command=lambda: self.code_debug_button_call())
        debug_button.place(relx=.913, rely=.1)

        #create run button
        run_button = Button(main_frame, text="Run", width=7,command=lambda: self.code_run_button_call())
        run_button.place(relx=.913, rely=.16)

        # create save button
        save_button = Button(main_frame, text="Save", width=7,command=lambda: self.code_save_button_call())
        save_button.place(relx=.913, rely=.22)

        #sore widgets in code widgets dictionary
        self.code_wids_dict = {'CodeTextbox': txt,'DebugButton': debug_button, 'RunButton': run_button, 'SaveButton': save_button}

    def code_debug_button_call(self):
        self.module_validate_button_call()
        self.input_validate_button_call()
        self.output_validate_button_call()

    def code_run_button_call(self):
        hs_tab_wids_dict = self.hs_tab_wids_dict  # store tabs widgets inherited from HandlerStudio Class
        code_tab = hs_tab_wids_dict['CodeTab']  # store code tab widget
        # store table widgets

        error_list=self.validate_all_tables()
        if len(''.join(error_list))>0:
            messagebox.showerror('Error', message= ','.join(error_list), parent=code_tab)
            return


        # import all table dictionaries
        module_table_dict=self.create_module_table_dict()
        input_table_dict=self.create_input_table_dict()
        output_table_dict=self.create_output_table_dict()
        code_dict=self.create_code_dict()

        outcome_dict={} # create a dictionary to store the outcome of the run

        #create string to store scripts for module, input ,output an dcode
        module_script,input_script,output_script,code_script='','','',''

        # create module script
        for each in module_table_dict:
            module_script=module_script + '\n\timport ' + module_table_dict[each]['ModuleName']

        # create input script
        for each in input_table_dict:
            if input_table_dict[each]['InputValue']=='':
                InputValue='str()'
            else:
                InputValue=input_table_dict[each]['InputValue']
            input_script=input_script + '\n\t\t' + input_table_dict[each]['InputName'] + "=" + InputValue

        # create output script
        for each in output_table_dict:
            if output_table_dict[each]['OutputValue']=="":
                OutputValue='str()'
            else:
                OutputValue=output_table_dict[each]['OutputValue']
            output_script=output_script + '\n\t\t' + output_table_dict[each]['OutputName'] + "=" + OutputValue
            outcome_dict[output_table_dict[each]['OutputName']]=''

        # create code script
        for each in code_dict:
            code_script=code_script + '\n\t\t' + code_dict[each]

        # create function combining module,input,output and code script
        function = "\n\t#import modules" + module_script + "\n\tdef function():\n\n\t\t#input" + input_script + \
                   "\n\n\t\t#output" + output_script + "\n\n\t\t#code" + code_script

        # create function script by adding try and except block
        function_script = '\ntry:\n\t' + function + \
                          "\nexcept Exception as e:\n\terror='Error: Error in running the action as:'" + '+ str(e)' \
                            "\n\tmessagebox.showerror('Error',error,parent=self.handler_studio_notebook)"


        #add try block in manin script
        script_TryPortion= "\ntry:\n\toutcome=function()\n\tloop_count=0" \
                           "\n\tfor each in outcome_dict:\n\t\toutcome_dict[each] = outcome[loop_count]" \
                           "\n\t\tloop_count+=1\n\tmessagebox.showinfo('Result',outcome_dict,parent=self.handler_studio_notebook)"


        #add exception block in main script
        script_ExceptionPortion="\nexcept Exception as e:\n\terror='Error: Error in running the action as:'" + '+ str(e)' \
                                "\n\tmessagebox.showerror('Error',error,parent=self.handler_studio_notebook)"

        # create main script by combining function_script,script_TryPortion and script_ExceptionPortion
        script=function_script+script_TryPortion+script_ExceptionPortion

        print('script in runn button call in handler studio-code screen\n',script)

        #excute script
        exec(script)

    def validate_all_tables(self):
        #call all validate table function
        result_module,error_list_module=self.validate_module_table()
        result_input,error_list_input=self.validate_input_table()
        result_output, error_list_output = self.validate_output_table()

        error_list=[] # create list to store all error list
        #append all error list into error list
        error_list.append(error_list_module)
        error_list.append(error_list_input)
        error_list.append(error_list_output)
        print('error_list: ',error_list)

        return error_list

    def create_module_table_dict(self):
        table_frame=self.module_wids_dict['TableFrame']

        module_table_dict = {}  # create dictionary to store module name and module path by rows
        childs_table_frame = table_frame.winfo_children() # store all the widgets from mkdule table frame(table frame consist of header label as well)

        entry_wids_list=[] # create list to store all entry widgets


        # append widget into entry_wids_list
        for each_widget in childs_table_frame:
            if each_widget.winfo_class()=='Entry' :
                entry_wids_list.append(each_widget)

        # create  module table dictionary
        loop_count = 0
        row_num=0
        for each_wid in entry_wids_list:
            loop_count += 1
            if loop_count % 2 == 0:
                continue
            if loop_count % 2 != 0:
                row_num += 1
                name = each_wid.get() #
                path=entry_wids_list[loop_count].get()
                module_table_dict[row_num]=({'ModuleName':name,'ModulePath':path})



        return module_table_dict

    def create_input_table_dict(self):
        table_frame = self.input_wids_dict['TableFrame']

        input_table_dict = {}  # create dictionary to store input name and value by rows
        childs_table_frame = table_frame.winfo_children()  # store all the widgets from input table frame(table frame consist of header label as well)

        entry_wids_list = []  # create list to store all entry widgets
        # append widget into entry_wids_list
        for each_widget in childs_table_frame:
            if each_widget.winfo_class() == 'Entry':
                entry_wids_list.append(each_widget)

        # create  module table dictionary
        loop_count = 0
        row_num = 0
        for each_wid in entry_wids_list:
            loop_count += 1

            if loop_count % 2 == 0:
                continue
            if loop_count % 2 != 0:
                row_num += 1
                name = each_wid.get()  #
                value = entry_wids_list[loop_count].get()
                input_table_dict[row_num] = ({'InputName': name, 'InputValue': value})

        return input_table_dict

    def create_output_table_dict(self):
        table_frame = self.output_wids_dict['TableFrame']

        output_table_dict = {}  # create dictionary to store output name and value by rows
        childs_table_frame = table_frame.winfo_children()  # store all the widgets from output table frame(table frame consist of header label as well)

        entry_wids_list = []  # create list to store all entry widgets
        # append widget into entry_wids_list
        for each_widget in childs_table_frame:
            if each_widget.winfo_class() == 'Entry':
                entry_wids_list.append(each_widget)

        # create  module table dictionary
        loop_count =0
        row_num = 0
        for each_wid in entry_wids_list:
            loop_count += 1

            # donot consider loop if the entry widget is in even position of list
            if loop_count % 2 == 0:
                continue
            # if the loop count is an odd number
            if loop_count % 2 != 0:
                row_num += 1 # add the row number
                name = each_wid.get()  # # get the name
                value = entry_wids_list[loop_count].get() #get the value
                output_table_dict[row_num] = ({'OutputName': name, 'OutputValue': value}) # append to dictionary

        return output_table_dict

    def create_code_dict(self):
        code_textbox = self.code_wids_dict['CodeTextbox']
        code=code_textbox.get('1.0', END).splitlines()
        code_dict = {}  # create dictionary to store code by lines


        row_num=1
        for each_line in code:
            code_dict[row_num]=each_line
            row_num+=1

        return code_dict

    def code_save_button_call(self):
        hs_tab_wids_dict = self.hs_tab_wids_dict  # store tabs widgets inherited from HandlerStudio Class
        code_tab = hs_tab_wids_dict['CodeTab']  # store code tab widget
        table_frame = self.module_wids_dict['TableFrame'] # store frame to show message
        # store table widgets

        error_list = self.validate_all_tables()
        print(','.join(error_list))
        if len(''.join(error_list)) > 0:
            messagebox.showerror('Error', message=','.join(error_list), parent=code_tab)
            return

        # import all table dictionaries
        module_table_dict = self.create_module_table_dict()
        input_table_dict = self.create_input_table_dict()
        output_table_dict = self.create_output_table_dict()
        code_dict = self.create_code_dict()

        handle=self.module_wids_dict['HandleVar'].get() #get the handle value

        # perform below activity if the handle is Create New Handle
        if handle == "Create New Handle":
            new_handle = self.module_wids_dict['NewHandleEntry'].get()
            new_action = self.module_wids_dict['NewActionEntry'].get()

            result,message=db.create_new_handle(handler=new_handle,action=new_action,module=module_table_dict,
                                                           input=input_table_dict,output=output_table_dict,code=code_dict)

            if result=='Error':
                messagebox.showerror('Error', message, parent=table_frame)
            else:
                messagebox.showinfo('Success', message, parent=table_frame)

        # perform below activity if the handle is not Create New Handle
        elif handle != "Create New Handle":
            action= self.module_wids_dict['ActionVar'].get()
            if action=="Create New Action":
                new_action=self.module_wids_dict['NewActionEntry'].get()

                result, message = db.create_new_handle(handler=handle, action=new_action,module=module_table_dict,
                                                                  input=input_table_dict, output=output_table_dict,code=code_dict)

                if result == 'Error':
                    messagebox.showerror('Error', message, parent=table_frame)
                else:
                    messagebox.showinfo('Success', message, parent=table_frame)

            if action != "Create New Action":

                result, message = db.update_action(handler=handle, action=action,module=module_table_dict,
                                                                  input=input_table_dict, output=output_table_dict,code=code_dict)

                if result == 'Error':
                    messagebox.showerror('Error', message, parent=table_frame)
                else:
                    messagebox.showinfo('Success', message, parent=table_frame)


primary_db=r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
secondary_db=r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
db=Database.database(primary_db,secondary_db)
main=MainWindow(primary_db,secondary_db)
main.main_frame()