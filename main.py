import core
import interface
import wx
import wx.grid as gridlib

#Configuration
HALT_STATE = 'halt'
REAL_BLANK_SYMBOL = ' '
VISUAL_BLANK_SYMBOL = '_'
CURRENT_POS_STYLE = wx.TextAttr(wx.Colour(0, 0, 0), colBack=wx.Colour(0, 200, 255))


class Main(interface.Interface):
    def __init__(self, *args, **kargs):
        interface.Interface.__init__(self, *args, **kargs)

        #Binding buttons to functions to be executed
        #===================================
        self.Bind(wx.EVT_BUTTON, self.add_tape, self.add_tape_btn)
        self.Bind(wx.EVT_BUTTON, self.remove_tape, self.remove_tape_btn)
        
        self.Bind(wx.EVT_BUTTON, self.add_stack, self.add_stack_btn)
        self.Bind(wx.EVT_BUTTON, self.remove_stack, self.remove_stack_btn)
        
        self.Bind(wx.EVT_BUTTON, self.load_program, self.load_btn)
        self.Bind(wx.EVT_BUTTON, self.save_program, self.save_btn)

        self.Bind(wx.EVT_BUTTON, self.run, self.run_btn)
        self.Bind(wx.EVT_BUTTON, self.step, self.step_btn)
        self.Bind(wx.EVT_BUTTON, self.clear_values, self.clear_btn)
        #===================================
        
        self.tapes = []
        self.stacks = []

        self.machine = None
        self.add_tape(None)
        self.add_stack(None)
        self.last_action = -1 #-1 means the machine is not running

        
    def add_tape(self, event):
        tape = wx.TextCtrl(self.tapes_panel, style=wx.TE_RICH2)
        self.tapes.append(tape)
        self.tapes_sizer.Add(tape, 0, wx.EXPAND|wx.ALL, interface.ROWS_BORDER)
        self.tapes_sizer.Layout()

    def remove_tape(self, event):
        if len(self.tapes) > 1:
            last_tape = self.tapes.pop()
            self.tapes_sizer.Remove(last_tape)
            last_tape.Destroy()
            self.tapes_sizer.Layout()

    def add_stack(self, event):
        stack = wx.StaticText(self.stacks_panel, style=wx.SIMPLE_BORDER|wx.ST_NO_AUTORESIZE)
        self.stacks.append(stack)
        self.stacks_sizer.Add(stack, 0, wx.EXPAND|wx.ALL, interface.ROWS_BORDER)
        self.stacks_sizer.Layout()
        self.left_sizer.Layout()

    def remove_stack(self, event):
        if len(self.stacks) > 1:
            last_stack = self.stacks.pop()
            self.stacks_sizer.Remove(last_stack)
            last_stack.Destroy()
            self.stacks_sizer.Layout()
            self.left_sizer.Layout()

    
    def clear_tape_list(self):
        while len(self.tapes) > 1: #A turing machine should have at least one tape
            self.remove_tape(None) #We provide the event as None because we run the function manually
        while len(self.stacks) > 1:
            self.remove_stack(None)
        self.clear_values(None)
        self.program_table.ClearGrid()
    
    def load_program(self, event):
        openFileDialog = wx.FileDialog(self, "Open Turing Machine program", wildcard="Turing Machine program (*.tm)|*.tm", style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK: #ShowModal opens the dialog box . wx.ID_OK = OK button being pressed
            file_path = openFileDialog.GetPath()
            openFileDialog.Destroy()
            
            self.clear_tape_list()
            
            f = open(file_path, 'r')
            config_line = f.readline()
            config = config_line.split()
            for nr_tape in range(int(config[0])-1):
                self.add_tape(None)
            for nr_stack in range(int(config[1])-1):
                self.add_stack(None)
            self.initial_state_ctrl.SetValue(config[2])

            row = 0
            for line in f:
                action = line.split()
                for column, content in enumerate(action):
                    self.program_table.SetCellValue(row, column, content)
                row += 1
                
            f.close()
        
    def save_program(self, event):
        saveFileDialog = wx.FileDialog(self, "Save Turing Machine program", wildcard="Turing Machine program (*.tm)|*.tm", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_OK:
            file_path = saveFileDialog.GetPath()
            saveFileDialog.Destroy()

            f = open(file_path, 'w')
            f.write(str(len(self.tapes))+" "+str(len(self.stacks))+" "+self.initial_state_ctrl.GetValue()+"\n")

            row = 0
            list_finished = False
            while not list_finished:
                action = []
                for column in range(7):
                    value = self.program_table.GetCellValue(row, column)
                    if value.strip() == '':
                        list_finished = True
                    else:
                        action.append(value)
                if not list_finished:
                    f.write(" ".join(action) + "\n")
                    row += 1
                    
            f.close()

    #Used to disable editing while running by step
    def enable_editing(self, bool_enable):
        for tape in self.tapes:
            tape.SetEditable(bool_enable)
        self.program_table.EnableEditing(bool_enable)
        self.clear_btn.Enable(bool_enable)

    #Updates tape values and positions, and stack values with those from the machine
    def update_values(self):
        for tape_nr, tape_entry in enumerate(self.machine.tapes):
            tape_ctrl = self.tapes[tape_nr]
            tape_ctrl.SetValue("")
            tape_ctrl.SetValue(''.join(tape_entry['tape']))
            current_pos = tape_entry['position']
            tape_ctrl.SetStyle(current_pos, current_pos+1, CURRENT_POS_STYLE)
            
        for stack_nr, stack in enumerate(self.machine.stacks):
            self.stacks[stack_nr].SetLabel(''.join(stack))

    #Highlight the last action 
    def update_current_action(self):
        if self.last_action != -1:
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(wx.WHITE)
            self.program_table.SetRowAttr(self.last_action, attr)

        if self.machine.running:
            attr = gridlib.GridCellAttr()
            attr.SetBackgroundColour(wx.GREEN)
            self.program_table.SetRowAttr(self.machine.current_action_id, attr)
        
        self.program_table.Refresh()
        self.last_action = self.machine.current_action_id

    #Creates a turing machine and prepares it for running
    def prepare_machine(self):
        initial_state = self.initial_state_ctrl.GetValue()
        self.machine = core.TuringMachine(state_initial=initial_state, state_halt=HALT_STATE, alphabet=(REAL_BLANK_SYMBOL,'0','1'))

        for tape in self.tapes:
            self.machine.add_tape(list(tape.GetValue()))
        for stack in self.stacks:
            self.machine.add_stack(list(stack.GetLabel()))

        #Add the actions from the table to the machine
        row = 0
        list_finished = False
        while not list_finished:
            action = []
            for column in range(7):
                value = self.program_table.GetCellValue(row, column)
                if value.strip() == '':
                    list_finished = True
                else:
                    if column in range(1,3):
                        value = value.replace(VISUAL_BLANK_SYMBOL, REAL_BLANK_SYMBOL)
                    if column in range(1,6):
                        value=value.split(',')
                    action.append(value)
            if not list_finished:
                self.machine.add_action(*action)
                row += 1
            
        self.machine.init()
        self.update_values()
        
    def run(self, event):
        try:
            if self.machine == None or not self.machine.running:
                self.prepare_machine()
            self.machine.run()
        except core.TuringException as e:
            wx.MessageBox(str(e), 'Error', wx.OK|wx.ICON_ERROR)
        else:
            self.update_values()

        self.machine = None
        self.enable_editing(True)
    
    def step(self, event):
        try:
            if self.machine == None:
                self.prepare_machine()
                self.enable_editing(False)
            elif self.machine.state == HALT_STATE:
                self.update_values()
                self.update_current_action()
                wx.MessageBox('Program Complete', 'Info', wx.OK|wx.ICON_INFORMATION)
                self.machine = None
                self.enable_editing(True)
            else:
                self.update_values()
                self.machine.get_next_action()
                self.update_current_action()
                self.machine.run_next_action()
        except core.TuringException as e:
            wx.MessageBox(str(e), 'Error', wx.OK|wx.ICON_ERROR)
            self.machine = None
            self.enable_editing(True)

    def clear_values(self, event):
        for tape in self.tapes:
            tape.Clear()
        for stack in self.stacks:
            stack.SetLabel("")



if __name__=='__main__':
    app=wx.App()
    frame=Main(parent=None, id=wx.ID_ANY)
    frame.Show()
    app.MainLoop()
