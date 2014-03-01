import wx
import wx.grid as gridlib

class Interface(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Machine Turing',size=(740,400))
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(hbox)
        
        pnl1 = wx.Panel(self, -1, style=wx.NO_BORDER,size=(300,0))
        hbox.Add(pnl1,0, wx.EXPAND | wx.RIGHT, 4)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        pnl1.SetSizer(vbox)
        
        tape = wx.TextCtrl(pnl1)
        vbox.Add(tape,0,wx.EXPAND | wx.ALL, 10)

        pnl_btn = wx.Panel(pnl1, -1, style=wx.NO_BORDER)
        vbox.Add(pnl_btn,0,wx.EXPAND | wx.ALL, 10)

        btn_box = wx.BoxSizer(wx.HORIZONTAL)
        pnl_btn.SetSizer(btn_box)

        add_btn=wx.Button(pnl_btn,label="+")
        btn_box.Add(add_btn,0,wx.EXPAND | wx.RIGHT, 10)

        remove_btn=wx.Button(pnl_btn,label="-")
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

        
   
    def closewindow(self,event):
        self.Destroy()

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=Interface(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
