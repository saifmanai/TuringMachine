
import tm
import programs
import gui
import wx


class Main:
    def __init__(self):
        self.window = gui.MainWindow()

        for program in programs.plist:
            self.window.program_chooser.Append(program.name)

        self.window.Bind(wx.EVT_CHOICE, self.load_program, self.window.program_chooser)
        self.window.Bind(wx.EVT_BUTTON, self.run_pause, self.window.run_pause_button)
        self.window.Bind(wx.EVT_BUTTON, self.reset, self.window.reset_button)

        self.window.Show()
        
    def load_program(self, event):
        program_id = event.GetSelection()
        self.program = programs.plist[program_id]

        self.window.set_alphabet(self.program.alphabet)
        
        self.window.clear_tapes()
        for tape in self.program.tapes:
            self.window.add_tape(''.join(tape))
        self.window.tapes_panel.Layout()

        self.window.clear_actions()
        for action in self.program.actions:
            self.window.add_action(action)
        
    def run_pause(self, event):
        if hasattr(self, 'tm') and self.tm.running:
            if self.tm.should_continue.is_set():
                self.tm.should_continue.clear()
                
                self.window.speed_input.Enable(True)
                self.window.run_pause_button.SetLabel("Resume")
            else:
                self.tm.speed = self.window.speed_input.GetValue()
                self.tm.should_continue.set()
                
                self.window.speed_input.Enable(False)
                self.window.run_pause_button.SetLabel("Pause")
        elif self.window.program_chooser.GetSelection() != wx.NOT_FOUND:
                self.window.program_chooser.Enable(False)
                self.window.speed_input.Enable(False)
                self.window.run_pause_button.SetLabel("Pause")
                self.window.reset_button.Enable(True)
                self.window.enable_tapes(False)

                for tape_nr, tape in enumerate(self.program.tapes):
                    self.program.tapes[tape_nr] = list(self.window.get_tape_value(tape_nr))

                self.tm = tm.TuringMachine(self.program, self.window.speed_input.GetValue(), self.tm_listener)
                self.tm.start()
                    

    def reset(self, event=None):
        if hasattr(self, 'tm'):
            self.tm.running = False

        self.window.program_chooser.Enable(True)
        self.window.speed_input.Enable(True)
        self.window.run_pause_button.SetLabel("Run")
        self.window.reset_button.Enable(False)
        self.window.enable_tapes(True)
        self.window.select_action(-1)

    def tm_listener(self, tm):
        wx.CallAfter(self.window_updater, tm)
    
    def window_updater(self, tm):
        if hasattr(tm, 'error'):
            wx.MessageBox(str(tm.error), 'Error', wx.OK|wx.ICON_ERROR)
        else:
            for tape_nr, tape in enumerate(tm.program.tapes):
                if not tm.running:
                    pos = -1
                else:
                    pos = tm.tapes_pos[tape_nr]
                self.window.update_tape(tape_nr, ''.join(tape), pos)
            
            if hasattr(tm, 'action') and tm.action != None:
                self.window.select_action(tm.action['id'])

        if tm.running == False:
            self.reset()
                

if __name__=='__main__':
    app = wx.App()
    main = Main()
    app.MainLoop()
