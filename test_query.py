from tinydb import TinyDB, Query
db = TinyDB(r"C:\Users\Dell\Documents\HK Project GUI\Autom Database\database.json")
import  re

x='=&dummy&'
a=re.findall("^=&.*&$",x)
print(a)

'''q=Query()
x=table_handle_studio.search(q.object_name=='web_handle6')
if len(x)==0:
    table_handle_studio.insert({'object_name': 'web_handle6', 'actions':[{'action_name':'open_website','input':{'input1':"input_v1",'n2':'v2'}}]})
else:
    print("object has already been created")

table_handle_studio.insert({'object_name': 'web_handle13', 'action':'open_website','input':"\n\tn1=10\n\tn2='test'",'output':"\n\to1=''",'code':"\ndef " ""})



#table_handle_studio.update({'actions':[{'action_name':'open_website_added','input':{'input1':"input_v1",'n2':'v2'}}]},q.object_name=='web_handle6')

x=table_handle_studio.search((q.object_name=='web_handle13') & (q.action=='open_website'))
print(x)
print(len(x))
print(x[0]['input'])
print(x[0]['output'])
input=x[0]['input'].split(";")
print(input)'''


