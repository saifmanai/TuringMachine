
import wx
import random
import tm
import programs

BORDER = 2
CURRENT_POS_STYLE = wx.TextAttr(wx.Colour(0, 0, 0), colBack=wx.Colour(0, 200, 255))


#utility function for making a panel with a predefined sizer, for layouting
def make_layout_panel(parent, direction=wx.HORIZONTAL, *args, **kwargs):
    panel = wx.Panel(parent, *args, **kwargs)
    panel.SetSizer(wx.BoxSizer(direction))
    return panel


class Main(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Frame.__init__(self, parent, id, 'Turing Machine', size=(660,440), style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX) #style used to disable window resizing
        self.Centre()
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))


        controls_panel = make_layout_panel(self, wx.HORIZONTAL)
        self.Sizer.Add(controls_panel, 0, wx.EXPAND)


        program_label = wx.StaticText(controls_panel, label="Program: ") 
        controls_panel.Sizer.Add(program_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, BORDER)
        
        program_chooser = wx.Choice(controls_panel)
        for program in programs.plist:
            program_chooser.Append(program.name)
        controls_panel.Sizer.Add(program_chooser, 0, wx.EXPAND|wx.ALL, BORDER)

        
        speed_label = wx.StaticText(controls_panel, label="Simulation speed (OPs/sec): ") 
        controls_panel.Sizer.Add(speed_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, BORDER)
        
        speed_input = wx.SpinCtrl(controls_panel, min=1, initial=8, value='8', size=(60,-1))
        controls_panel.Sizer.Add(speed_input, 0, wx.EXPAND|wx.ALL, BORDER)


        run_pause_button = wx.Button(controls_panel, label="Run")
        controls_panel.Sizer.Add(run_pause_button, 0, wx.EXPAND|wx.ALL, BORDER)
        
        reset_button = wx.Button(controls_panel, label="Reset")
        reset_button.Enable(False)
        controls_panel.Sizer.Add(reset_button, 0, wx.EXPAND|wx.ALL, BORDER)


        main_panel = make_layout_panel(self, wx.HORIZONTAL)
        self.Sizer.Add(main_panel, 1, wx.EXPAND)

        tapes_panel = make_layout_panel(main_panel, wx.VERTICAL, size=(230,-1), style=wx.BORDER_SIMPLE)
        main_panel.Sizer.Add(tapes_panel, 0, wx.EXPAND)

        program_table = wx.ListCtrl(main_panel, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        program_table.InsertColumn(0, "State")
        program_table.InsertColumn(1, "Read")
        program_table.InsertColumn(2, "To Write")
        program_table.InsertColumn(3, "Move")
        program_table.InsertColumn(4, "Next State")
        main_panel.Sizer.Add(program_table, 1, wx.EXPAND)


        self.Bind(wx.EVT_CHOICE, self.change_program, program_chooser)
        self.Bind(wx.EVT_BUTTON, self.run_pause, run_pause_button)
        self.Bind(wx.EVT_BUTTON, self.reset, reset_button)
        
        self.program_chooser = program_chooser
        self.speed_input = speed_input
        self.run_pause_button = run_pause_button
        self.reset_button = reset_button
        self.tapes_panel = tapes_panel
        self.program_table = program_table
        
        self.tape_panels = list()


    def add_tape(self, value):
        tape_row = make_layout_panel(self.tapes_panel, wx.HORIZONTAL)
        self.tapes_panel.Sizer.Add(tape_row, 0, wx.EXPAND|wx.ALL, BORDER)

        label = wx.StaticText(tape_row, label="Tape #%d: " % (len(self.tape_panels)+1)) 
        tape_row.Sizer.Add(label, 1, wx.ALIGN_CENTER_VERTICAL)

        tape_entry = wx.TextCtrl(tape_row, value=value, style=wx.TE_RICH2, size=(100,-1)) 
        tape_row.Sizer.Add(tape_entry, 0, wx.EXPAND)

        gen_button = wx.Button(tape_row, label="Generate", size=(70,-1))
        tape_row.Sizer.Add(gen_button, 0, wx.EXPAND)

        def value_generator(event):
            random.seed()
            value = list()
            for i in range(random.randint(4, 10)):
                value.append(random.choice(self.program.input_values))
            tape_entry.SetValue(''.join(value))
        tape_row.Bind(wx.EVT_BUTTON, value_generator, gen_button)

        self.tape_panels.append(tape_entry)

    def reload_tapes(self):
        self.tapes_panel.Sizer.Clear(True)
        self.tape_panels = list()
        
        for tape in self.program.tapes:
            self.add_tape(''.join(tape))
        self.tapes_panel.Layout()

    def update_tape(self, tape_nr, value, current_pos):
        tape_entry = self.tape_panels[tape_nr]
        tape_entry.SetValue("")
        tape_entry.SetValue(value)
        
        if current_pos != -1:
            tape_entry.SetStyle(current_pos, current_pos+1, CURRENT_POS_STYLE)


    def add_action(self, action):
        row = self.program_table.InsertStringItem(action['id'], action['state'])
        self.program_table.SetStringItem(row, 1, ','.join(action['read_values']))
        self.program_table.SetStringItem(row, 2, ','.join(action['write_values']))
        self.program_table.SetStringItem(row, 3, ','.join(action['directions']))
        self.program_table.SetStringItem(row, 4, action['next_state'])

    def reload_program(self):
        self.program_table.DeleteAllItems()
        for action in self.program.actions:
            self.add_action(action)
    
    def select_action(self, action_id):
        for id in range(0, self.program_table.GetItemCount()):
            self.program_table.Select(id, False)

        if action_id != -1:
            self.program_table.Select(action_id, True)
            self.program_table.EnsureVisible(action_id)


    def change_program(self, event):
        program_id = event.GetSelection()
        self.program = programs.plist[program_id]
        
        self.reload_tapes()
        self.reload_program()
    
    
    def run_pause(self, event):
        if hasattr(self, 'tm') and self.tm.running:
            if self.tm.should_continue.is_set():
                self.tm.should_continue.clear()
                
                self.speed_input.Enable(True)
                self.run_pause_button.SetLabel("Resume")
            else:
                self.tm.speed = self.speed_input.GetValue()
                self.tm.should_continue.set()
                
                self.speed_input.Enable(False)
                self.run_pause_button.SetLabel("Pause")
        elif self.program_chooser.GetSelection() != wx.NOT_FOUND:
                self.program_chooser.Enable(False)
                self.speed_input.Enable(False)
                self.run_pause_button.SetLabel("Pause")
                self.reset_button.Enable(True)
                self.tapes_panel.Enable(False)

                for tape_nr, tape in enumerate(self.program.tapes):
                    self.program.tapes[tape_nr] = list(self.tape_panels[tape_nr].GetValue())

                self.tm = tm.TuringMachine(self.program, self.speed_input.GetValue(), self.tm_listener)
                self.tm.start()
                    
    def reset(self, event=None):
        if hasattr(self, 'tm'):
            self.tm.running = False

        self.program_chooser.Enable(True)
        self.speed_input.Enable(True)
        self.run_pause_button.SetLabel("Run")
        self.reset_button.Enable(False)
        self.tapes_panel.Enable(True)
        self.select_action(-1)
        
        for tape_nr, tape in enumerate(self.tm.program.tapes):
            self.update_tape(tape_nr, ''.join(tape), -1)


    def tm_listener(self, tm, state):
        wx.CallAfter(self.window_updater, tm, state)
    
    def window_updater(self, tm, state):
        if hasattr(tm, 'error'):
            wx.MessageBox(str(tm.error), 'Error', wx.OK|wx.ICON_ERROR)
            self.reset()
        else:
            if tm.running:
                for tape_nr, tape in enumerate(tm.program.tapes):
                    self.update_tape(tape_nr, ''.join(tape), tm.tapes_pos[tape_nr])
                
                if tm.current_action != None:
                    self.select_action(tm.current_action['id'])
            else:
                self.reset()



if __name__ == '__main__':
    app = wx.App()
    window = Main()
    window.Show()
    app.MainLoop()
