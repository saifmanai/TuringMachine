import wx
import wx.grid as gridlib

ROWS_BORDER = 4 #Border for buttons panel
BUTTONS_SPACING = 6 #Space between buttons. Check the "Adding buttons..." section

class Interface(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent, id, 'Turing Machine', size=(987,600), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX) #style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX  added to disable the window maximize function
        self.Centre()

        #Create global sizer for frame
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(main_sizer)

        #Create panel on the frame . Will act as the left panel later
        self.left_panel = wx.Panel(self, style=wx.NO_BORDER)
        main_sizer.Add(self.left_panel, 0, wx.EXPAND|wx.RIGHT, 4) #Add left panel to the global sizer

        #Create sizer for the left panel 
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_panel.SetSizer(self.left_sizer) #Set the sizer of the left panel to the left sizer

        #Create panel for buttons 
        main_btn_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(main_btn_panel, 0, wx.EXPAND|wx.ALL, ROWS_BORDER) #Add buttons panel to the left sizer to arrange it vertically

        #Create sizer for buttons 
        main_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_btn_panel.SetSizer(main_btn_sizer) #Set the sizer of the buttons panel to the newly created sizer in order to arrange the buttons horizontally

        #Adding buttons to the top buttons panel
        #===================================
        self.run_btn = wx.Button(main_btn_panel, label="Run")
        main_btn_sizer.Add(self.run_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        self.step_btn = wx.Button(main_btn_panel, label="Step")
        main_btn_sizer.Add(self.step_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        self.clear_btn = wx.Button(main_btn_panel, label="Clear")
        main_btn_sizer.Add(self.clear_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        #===================================

        #Create panel for stacks
        self.stacks_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(self.stacks_panel, 0, wx.EXPAND) #Add the stacks panel to the vertically arranged left sizer

        #Create sizer for stacks , arranged vertically
        self.stacks_sizer = wx.BoxSizer(wx.VERTICAL)
        self.stacks_panel.SetSizer(self.stacks_sizer) #Set the stacks panel sizer to the stacks sizer

        #Create panel for tapes
        self.tapes_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(self.tapes_panel, 1, wx.EXPAND) #Add it to the left sizer to arrange the panel vertically

        #Create sizer for tapes
        self.tapes_sizer = wx.BoxSizer(wx.VERTICAL)
        self.tapes_panel.SetSizer(self.tapes_sizer) #Arrange them vertically

        #Create tape buttons panel
        tape_btn_panel = wx.Panel(self.left_panel, style=wx.NO_BORDER)
        self.left_sizer.Add(tape_btn_panel, 0, wx.EXPAND|wx.ALL, ROWS_BORDER) #Arrange the tape buttons panel vertically by adding it to the left sizer

        #Create sizer for tape buttons
        tape_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tape_btn_panel.SetSizer(tape_btn_sizer) #Arrange buttons horizontally

        #Adding buttons to the bottom buttons panel
        #===================================
        self.add_tape_btn = wx.Button(tape_btn_panel, label="Add Tape")
        tape_btn_sizer.Add(self.add_tape_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        
        self.remove_tape_btn = wx.Button(tape_btn_panel, label="Remove Tape")
        tape_btn_sizer.Add(self.remove_tape_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        
        self.add_stack_btn = wx.Button(tape_btn_panel, label="Add Stack")
        tape_btn_sizer.Add(self.add_stack_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        
        self.remove_stack_btn = wx.Button(tape_btn_panel, label="Remove Stack")
        tape_btn_sizer.Add(self.remove_stack_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)
        #===================================

        #Create panel for the right side . Will contain the GRID and bottom buttons panel
        right_panel = wx.Panel(self, style=wx.NO_BORDER, size=(400,0))
        main_sizer.Add(right_panel, 1, wx.EXPAND|wx.RIGHT, 4) # Add the panel to the global sizer

        #Create vertical sizer for the right side panel
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_panel.SetSizer(right_sizer)
        
        #Create GRID
        #===================================
        self.program_table=gridlib.Grid(right_panel)
        self.program_table.CreateGrid(40,7)
        self.program_table.SetRowLabelSize(0) #Set to zero to remove the first column containing the name of each row
        self.program_table.SetColLabelValue(0, "State")
        self.program_table.SetColLabelValue(1, "Read Tapes")
        self.program_table.SetColLabelValue(2, "Read Stacks")
        self.program_table.SetColLabelValue(3, "Write Tapes")
        self.program_table.SetColLabelValue(4, "Write Stacks")
        self.program_table.SetColLabelValue(5, "Move")
        self.program_table.SetColLabelValue(6, "Next State")
        #===================================

        right_sizer.Add(self.program_table, 1, wx.EXPAND|wx.BOTTOM, 4) #Add the grid to the right side sizer

        #Create bottom buttons panel for the right side 
        program_btn_panel = wx.Panel(right_panel, style=wx.NO_BORDER)
        right_sizer.Add(program_btn_panel, 0, wx.EXPAND|wx.ALL, ROWS_BORDER) #Add it to the right sizer to display it vertically after the grid

        #Create bottom buttons sizer
        program_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        program_btn_panel.SetSizer(program_btn_sizer) #Arrange them horizontally

        #Adding buttons + label + input
        #===================================
        self.load_btn = wx.Button(program_btn_panel, label="Load Program")
        program_btn_sizer.Add(self.load_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        self.save_btn = wx.Button(program_btn_panel, label="Save Program")
        program_btn_sizer.Add(self.save_btn, 0, wx.EXPAND|wx.RIGHT, BUTTONS_SPACING)

        initial_state_label = wx.StaticText(program_btn_panel, label="Initial State: ") 
        program_btn_sizer.Add(initial_state_label, 0, wx.ALIGN_CENTER_VERTICAL)

        self.initial_state_ctrl = wx.TextCtrl(program_btn_panel) #Input for initial state
        program_btn_sizer.Add(self.initial_state_ctrl, 0, wx.EXPAND)
        #===================================

if __name__=='__main__':
    app=wx.App() #Switched the deprecated PySimpleApp() with a newer one
    frame=Interface(parent=None, id=wx.ID_ANY) #wx.ID_ANY = -1
    frame.Show()
    app.MainLoop()
