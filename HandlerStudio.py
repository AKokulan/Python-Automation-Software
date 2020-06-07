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

    def __init__(self, db):
        self.num_rows = 4
        self.database = db
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

        module=Module(handler_studio_notebook)
        module.handler_studio()
        module.module_tab_gui()

        '''process_studio_notebook = ttk.Notebook(process_studio_frame_tab)
        process_studio_notebook.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

        os=ObjectStudio(self.root,db,object_studio_notebook)
        os.object_studio()

        ps=ProcessStudio.ProcessStudio(process_studio_notebook,self.database)
        ps.process_studio()

        #return object_studio_notebook,process_studio_notebook

        #self.object_studio(object_studio_notebook)'''


class HandlerStudio:

    def __init__(self,handler_studio_notebook):
        self.x=100
        self.handler_studio_notebook=handler_studio_notebook
        self.hs_tab_wids_dict = {'ModuleTab': '', 'InputTab': '', 'OutputTab': '','CodeTab': ''} # store all the tabs widgets into a session variable

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
        self.module_wids_dict={'ParameterFrame':'','HandleLabel':'','HandleOptionMenu':'','TableFrame':'','HandleVar':'',
                               'ActionLabel':'','ActionOptionMenu':'','ActionVar':'',
                               'TableCanvas':'','TableScrollBar':'','AddTableRowButton':'','DelTableRowButton':'',
                               'ValidateTableRowButton':''}
        print("x is : ",self.x)

    def module_tab_gui(self):
        hs_tab_wids_dict=self.hs_tab_wids_dict # store tabs widgets inherited from HandlerStudio Class
        module_tab=hs_tab_wids_dict['ModuleTab'] #store module tab widget

        #create parent frame in module tab
        parent = Frame(module_tab)
        parent.place(relx=0.2, rely=0.31, relheight=.4, relwidth=0.501)

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
        add_button = Button(module_tab, text='Add',command=lambda:self.module_add_button_call())
        add_button.place(relx=.703, rely=.32, relheight=.03, relwidth=.05)
        remove_button = Button(module_tab, text='Remove',command=lambda:self.module_remove_button_call())
        remove_button.place(relx=.703, rely=.36, relheight=.03,relwidth=.05)
        validate_button = Button(module_tab, text='Validate',command=lambda:self.module_validate_button_call())
        validate_button.place(relx=.703, rely=.40, relheight=.03,relwidth=.05)

        #create frame for parameters to place the widgets such as ahndle and action
        fr_parameter = Frame(module_tab)
        fr_parameter.place(relx=0.2, rely=0.1, relheight=.20, relwidth=0.5)

        #create handle label on parameter frame
        handle_label = Label(fr_parameter, text="Handle:",font=("Arial Bold", 9))
        handle_label.place(relx=0.05, rely=0.2, relheight=.18, relwidth=0.2)

        # create option menue for handles on parameter5 frame
        handle_var = StringVar(fr_parameter)
        choices = ["Create New Handle",'#NA']
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

        #creare list to store module name, path and validation error
        text_list,modue_name_list,module_path_list,validation_error_list=list(),list(),list(),list()

        loop_count=0
        children_widgets = frame.winfo_children() #store all the widgets in the frame(widgets include header labels and entry wwidgets)

        # Loop widgets in table frame and the widget is entry, get the value to append in module name and path list
        for child_widget in children_widgets:
            loop_count+=1
            if child_widget.winfo_class() == 'Entry':
                text=child_widget.get() # get the value from entry box
                if loop_count%2!=0 and len(text)>0:modue_name_list.append(text) # if the entry widget in odd position, it is a module name
                if loop_count % 2 == 0 and len(text)>0: module_path_list.append(text) # if the entry widget in even position, it is a module name
                #if len(text)>0:text_list.append(text)

        # validation for module path will be used in future. Find the validation
        '''if len(module_path_list)>len(modue_name_list):validation_error_list.append("Module name missing for a given module path")
        for each in module_path_list:
            if os.path.exists(each)==False:validation_error_list.append("Module path not exist: " + each )
        if len(validation_error_list)>0:messagebox.showerror("Error",validation_error_list,parent=frame)'''

        # validate module name and if the module is not available , add it to validation_error_list
        for each in modue_name_list:
            script = "try:\n\timport " + each + "\nexcept:\n\tvalidation_error_list.append(each)"
            #below code depreciated
            #script="try:\n\timport " + each  + "\n\tmessagebox.showinfo('Success','All modules successfuly validated',parent=frame)" +"\nexcept:\n\tmessagebox.showerror('Error'," + "'"+ "Module is not available: " + each + "'," + "parent=frame)  "
            exec(script)

        #show the error if there error in validation_error_list, else show succes message
        if len(validation_error_list)>0:
            messagebox.showerror("Error","Moduels are not available: " + ','.join(validation_error_list),parent=frame )
        else:
            messagebox.showinfo('Success','All modules successfuly validated',parent=frame)

    def module_handle_refresh_call(self):

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
            action_choices = ["Create New Action",'#NA']
            action_menu = OptionMenu(parameter_frame, action_value_var, *action_choices)
            action_menu.configure(bg='snow')
            action_menu.place(relx=0.25, rely=0.45,relheight=.24, relwidth=0.5)
            self.module_wids_dict['ActionOptionMenu'] = action_menu
            self.module_wids_dict['ActionVar'] = action_value_var

            # trace the value change for action
            def module_action_refresh_call(*args):self.module_action_refresh_call()
            action_value_var.trace("w", module_action_refresh_call)

        self.clear_module_table()

    def module_action_refresh_call(self):

        #store widgets in module
        parameter_frame = self.module_wids_dict['ParameterFrame']
        action_var = self.module_wids_dict['ActionVar']
        option_value = action_var.get()

        # perform below activity if the action is 'Create New Action'
        if option_value == 'Create New Action':

            #create new action label
            new_action_label = Label(parameter_frame, text="New Action:", font=("Arial Bold", 9))
            new_action_label.place(relx=0.05, rely=0.74,relheight=.18,relwidth=0.2)
            self.module_wids_dict['NewActionLabel'] = new_action_label

            #create new action entry
            new_action_entry = Entry(parameter_frame)
            new_action_entry.place(relx=0.25, rely=0.74,  relwidth=0.5)
            self.module_wids_dict['NewActionEntry'] = new_action_entry

        # destory NewActionLabel and NewActionEntry widgets , if the other value is selected in action
        else:
            if self.module_wids_dict['NewActionLabel']!='':self.module_wids_dict['NewActionLabel'].destroy()
            self.module_wids_dict['NewActionLabel'] = ''
            if self.module_wids_dict['NewActionEntry'] != '': self.module_wids_dict['NewActionEntry'].destroy()
            self.module_wids_dict['NewActionEntry'] = ''

        self.clear_module_table()

    def clear_module_table(self):
        table_frame = self.module_wids_dict['TableFrame']
        # clear text in module tab table
        child_widgets_table_frame = table_frame.winfo_children()
        for each in child_widgets_table_frame:
            if each.winfo_class() == 'Entry':
                each.delete(0, END)

        # clear entry boxes in input and output tabs
        '''table_frame_os_input_tab = (
        ((object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
        table_frame_os_output_tab = (
        ((object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0])
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

        self.load_os_module_action_optionmenu(object_studio_module_tab, object_studio_input_tab,
                                              object_studio_output_tab, object_studio_code_tab)'''

primary_db=r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
main=MainWindow(primary_db)
main.main_frame()