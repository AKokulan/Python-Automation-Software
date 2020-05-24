'''try:
    import o
except:
    print("OS no found")

module='os'
x="try:\n\timport " + module +"\nexcept:\n\tmessagebox.showerror('Error'," + "'"+ "Module not installed: " + module + "'," + "parent=frame)  "
print(x)'''

#web_handle_dict={'module':{'os':'c\\test','openpyxl':'c\\test\\done'},'Action':{'input':{'var1':10,'var2':'testvar'},'output':{'o1':1,'o2':10}}}

#print(web_handle_dict['module']['os'])

'''file=open(r"C:\Dell\Documents\HK Project GUI\Autom Database\Handler Studio\web Handle.txt",'r')
#file.write("web_handle_dict={'module':{'os':'c\\test','openpyxl':'c\\test\\done'},'input':{'var1':10,'var2':'testvar'}}")
file_list=list()
for each in file:
    #each=each.replace('\','\\\')
    exec(each)'''


from datetime import datetime

# date object of today's date
now=datetime.utcnow()
key=now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + now.strftime("%H") + now.strftime("%M") + now.strftime("%S")  + now.strftime("%f") + "-P"
print("Current year:", now.year)
print("Current day:", now.day)
print(key)