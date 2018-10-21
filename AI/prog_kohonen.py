import os
import wx
import wx.stc
import wx.richtext
import math
from kohonen_net import KohonenNet
import time
from random import random
from copy import deepcopy
from copy import copy

ID_ABOUT = 101
ID_EXIT = 110
ID_START = 1001


class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        self.isRunning = False
        self.koh = None
        self.dataPath = None
        self.dc = None
        self.savedWeight = None;

        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = (935,700))
        # Setting up the menu.
        filemenu= wx.Menu()
        m_open = filemenu.Append(wx.ID_OPEN, "&Open"," Open file with data")
        filemenu.AppendSeparator()
        m_exit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Bind(wx.EVT_MENU,  self.OnExit, m_exit)
        self.Bind(wx.EVT_MENU,  self.OnOpen, m_open)

        #Panel with input data
        panel = wx.Panel(self, pos=(0,0), size=(300, 690))
        box = wx.BoxSizer(wx.VERTICAL)

        m_text = wx.StaticText(panel, 0, "Classes:", pos=(10,10))
        #m_text.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        #m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 6)
        m_text = wx.StaticText(panel, 1, "Cycles:", pos=(10,20))
        box.Add(m_text, 0, wx.ALL, 6)
        m_text = wx.StaticText(panel, 2, "Alpha:", pos=(10,30))
        box.Add(m_text, 0, wx.ALL, 6)
        m_text = wx.StaticText(panel, 3, "Neighbourhood:", pos=(10,40))
        box.Add(m_text, 0, wx.ALL, 6)
        m_text = wx.StaticText(panel, 4, "Data:", pos=(5,145))
        m_text = wx.StaticText(panel, 5, "Results:", pos=(5,275))


        self.m_start = wx.Button(panel, ID_START, "Start", pos=(5,110))
        self.m_start.Bind(wx.EVT_BUTTON, self.OnStartClick)
        #box.Add(self.m_start, 0, wx.ALL, 10)

        self.m_step = wx.Button(panel, ID_START+1, "Step", pos=(83,110))
        self.m_step.Bind(wx.EVT_BUTTON, self.OnStepClick)

        self.m_step = wx.Button(panel, ID_START+4, "Change Colors", pos=(194,110))
        self.m_step.Bind(wx.EVT_BUTTON, self.OnChangeColorsClick)
        #box.Add(self.m_step, 0, wx.ALL, 10)

        self.classesCtrl = wx.TextCtrl(panel, 0, pos = (100,5), size = (60, 20))
        self.classesCtrl.SetValue("10")
        self.cyclesCtrl = wx.TextCtrl(panel, 1, pos = (100,30), size = (60, 20))
        self.cyclesCtrl.SetValue("100")
        self.alphaCtrl = wx.TextCtrl(panel, 2, pos = (100,55), size = (60, 20))
        self.alphaCtrl.SetValue("0.5")
        self.neighbourhoodCtrl = wx.TextCtrl(panel, 3, pos = (100,80), size = (60, 20))
        self.neighbourhoodCtrl.SetValue("2.0")
        self.pointCtrl = wx.TextCtrl(panel, 4, pos = (5,160), size = (280, 110), style=wx.TE_MULTILINE)
        self.pointCtrl.SetEditable(False)
        self.resultCtrl = wx.TextCtrl(panel, 5, pos = (5,290), size = (280, 266), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.wx.TE_RICH)
        self.resultCtrl.SetEditable(False)

        #new point
        m_text = wx.StaticText(panel, 7, "Add new point:", pos=(5,570))
        self.ptXCtrl = wx.TextCtrl(panel, 6, pos = (5, 586), size = (60, 23))
        self.ptXCtrl.SetValue("0.0")
        self.ptYCtrl = wx.TextCtrl(panel, 7, pos = (65, 586), size = (60, 23))
        self.ptYCtrl.SetValue("0.0")
        self.m_add = wx.Button(panel, ID_START+2, "Add", pos=(130,586))
        self.m_add.Bind(wx.EVT_BUTTON, self.OnAddClick)

        panel.SetSizer(box)
        panel.Layout()


        #Panel with graph
        graphPanel = wx.Panel(self, pos=(300,0), size=(630, 622))
        #graphPanel.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.graphPanel = graphPanel
        graphPanel.Bind(wx.EVT_PAINT, self.OnPaint)
        graphPanel.Layout()
        #self.graphPanel.Refresh()

        self.statusbar = self.CreateStatusBar()
        self.Show(True)

    def WriteResults(self):
        self.resultCtrl.Clear()
        outStr = ""
        for i in range(self.koh.MaxClass):
            cnt = 0
            for j in range(self.koh.NPatterns):
                if self.koh.Membership[j] == i:
                    cnt += 1
            addStr = "Class "+str(i)+": "+str(cnt)+"\n"
            outStr += addStr
            textattr = wx.TextAttr(self.colors[i])
            self.resultCtrl.AppendText(addStr)
            self.resultCtrl.SetStyle(len(outStr)-len(addStr), len(outStr), textattr)


    def OnAbout(self,e):
        d= wx.MessageDialog( self, " Bleble \n"
                            " Ble", wx.OK)# Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.dataPath = os.path.join(self.dirname,self.filename)
            f=open(os.path.join(self.dirname,self.filename),'r')
            self.pointCtrl.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnChangeColorsClick(self, event):
        if self.koh!=None:
            self.colors = [[int(255*random()), int(255*random()), int(255*random())] for i in range(self.koh.MaxClass)]
            self.graphPanel.Refresh()
        self.WriteResults()


    def OnAddClick(self,e):
        if self.koh != None:
            #print [float(self.ptXCtrl.GetValue()), float(self.ptYCtrl.GetValue())]
            self.koh.AddPattern([float(self.ptXCtrl.GetValue()), float(self.ptYCtrl.GetValue())])
            self.graphPanel.Refresh()
        self.WriteResults()

    def OnStartClick(self,e):
        #print int(self.cyclesCtrl.GetValue()),  int(self.classesCtrl.GetValue()), float(self.neighbourhoodCtrl.GetValue()), float(self.alphaCtrl.GetValue())
        if self.dataPath == None:
            return None
        self.m_start.SetLabel("Processing...")
        self.koh = KohonenNet( int(self.cyclesCtrl.GetValue()),  int(self.classesCtrl.GetValue()), float(self.neighbourhoodCtrl.GetValue()), float(self.alphaCtrl.GetValue()))
        if self.savedWeight == None or len(self.savedWeight) != len(self.koh.W):
            self.savedWeight = deepcopy(self.koh.W)
            self.colors = [[int(255*random()), int(255*random()), int(255*random())] for i in range(self.koh.MaxClass)]
        else:
            self.koh.W = deepcopy(self.savedWeight)

        self.koh.ReadPatterns(self.dataPath);

        while self.koh.Step():
            self.graphPanel.Refresh()
            #time.sleep(1)

        self.m_start.SetLabel("Start")

        self.koh.updateMembership()
        self.WriteResults()
        self.isRunning = False;

    def OnStepClick(self,e):
        if self.dataPath == None:
            return None
        if self.isRunning == False:
            self.isRunning = True;
            self.koh = KohonenNet( int(self.cyclesCtrl.GetValue()),  int(self.classesCtrl.GetValue()), float(self.neighbourhoodCtrl.GetValue()), float(self.alphaCtrl.GetValue()))
            if self.savedWeight == None or len(self.savedWeight) != len(self.koh.W):
                self.savedWeight = deepcopy(self.koh.W)
                self.colors = [[int(255*random()), int(255*random()), int(255*random())] for i in range(self.koh.MaxClass)]
            else:
                self.koh.W = deepcopy(self.savedWeight)
            self.koh.ReadPatterns(self.dataPath);
        self.koh.Step()
        self.graphPanel.Refresh()
        self.koh.updateMembership()
        self.WriteResults()

        self.resultCtrl.AppendText("\nStep Number: "+str(self.koh.CycleNo))


    def OnPaint(self, event=None):
        dc = wx.PaintDC(self.graphPanel)

        #self.classesCtrl.SetValue(str(int(self.classesCtrl.GetValue())+1))
        #self.dc.SetBackground(wx.Brush('black'))
        #dc.SetPen(wx.Pen('blue', 4))
        dc.SetPen(wx.Pen('gray', 1))
        rect = wx.Rect(5, 5, 600, 600)
        dc.DrawRectangleRect(rect)
        dc.SetPen(wx.Pen((240, 240, 240), 1, wx.DOT))#wx.SHORT_DASH))
        dc.DrawLine(155, 6, 155, 603)
        dc.DrawLine(455, 6, 455, 603)
        dc.DrawLine(6, 155, 603, 155)
        dc.DrawLine(6, 455, 603, 455)
        dc.SetPen(wx.Pen((220, 220, 220), 1, wx.DOT))
        dc.DrawLine(305, 6, 305, 603)
        dc.DrawLine(6, 305, 603, 305)


        #dc.DrawRoundedRectangleRect(rect, 8)
        if(self.koh != None):
            self.koh.updateMembership()
            dc.SetPen(wx.Pen('black', 1))
            for i in range(self.koh.NPatterns):
                dc.SetBrush(wx.Brush((self.colors[self.koh.Membership[i]][0],self.colors[self.koh.Membership[i]][1],self.colors[self.koh.Membership[i]][2])))
                dc.DrawCircle(5+(600*self.koh.X[i][0]), 5+(600*self.koh.X[i][1]), 4)



app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Kohonen networks")
app.MainLoop()

