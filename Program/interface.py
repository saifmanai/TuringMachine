
#interface.py: Defines the user interface


#Small config
ROWS_BORDER = 4 #Border for the rows of tapes, stacks and panels
BUTTONS_SPACING = 6


import wx
import wx.grid as gridlib


class Interface(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent, id, 'Turing Machine', size=(984,600), style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX) #style used to disable window resizing
        self.Centre()

        #The frame's sizer, used to split it into the left and right sections
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(main_sizer)



        #==========Left Section=========
        #(contains the Main Controls and the lists of Tapes and Stacks)

        #Base Panel, children will be positioned Vertically
        self.left_panel = wx.Panel(self, style=wx.NO_BORDER)
        main_sizer.Add(self.left_panel, 0, wx.EXPAND|wx.RIGHT, 4)
        
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_panel.SetSizer(self.left_sizer)


        #Panel for the Main Controls, positions them Horizontally
        main_btn_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(main_btn_panel, 0, wx.EXPAND|wx.ALL, ROWS_BORDER)
         
        main_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_btn_panel.SetSizer(main_btn_sizer)


        #Main Controls
        #====================
        self.run_btn = wx.Button(main_btn_panel, label="Run")
        main_btn_sizer.Add(self.run_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        self.step_btn = wx.Button(main_btn_panel, label="Step")
        main_btn_sizer.Add(self.step_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        self.clear_values_btn = wx.Button(main_btn_panel, label="Clear Values")
        main_btn_sizer.Add(self.clear_values_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        #====================

        
        #Panel for the Stacks, positions them Vertically
        self.stacks_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(self.stacks_panel, 0, wx.EXPAND)
        
        self.stacks_sizer = wx.BoxSizer(wx.VERTICAL)
        self.stacks_panel.SetSizer(self.stacks_sizer)


        #Panel for the Tapes, positions them Vertically
        self.tapes_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(self.tapes_panel, 1, wx.EXPAND)

        self.tapes_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tapes_panel.SetSizer(self.tapes_sizer)


        #Panel for the Tapes and Stacks Controls, positions them Horizontally
        tape_btn_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(tape_btn_panel, 0, wx.EXPAND|wx.ALL, ROWS_BORDER)

        tape_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tape_btn_panel.SetSizer(tape_btn_sizer)


        #Tapes and Stacks Controls
        #====================
        self.add_tape_btn = wx.Button(tape_btn_panel, label="Add Tape")
        tape_btn_sizer.Add(self.add_tape_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        
        self.remove_tape_btn = wx.Button(tape_btn_panel, label="Remove Tape")
        tape_btn_sizer.Add(self.remove_tape_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        
        self.add_stack_btn = wx.Button(tape_btn_panel, label="Add Stack")
        tape_btn_sizer.Add(self.add_stack_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        
        self.remove_stack_btn = wx.Button(tape_btn_panel, label="Remove Stack")
        tape_btn_sizer.Add(self.remove_stack_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        #====================
        
        #==========End of Left Section=========

        
        
        #==========Right Section=========
        #(contains the Program Table and Program Editing Controls)

        #Base Panel, children will be positioned Vertically
        right_panel = wx.Panel(self, style=wx.NO_BORDER, size=(400,0))
        main_sizer.Add(right_panel, 1, wx.EXPAND)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_sizer)

        
        #Program Table
        self.program_table=gridlib.Grid(right_panel)
        self.program_table.CreateGrid(40,7)
        self.program_table.SetRowLabelSize(0) #Set to zero to hide the first column containing the name of each row
        self.program_table.SetColLabelValue(0, "State")
        self.program_table.SetColLabelValue(1, "Read Tapes")
        self.program_table.SetColLabelValue(2, "Read Stacks")
        self.program_table.SetColLabelValue(3, "Write Tapes")
        self.program_table.SetColLabelValue(4, "Write Stacks")
        self.program_table.SetColLabelValue(5, "Move")
        self.program_table.SetColLabelValue(6, "Next State")
        right_sizer.Add(self.program_table, 1, wx.EXPAND|wx.BOTTOM, 4)


        #Panel for the Program Controls, positions them Horizontally
        program_btn_panel = wx.Panel(right_panel, style=wx.NO_BORDER)
        right_sizer.Add(program_btn_panel, 0, wx.EXPAND|wx.ALL, ROWS_BORDER)

        program_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        program_btn_panel.SetSizer(program_btn_sizer)


        #Program Editing Controls
        #====================
        self.load_btn = wx.Button(program_btn_panel, label="Load Program")
        program_btn_sizer.Add(self.load_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        self.save_btn = wx.Button(program_btn_panel, label="Save Program")
        program_btn_sizer.Add(self.save_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
		
        self.clear_program_btn = wx.Button(program_btn_panel, label="Clear Program")
        program_btn_sizer.Add(self.clear_program_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        initial_state_label = wx.StaticText(program_btn_panel, label="Initial State: ",style=wx.ST_NO_AUTORESIZE|wx.ALIGN_RIGHT) 
        program_btn_sizer.Add(initial_state_label, 1, wx.ALIGN_CENTER_VERTICAL)

        self.initial_state_ctrl = wx.TextCtrl(program_btn_panel)
        program_btn_sizer.Add(self.initial_state_ctrl, 0, wx.EXPAND)
        #====================

        #==========End of Right Section=========



#test code to view the interface
if __name__=='__main__':
    app=wx.App()
    frame=Interface(parent=None, id=wx.ID_ANY)
    frame.Show()
    app.MainLoop()
