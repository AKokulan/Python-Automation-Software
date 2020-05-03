
class os_globalvariable:

    def __init__(self,object_studio_module_tab,object_studio_input_tab,object_studio_output_tab,object_studio_code_tab):
        self.object_studio_module_tab=object_studio_module_tab
        self.object_studio_input_tab=object_studio_input_tab
        self.object_studio_output_tab=object_studio_output_tab
        self.object_studio_code_tab=object_studio_code_tab

    def os_module_gv(self):
        fr_table = self.object_studio_module_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0]
        frame_config = (self.object_studio_module_tab.winfo_children()[4])

    def os_input_gv(self):
        fr_table = ((self.object_studio_input_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0]

        lb_config_handle_value=(self.object_studio_input_tab.winfo_children()[4]).winfo_children()[1]
        lb_config_action_value=(self.object_studio_input_tab.winfo_children()[4]).winfo_children()[3]

    def os_output_gv(self):
        fr_table = ((self.object_studio_output_tab.winfo_children()[0]).winfo_children()[0]).winfo_children()[0]

        lb_config_handle_value=((self.object_studio_output_tab.winfo_children()[4]).winfo_children()[1])
        lb_config_action_value=((self.object_studio_output_tab.winfo_children()[4]).winfo_children()[3])

    def os_code_gv(self):
        txt_code = (self.object_studio_code_tab.winfo_children()[0]).winfo_children()[1]