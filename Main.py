from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from PIL import ImageTk, Image
import time

#import files
import Database, ObjectStudio, ProcessStudio

class Main:

    def __init__(self):
        self.startup_window()

    def startup_window(self):
        root = Tk() # Create root window
        root.overrideredirect(True) # Remove title bar
        #image = PhotoImage(file=r"C:\Users\Dell\Desktop\ROBOx\Main screen pic\https___blogs-images.forbes.com_bernardmarr_files_2019_06_Hitachi-1200x800.jpg")
        w,h=600,400
        # Create image object for .jpg type image
        image=Image.open(r"C:\Users\Dell\Desktop\ROBOx\Main screen pic\https___blogs-images.forbes.com_bernardmarr_files_2019_06_Hitachi-1200x800.jpg")
        image = image.resize((w, h)) # Resize image same as start up windows's height and width
        image = ImageTk.PhotoImage(image)

        #Create start up button image
        start_button_image = Image.open(r"C:\Users\Dell\Desktop\ROBOx\Main screen pic\start button.jpg")
        start_button_image = start_button_image.resize((20,20))
        start_button_image = ImageTk.PhotoImage(start_button_image)


        cn=Canvas(root,bg='red') # Create Canvas in start up window
        cn.pack(side = LEFT,fill=BOTH, expand = True)
        #cn.create_image(50, 10, image=start_button_image, anchor=NW)# Create image in Canvas
        '''button=Button(cn,image=start_button_image,command=lambda x=root:self.call_main_window(x)) #Create start up button
        button.pack()'''

        # get screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        cn.create_image(0, 0, image=image, anchor=NW)

        #time.sleep(5)
        root.after(3000, lambda x=root: self.call_main_window(x))
        #self.import_files(root)
        root.mainloop()

    def import_files(self,root_startup):
        import Database, ObjectStudio, ProcessStudio
        time.sleep(3)
        root_startup.destroy()
        self.call_main_window(root_startup)


    def call_main_window(self,startup_window):
        startup_window.destroy() #Destory start up window

        # Create databases
        primary_db=r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json"
        secondary_db=r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomSecondaryDatabase.json"

        db = Database.database(primary_db,secondary_db) #Create Databaswe object
        self.main_frame(db) #call mainframe from mainwindow

    def main_frame(self,db):
        root = Tk()
        root.title('AIx - Empower ROBOT with Artificial Intelligence')
        root.iconbitmap(r"C:\Users\Dell\Desktop\ROBOx\Main screen pic\icon.ico")
        #self.root.geometry("200x200")
        root.resizable(0, 0)
        w=800
        h=534
        # get screen width and height
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        print("windows width and height in --main_fram call:",ws,hs)
        # calculate position x, y
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        main_frame=Frame(root,bg='midnight blue')
        main_frame.pack(expand=True,fill=BOTH)
        inner_main_frame=Canvas(main_frame,bg='snow')
        inner_main_frame.place(relx=.004, rely=.004, relwidth=.992, relheight=.992)



        header_frame=Frame(inner_main_frame,bg='steel blue')
        header_frame.place(relx=.006, rely=.007, relwidth=.988, relheight=.07)

        home_label = Label(header_frame, text="Home", relief=RAISED)
        home_label.place(relx=.003, rely=.06, width=200, height=34)

        rpa_label=Label(header_frame,text="Robotic Process Automation",relief=RAISED,fg="black")
        rpa_label.place(relx=.259, rely=.06, width=200, height=34)

        ia_label = Label(header_frame, text="Intelligent Automation", relief=GROOVE)
        ia_label.place(relx=.514, rely=.06, width=200, height=34)

        configuration_label = Label(header_frame, text="Configuration", relief=GROOVE)
        configuration_label.place(relx=.77, rely=.06, width=180, height=34)

        home_frame = Canvas(inner_main_frame, bg='red')
        rpa_frame = Canvas(inner_main_frame, bg='snow')
        ia_frame = Canvas(inner_main_frame, bg='snow')

        image = Image.open(
            r"C:\Users\Dell\Desktop\ROBOx\Main screen pic\https___blogs-images.forbes.com_bernardmarr_files_2019_06_Hitachi-1200x800.jpg")
        # image = Image.open(r"C:\Users\Dell\Desktop\ROBOx\Main screen pic\start button.jpg")
        image = image.resize((w, h))  # Resize image same as start up windows's height and width
        image = ImageTk.PhotoImage(image)
        print(image)

        home_frame.create_image(0, 0, image=image, anchor=NW)  # Create image in Canvas

        #rpa_frame.create_line(2, 58, 800, 58, fill="steel blue", width=10)  # Create left line in run process

        def home_tab_call(*kwrgs): self.home_tab_call(home_frame,rpa_frame, ia_frame, home_label,rpa_label, ia_label)
        def rpa_label_call(*kwrgs):self.rpa_label_call(home_frame,rpa_frame,ia_frame,home_label,rpa_label,ia_label,root,db)
        def ia_label_call(*kwrgs): self.ia_label_call(home_frame,rpa_frame,ia_frame,home_label,rpa_label, ia_label)

        home_label.bind('<Button-1>', home_tab_call)
        rpa_label.bind('<Button-1>',rpa_label_call)
        ia_label.bind('<Button-1>', ia_label_call)


        self.home_tab_call(home_frame,rpa_frame, ia_frame, home_label,rpa_label, ia_label)


        '''button1 = Button(root, text="open new window", command= lambda x=root,y=db:self.studio_window(x,y))
        button1.place(x=50, y=25, width=100, height=25)'''
        root.mainloop()

    def rpa_label_call(self,home_frame,rpa_frame, ia_frame, home_label,rpa_label, ia_label,root,db):
        rpa_label.configure(relief=RAISED,font=("Arial Bold", 10))
        ia_label.configure(relief=GROOVE,font=("Arial", 10))
        home_label.configure(relief=GROOVE,font=("Arial", 10))
        home_frame.place_forget()
        ia_frame.place_forget()

        rpa_frame.place(relx=.004, rely=.12, relwidth=.992, relheight=.992)
        rpa_frame.create_line(2, 2, 800, 2, fill="steel blue", width=10)  # Create left line in run process

        run_frame=Canvas(rpa_frame,bg='steel blue')
        run_frame.place(relx=.1, rely=.05, relwidth=.6, relheight=.75)

        run_frame.create_line(30, 25, 30, 250, fill="snow", width=3) # Create left line in run process
        run_frame.create_line(450, 25, 450, 250, fill="snow", width=3)# Create right line in run process
        run_frame.create_line(30, 25, 50, 25, fill="snow", width=3) # Create top line-first half in run process
        lb_run_line = Label(run_frame, text="Run Panel", bg='steel blue', font=("Arial Bold", 10), anchor="w",fg="snow")
        lb_run_line.place(x=50, y=10, width=75, height=30)
        run_frame.create_line(125, 25, 450, 25, fill="snow", width=3)  # Create top line-second half in run process
        run_frame.create_line(30, 250, 450, 250, fill="snow", width=3) # Create bottom line in run proces


        lb_cluster=Label(run_frame,text="Cluster:",bg='steel blue',font=("Arial Bold", 10),anchor="e")
        lb_cluster.place(relx=.1, rely=.1, width=100, height=30)

        var_cluster=StringVar()
        cluster_choices=["Sample Cluster"]
        om_cluster=OptionMenu(run_frame,var_cluster,*cluster_choices)
        om_cluster.place(relx=.35, rely=.1, width=250, height=30)

        lb_process=Label(run_frame,text="Process:",bg='steel blue',font=("Arial Bold", 10),anchor="e")
        lb_process.place(relx=.1, rely=.19, width=100, height=30)

        var_process=StringVar()
        process_choices=["Sample Process:"]
        om_process=OptionMenu(run_frame,var_process,*process_choices)
        om_process.place(relx=.35, rely=.19, width=250, height=30)

        lb_scheduler=Label(run_frame,text="Scheduler:",bg='steel blue',font=("Arial Bold", 10),anchor="e")
        lb_scheduler.place(relx=.1, rely=.28, width=100, height=30)

        var_shedule_date=StringVar()
        sb_sheduler_date = Spinbox(run_frame, from_=00, to=31, validate="all", textvariable=var_shedule_date)
        sb_sheduler_date.place(relx=0.35, rely=0.285, width=35)

        var_shedule_month = StringVar()
        sb_scheduler_month = Spinbox(run_frame, from_=00, to=12, validate="all", textvariable=var_shedule_month)
        sb_scheduler_month.place(relx=0.43, rely=0.285, width=35)

        var_shedule_year = StringVar()
        sb_scheduler_year = Spinbox(run_frame, from_=2020, to=2050, validate="all", textvariable=var_shedule_year)
        sb_scheduler_year.place(relx=0.51, rely=0.285, width=40)

        ld_dass=Label(run_frame,text="-",bg='steel blue',font=("Arial Bold", 10),anchor="e")
        ld_dass.place(relx=0.6, rely=0.285, width=30)

        var_shedule_hour = StringVar()
        sb_scheduler_hour = Spinbox(run_frame, from_=00, to=24, validate="all", textvariable=var_shedule_hour)
        sb_scheduler_hour.place(relx=0.63, rely=0.285, width=35)

        var_shedule_minute = StringVar()
        sb_scheduler_minute = Spinbox(run_frame, from_=00, to=60, validate="all", textvariable=var_shedule_minute)
        sb_scheduler_minute.place(relx=0.71, rely=0.285, width=35)

        var_shedule_sec = StringVar()
        sb_scheduler_sec = Spinbox(run_frame, from_=00, to=60, validate="all", textvariable=var_shedule_sec)
        sb_scheduler_sec.place(relx=0.79, rely=0.285, width=35)

        lb_robots=Label(run_frame,text="Robots:",bg='steel blue',font=("Arial Bold", 10),anchor="e")
        lb_robots.place(relx=.1, rely=.37, width=100, height=30)

        var_robots=StringVar()
        robots_choices=["Sample Process:"]
        om_robots=OptionMenu(run_frame,var_robots,*robots_choices)
        om_robots.place(relx=.35, rely=.37, width=250, height=30)

        bt_run=Button(run_frame,text="Run")
        bt_run.place(relx=.72, rely=.49, width=75, height=30)






        options_frame=Frame(rpa_frame,bg='steel blue')
        options_frame.place(relx=.7, rely=.05, relwidth=.29, relheight=.75)

        inner_options_frame=Frame(options_frame,bg='snow')
        inner_options_frame.place(relx=.004, rely=.004, relwidth=.992, relheight=.992)

        lb_queue=Label(inner_options_frame,text="Queue")
        lb_queue.place(relx=.025, rely=.05, width=200, height=30)

        lb_environemt_var=Label(inner_options_frame,text="Environment Variable")
        lb_environemt_var.place(relx=.025, rely=.15, width=200, height=30)

        lb_studio=Label(inner_options_frame,text="Studio")
        lb_studio.place(relx=.025, rely=.25, width=200, height=30)

        def studio_call(*kwrgs):self.studio_window(root,db)
        lb_studio.bind('<Button-1>', studio_call)

        lb_application_moduler = Label(inner_options_frame, text="Application Moduler")
        lb_application_moduler.place(relx=.025, rely=.35, width=200, height=30)

        lb_robots = Label(inner_options_frame, text="Robots")
        lb_robots.place(relx=.025, rely=.45, width=200, height=30)

        lb_session_log = Label(inner_options_frame, text="Sessions Log")
        lb_session_log.place(relx=.025, rely=.55, width=200, height=30)

        lb_scheduler = Label(inner_options_frame, text="Scheduler")
        lb_scheduler.place(relx=.025, rely=.65, width=200, height=30)

    def ia_label_call(self,home_frame,rpa_frame, ia_frame, home_label,rpa_label, ia_label):
        home_label.configure(relief=GROOVE,font=("Arial", 10))
        rpa_label.configure(relief=GROOVE,font=("Arial", 10))
        ia_label.configure(relief=RAISED,font=("Arial Bold", 10))
        home_frame.place_forget()
        rpa_frame.place_forget()
        ia_frame.place(relx=.004, rely=.12, relwidth=.992, relheight=.992)
        ia_frame.create_line(2, 2, 800, 2, fill="steel blue", width=10)  # Create left line in run process

    def home_tab_call(self,home_frame,rpa_frame, ia_frame, home_label,rpa_label, ia_label):
        rpa_label.configure(relief=GROOVE,font=("Arial", 10))
        ia_label.configure(relief=GROOVE,font=("Arial", 10))
        home_label.configure(relief=RAISED,font=("Arial Bold", 10))
        #if str(rpa_frame)!="":   rpa_frame.destroy()
        rpa_frame.place_forget()
        ia_frame.place_forget()
        home_frame.place(relx=.01, rely=.12, relwidth=.98, relheight=.85)


    def studio_window(self,root,db):  # new window definition
        studio_window = Toplevel(root) # Create studio window
        studio_window.title('Studio') # Set window title for studio window
        studio_window.iconbitmap(r"C:\Users\Dell\PycharmProjects\CTA-GUI\Images\icon.ico") # Set window icon
        #newwin.resizable(0, 0)
        studio_window.state('zoomed') # Set studio window in maximised state

        style = ttk.Style(studio_window) # Create style for studio window
        style.configure('lefttab.TNotebook', tabposition='wn') # Set the tab position for notebook as left
        nb = ttk.Notebook(studio_window, style='lefttab.TNotebook') #creat studio notebook
        nb.place(x=0,y=0,relheight=1,relwidth =1)

        # Make 1st tab
        object_studio_frame_tab = Frame(nb) # Create a frame -object_studio_frame_tab which needs to be added as tab in note book
        nb.add(object_studio_frame_tab, text="Object Studio") # Add the frame -object_studio_frame_tab as a tab in notebook

        # Make 2nd tab
        process_studio_frame_tab = Frame(nb)# Create a frame -process_studio_frame_tab which needs to be added as tab in note book
        nb.add(process_studio_frame_tab, text="Process Studio")# Add the frame -process_studio_frame_tab as a tab in notebook

        nb.select(object_studio_frame_tab) # Make Object studio tab as selected tab when open the stoduio notebook

        object_studio_notebook = ttk.Notebook(object_studio_frame_tab)
        object_studio_notebook.place(relx=0.01,rely=0.01,relheight=0.98,relwidth =0.98)

        process_studio_notebook = ttk.Notebook(process_studio_frame_tab)
        process_studio_notebook.place(relx=0.01, rely=0.01, relheight=0.98, relwidth=0.98)

        os=ObjectStudio.ObjectStudio(root,db,object_studio_notebook) # Create ObjectStudio object
        ps = ProcessStudio.ProcessStudio(process_studio_notebook, db) # Create ProcessStudio object

        os.object_studio() # Call object_studio function
        ps.process_studio() # call process_studio function


main= Main()
