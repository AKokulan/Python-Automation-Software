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

# Reset var and delete all old options
menu=os_module_action_option_menu['menu']
os_modules_action_optionmenu_var.set('')
menu.delete(0, 'end')


def module_refersh_button_call(a):
    print("actions: ",action)
    os_modules_action_optionmenu_var.set(action)

    self.os_module_action_optionmenu_call(object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab)

    os_modules_action_optionmenu_var.trace("w", module_refersh_button_call)


for actions in action_list:
    menu.add_command(label=actions,command=lambda action=actions :module_refersh_button_call())
