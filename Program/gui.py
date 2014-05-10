
#gui.py: Defines the graphical interface

import wx
import random

BORDER = 2
CURRENT_POS_STYLE = wx.TextAttr(wx.Colour(0, 0, 0), colBack=wx.Colour(0, 200, 255))


#utility function for making a panel with a predefined sizer, for layouting
def make_layout_panel(parent, direction=wx.HORIZONTAL, *args, **kwargs):
    panel = wx.Panel(parent, *args, **kwargs)
    panel.SetSizer(wx.BoxSizer(direction))
    return panel


class MainWindow(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Frame.__init__(self, parent, id, 'Turing Machine', size=(660,440), style=wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX) #style used to disable window resizing
        self.Centre()
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))

        
        controls_panel = make_layout_panel(self, wx.HORIZONTAL)
        self.Sizer.Add(controls_panel, 0, wx.EXPAND)

        program_label = wx.StaticText(controls_panel, label="Program: ") 
        controls_panel.Sizer.Add(program_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, BORDER)
        
        program_chooser = wx.Choice(controls_panel)
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


        self.program_chooser = program_chooser
        self.speed_input = speed_input
        self.run_pause_button = run_pause_button
        self.reset_button = reset_button
        self.tapes_panel = tapes_panel
        self.program_table = program_table
        self.tapes = list()


    def set_alphabet(self, alphabet):
        self.alphabet = alphabet


    def add_tape(self, value):
        tape_row = make_layout_panel(self.tapes_panel, wx.HORIZONTAL)
        self.tapes_panel.Sizer.Add(tape_row, 0, wx.EXPAND|wx.ALL, BORDER)

        label = wx.StaticText(tape_row, label="Tape #%d: " % (len(self.tapes)+1)) 
        tape_row.Sizer.Add(label, 1, wx.ALIGN_CENTER_VERTICAL)

        tape_entry = wx.TextCtrl(tape_row, value=value, style=wx.TE_RICH2, size=(100,-1)) 
        tape_row.Sizer.Add(tape_entry, 0, wx.EXPAND)

        gen_button = wx.Button(tape_row, label="Generate", size=(70,-1))
        tape_row.Sizer.Add(gen_button, 0, wx.EXPAND)

        def value_generator(event):
            random.seed()
            value = list()
            for i in range(random.randint(4, 10)):
                value.append(random.choice(self.alphabet))
            tape_entry.SetValue(''.join(value))
        tape_row.Bind(wx.EVT_BUTTON, value_generator, gen_button)

        self.tapes.append(tape_entry)

    def clear_tapes(self):
        self.tapes_panel.Sizer.Clear(True)
        self.tapes = list()

    def enable_tapes(self, bool_enable):
        self.tapes_panel.Enable(bool_enable)

    def get_tape_value(self, tape_nr):
        return self.tapes[tape_nr].GetValue()

    def update_tape(self, tape_nr, value, current_pos):
        tape_entry = self.tapes[tape_nr]
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
        
    def clear_actions(self):
        self.program_table.DeleteAllItems()

    def select_action(self, action_id):
        for id in range(0, self.program_table.GetItemCount()):
            self.program_table.Select(id, False)

        if action_id != -1:
            self.program_table.Select(action_id, True)
            self.program_table.EnsureVisible(action_id)


#test code to view the interface
if __name__ == '__main__':
    app = wx.App()
    window = MainWindow()
    window.set_alphabet("01")
    window.add_tape("1011")
    window.add_tape("1001011")
    window.Show()
    app.MainLoop()
