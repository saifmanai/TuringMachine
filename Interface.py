import wx
import wx.grid as gridlib

class Interface(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Machine Turing',size=(740,400), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)
        
        self.pnl1 = wx.Panel(self, -1, style=wx.NO_BORDER,size=(300,0))
        hbox.Add(self.pnl1,0, wx.EXPAND | wx.RIGHT, 4)
        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.pnl1.SetSizer(self.vbox)

        pnl_btn = wx.Panel(self.pnl1, -1, style=wx.NO_BORDER)
        self.vbox.Add(pnl_btn,0,wx.EXPAND | wx.ALL, 10)
        
        tape = wx.TextCtrl(self.pnl1)
        self.vbox.Add(tape,0,wx.EXPAND | wx.ALL, 10)
        
        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        pnl_btn.SetSizer(btn_box)

        add_btn=wx.Button(pnl_btn,label="+")
        self.Bind(wx.EVT_BUTTON, self.add_tape, add_btn)
        btn_box.Add(add_btn,0,wx.EXPAND | wx.RIGHT, 10)
        
        remove_btn=wx.Button(pnl_btn,label="-")
        self.Bind(wx.EVT_BUTTON, self.remove_tape, remove_btn)
        btn_box.Add(remove_btn,0,wx.EXPAND | wx.RIGHT, 10)

        start_btn=wx.Button(pnl_btn,label="Start")
        btn_box.Add(start_btn,0,wx.EXPAND | wx.RIGHT, 10)
        
        myGrid=gridlib.Grid(self)
        myGrid.CreateGrid(30,5)
        myGrid.SetRowLabelSize(0)
        hbox.Add(myGrid,1, wx.EXPAND, 1)
        myGrid.SetColLabelValue(0,"State")
        myGrid.SetColLabelValue(1,"Read Values")
        myGrid.SetColLabelValue(2,"Write Values")
        myGrid.SetColLabelValue(3,"Direction")
        myGrid.SetColLabelValue(4,"Next State")
        
        self.Centre()

        self.added_tapes = []
        
    def closewindow(self,event):
        self.Destroy()

    def add_tape(self, event):
        tape = wx.TextCtrl(self.pnl1)
        self.added_tapes.append(tape)
        self.vbox.Add(tape,0,wx.EXPAND | wx.ALL, 10)
        self.vbox.Layout()

    def remove_tape(self, event):
        if len(self.added_tapes) > 0:
            last_tape = self.added_tapes.pop()
            self.vbox.Remove(last_tape)
            last_tape.Destroy()
            self.vbox.Layout()

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=Interface(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
