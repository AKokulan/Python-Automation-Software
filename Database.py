from tinydb import TinyDB, Query
from tkinter import messagebox
class database:

    def __init__(self,Primarydatabase,SecondaryDatabase):
        self.p_db_path=Primarydatabase
        self.p_db = TinyDB(self.p_db_path)
        self.p_handler_table=self.p_db.table('HandlerStudio')
        self.p_process_table = self.p_db.table('ProcessStudio')

        self.s_db_path=SecondaryDatabase
        self.s_db = TinyDB(self.s_db_path)
        self.s_handler_table=self.s_db.table('HandlerStudio')
        self.s_process_table = self.s_db.table('ProcessStudio')

    def create_new_handler_action_in_primary_databse(self,frame,handler,module,action,input,output,code):
        try:
        #primary database
            query = Query()
            _action = self.p_handler_table.search((query.handler == handler) & (query.action == action))
            _handle_module = self.p_handler_table.search((query.handler == handler) & (query.type == 'module'))
            if len(_action)>0:
                messagebox.showerror('Error',"Handler with action already exist",parent=frame)
            else:
                self.p_handler_table.insert({'handler': handler,'type':'action' ,'action':action,'input':input,'output':output,'code':code})
                if len(_handle_module[0]['module'])==0:
                    self.p_handler_table.insert({'handler': handler, 'type': "module", 'module': module})
                else:
                    existing_modules=_handle_module[0]["module"]
                    print("existing module:",existing_modules)
                    if module not in existing_modules:
                        new_modules = existing_modules + module
                        self.p_handler_table.update({'module':new_modules }, ((query.handler==handler) & (query.type == 'module')) )
                        print("new modules: " + new_modules)
                messagebox.showinfo("Success", "New handler-action Created", parent=frame)
        except Exception as e:
            messagebox.showerror("Error", "Error in creating handler-action as: " + str(e), parent=frame)

    def create_new_handler_action_in_secondary_databse(self, frame, handler, module, action, input, output, code):
        #secondary database
        try:
            query = Query()
            _action = self.s_handler_table.search((query.handler == handler) & (query.action == action))
            _handle_module = self.s_handler_table.search((query.handler == handler) & (query.type == 'module'))
            if len(_action)>0:
                messagebox.showerror('Error',"Handler with action already exist",parent=frame)
            else:
                self.s_handler_table.insert({'handler': handler,'type':'action' ,'action':action,'input':input,'output':output,'code':code})
                if len(_handle_module[0]['module'])==0:
                    self.s_handler_table.insert({'handler': handler, 'type': "module", 'module': module})
                else:
                    existing_modules=_handle_module[0]["module"]
                    print("existing module:",existing_modules)
                    if module not in existing_modules:
                        new_modules = existing_modules + module
                        self.s_handler_table.update({'module':new_modules }, ((query.handler==handler) & (query.type == 'module')) )
                        print("new modules: " + new_modules)
        except Exception as e:
            return "Error", "Error in creating handler-action in secondary database as: " + str(e)

    def retrive_action_document_from_primary_databse(self, frame, handler, action):
        query = Query()
        action_doc = self.p_handler_table.search((query.handler == handler) & (query.action == action))
        handle_module_doc = self.p_handler_table.search((query.handler == handler) & (query.type == 'module'))
        print(action_doc)
        print(handle_module_doc[0]["module"])

        #format module names
        module_retrived = handle_module_doc[0]["module"]
        module = list()
        for each in (module_retrived.split("\n")):
            if len(each) != 0: module.append(each.replace("\t", ""))
        print("module: " , module)

        #format input names and values
        input_retrived = action_doc[0]["input"]
        #print(input_retrived)
        input, input_name, input_value = list(), list(), list()
        #print(input_retrived.split("\n"))
        for each_input in (input_retrived.split("\n")):
            if len(each_input) != 0:
                input_name_value_splitted = (each_input.replace("\t", "")).split("=")
                print(input_name_value_splitted)
                input.append(each_input.replace("\t", ""))
                input_name.append(input_name_value_splitted[0])

                nums = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9,', '0']
                isNum = True

                x=1 if len(input_name_value_splitted)>1 else 0
                for each in input_name_value_splitted[x]:
                    if each not in nums: isNum = False
                if isNum == True:
                    if "." in input_name_value_splitted[1]: input_value.append(float(input_name_value_splitted[x]))
                    if "." not in input_name_value_splitted[1]: input_value.append(int(input_name_value_splitted[x]))

                else:
                    input_value.append(input_name_value_splitted[x])
                    #print(input_name_value_splitted[1])
        print('input: ', input_name,input_value)

        # format output names and values
        output_retrived = action_doc[0]["output"]
        #print(output_retrived)
        output, output_name, output_value = list(), list(), list()
        #print(output_retrived.split("\n"))
        for each_output in (output_retrived.split("\n")):
            if len(each_output) != 0:
                output_name_value_splitted = (each_output.replace("\t", "")).split("=")
                print(output_name_value_splitted)
                output.append(each_output.replace("\t", ""))
                output_name.append(output_name_value_splitted[0])

                nums = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9,', '0']
                isNum = True
                x = 1 if len(output_name_value_splitted) > 1 else 0
                for each in output_name_value_splitted[x]:
                    if each not in nums: isNum = False
                if isNum == True:
                    if "." in output_name_value_splitted[1]: output_value.append(float(output_name_value_splitted[x]))
                    if "." not in output_name_value_splitted[1]: output_value.append(int(output_name_value_splitted[x]))

                else:
                    output_value.append(output_name_value_splitted[x])
                    # print(input_name_value_splitted[1])
        print('output: ', output_name, output_value)

        #format code
        code = action_doc[0]["code"]
        print("code: " , code)

        _handle_module = self.p_handler_table.search((query.handler == handler) & (query.type == 'module'))
        print("handle modules\n",_handle_module)
        print(len(_handle_module[0]['module']))

        return module, input_name, input_value, output_name, output_value, code


    def retrive_all_handles(self):
        query = Query()
        action_doc = self.p_handler_table.search(query.type == "action")
        handles=['Create New Handle']
        for each in action_doc:
            if each["handler"] not in handles:handles.append(each["handler"])
        print(action_doc)
        print(handles)
        return handles

    def retrive_action_for_handles(self,handler):
        query = Query()
        action_doc = self.p_handler_table.search((query.type == "action") & (query.handler == handler))
        actions = ['Create New Action']
        for each in action_doc:
            if each["action"] not in actions: actions.append(each["action"])
        print(action_doc)
        print(actions)
        return actions

    def retrive_input_for_action(self,handler,action):
        query = Query()
        action_doc = self.p_handler_table.search((query.type == "action") & (query.handler == handler) & (query.action == action))
        input = action_doc[0]['input']
        '''for each in action_doc:
            if each["input"] not in actions: actions.append(each["action"])'''


        print(action_doc)
        print(input)
        return input

    def retrive_output_for_action(self,handler,action):
        query = Query()
        action_doc = self.p_handler_table.search((query.type == "action") & (query.handler == handler) & (query.action == action))
        output = action_doc[0]['output']
        '''for each in action_doc:
            if each["input"] not in actions: actions.append(each["action"])'''
        print(action_doc)
        print(output)
        return output

    def retrive_code_for_action(self,handler,action):
        query = Query() # create query
        action_doc = self.p_handler_table.search((query.type == "action") & (query.handler == handler) & (query.action == action)) # retrive document that matched the type handler and action
        code = action_doc[0]['code'] # extrct code from document
        print('action doc in retrive_code_for_action: ', action_doc)
        print('code in retrive_code_for_action: ', code)
        return code # return code

    def retrive_module_for_handler(self,handler):
        query = Query() # create query
        action_doc = self.p_handler_table.search((query.type == "module") & (query.handler == handler)) # retrive document that matched the type handler
        module=[]
        if len(action_doc)>0:
            module = action_doc[0]['module'] # extrct module from document
        print('action doc in --retrive_code_for_action: ', action_doc)
        print('module in --retrive_code_for_action: ', module)
        return module # return module

    def update_action_doc_in_primary_databse(self,frame,handler,action,module,input,output,code):
        try:
            query = Query()
            action_doc = self.p_handler_table.search((query.type == "action") & (query.handler == handler) & (query.action == action))
            print(action_doc)
            print(len(action_doc))
            #db.upsert({'name': 'John', 'logged-in': True}, User.name == 'John')
            self.p_handler_table.update({'handler': handler, 'type': 'action', 'action': action, 'input': input, 'output': output, 'code': code},((query.type == "action") & (query.handler == handler) & (query.action == action)))
            self.p_handler_table.update({'module': module}, ((query.handler == handler) & (query.type == 'module')))
            messagebox.showinfo("Success", " handler-action updated", parent=frame)
        except Exception as e:
            messagebox.showerror("Error", "Error in updating handler-action as: " + str(e), parent=frame)

    def retrive_clusters(self):
        query = Query()
        process_doc = self.p_process_table.search((query.type == "process"))
        cluster = ['Create New Cluster']
        for each in process_doc:
            if each["cluster"] not in cluster: cluster.append(each["cluster"])
        print(process_doc)
        print(cluster)
        return cluster

    def retrive_process(self,cluster):
        query = Query()
        process_doc = self.p_process_table.search((query.cluster == cluster))
        process = ['Create New Process']
        for each in process_doc:
            if each["process"] not in process and each["process"]!="NA": process.append(each["process"])
        print(process_doc)
        print(process)
        return process

    def retrive_process_page(self,process):
        query = Query()
        process_doc = self.p_process_table.search((query.process == process))
        page = ['Create New Page']
        for each in process_doc:
            if each["page"] not in page and each["page"]!="NA": page.append(each["page"])
        print(process_doc)
        print(page)
        return page

    def retrive_process_page_doc(self,type,cluster,process,page):
        query = Query()
        process_doc = self.p_process_table.search((query.type == type) &(query.cluster == cluster) & (query.process == process) & (query.page == page))
        return process_doc

    def retrive_latest_page_for_page(self,type,cluster,process,page):
        query = Query()
        #retrive all the documents for the given page
        page_doc = self.p_process_table.search((query.type == type) &(query.cluster == cluster) & (query.process == process) & (query.page == page))
        existing_pages_key = [] # Create a list to store all the keys of the pages
        for each_doc in page_doc:
            existing_pages_key.append(each_doc['key']) # append the keys of the page documnts into existing_pages_key
        existing_pages_key.sort(reverse=True) # sort the key list in desending order

        latest_page_doc_key = existing_pages_key[0] # #take the first key in the list as the lates key

        # check each page document and the key match in its, take that document and return
        latest_page_doc = ''
        for each_doc in page_doc:
            if each_doc['key'] == latest_page_doc_key:
                latest_page_doc = each_doc
        print("latest page doc in --retrive_latest_page_for_page: ",latest_page_doc)
         # order the pages in asending order based on index value
        '''sorted_latest_pages=[]
        for each in range(500):
            for each_page in latest_page_doc:
                print(each_page)
                print(each_page['pageindex'])
                if int(each_page['pageindex'])==each:
                    sorted_latest_pages.append(each_page)
                    break'''


        return latest_page_doc


    def retrive_all_pages_for_process(self,type,cluster,process):
        query = Query()
        process_doc = self.p_process_table.search(
            (query.type == type) & (query.cluster == cluster) & (query.process == process))
        return process_doc

    def create_new_process_page_in_primary_databse(self,frame,key,type,cluster,process,page,pageindex,steps,outputstorein):
        #print('page is'+page)
        try:
            self.p_process_table.insert({'key': key, 'type': type, 'cluster': cluster, 'process': process,
                                         'page': page, 'pageindex': pageindex, 'steps': steps,
                                         'outputstorein': outputstorein})
            messagebox.showinfo("Success","Process Saved", parent=frame)
            '''query = Query()
            _page = self.p_process_table.search((query.type == type) &(query.cluster == cluster) & (query.process == process) & (query.page == page))
            if len(_page)>0:
                messagebox.showerror('Error',"Cluster/Process/Page  already exist",parent=frame)
            else:
                self.p_process_table.insert({'key': key,'type': type,'cluster':cluster ,'process':process,
                                             'page':page,'pageindex':pageindex,'steps':steps,'outputstorein':outputstorein})'''

        except Exception as e:
            messagebox.showerror("Error", "Error in creating Cluster/Process/Page as: " + str(e), parent=frame)

    def update_process_page_in_primary_databse(self,frame,type,cluster,process,page,handler,action,input,output,exception,status):
        try:
            query = Query()

            self.p_process_table.insert({'type': type,'cluster':cluster ,'process':process,
                                         'page':page,'handler':handler,'action':action,
                                         'input':input,'output':output,'exception':exception,'status':status},
                                        ((query.type == "process") & (query.cluster == cluster) ))

        except Exception as e:
            messagebox.showerror("Error", "Error in updating Cluster/Process/Page as: " + str(e), parent=frame)



db=database(r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomPrimaryDatabase.json",r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\AutomSecondaryDatabase.json")
#print(db.db)
#db.create_new_handler_action_in_primary_databse("frame","test_handler5","os","test_action23","test_input","test_output","test_code")
#db.create_new_handler_action_in_secondary_databse("frame","test_handler5","os","test_action23","test_input","test_output","test_code")
#db.retrive_action_document_from_primary_databse('frame',"test_handler5","test_action23")
db.retrive_action_document_from_primary_databse("","test_handler5",'open website')
#x=db.retrive_clusters()
#print(x)