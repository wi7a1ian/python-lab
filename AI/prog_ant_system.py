#python version 2.5.2
#wxPython library 2.8.9.1

import os
import wx
import wx.stc
import wx.richtext
import wx.grid
import math
from ant_system import AntSystem
from ant_system import dec
from ant_system import PosInf
import ant_system
import time
from random import random
from copy import deepcopy
from copy import copy



class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,wx.ID_ANY, title, size = (1000,700), style = wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER)

        # Setting up the menu.
        filemenu = wx.Menu()
        m_open = filemenu.Append(wx.ID_OPEN, "&Open"," Open file with data.")
        m_save = filemenu.Append(wx.ID_SAVE, "&Save"," Save file with data.")
        filemenu.AppendSeparator()
        m_exit = filemenu.Append(wx.ID_EXIT, "E&xit"," Terminate the program.")
        tablemenu = wx.Menu()
        m_table = tablemenu.Append(1000, "Costs &Matrix"," Grid representing travel costs.")
        m_graph = tablemenu.Append(1001, "&Calculations"," Calculation done using ans system algorithm.")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(tablemenu,"  &Options ")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Bind(wx.EVT_MENU, self.OnExit, m_exit)
        self.Bind(wx.EVT_MENU, self.OnOpen, m_open)
        self.Bind(wx.EVT_MENU, self.OnSave, m_save)
        self.Bind(wx.EVT_MENU, self.OnTable, m_table)
        self.Bind(wx.EVT_MENU, self.OnGraph, m_graph)

        #Predefined Attributes
        self.costMap = ""
        self.antSystem = AntSystem(1000, False, False, 5, 2, 1, 0.5)


        #mapVector = wx.DataViewCtrl()
        self.tablePanel = wx.Panel(self, pos=(0,0), size=(1000, 1000))
        self.graphPanel = wx.Panel(self, pos=(0,0), size=(1000, 1000))
        self.graphPanel.Show(False)

        #Panel with grid
        m_text = wx.StaticText(self.tablePanel, 1, "Number of cities:", pos=(5,5))
        self.cityNrCtrl = wx.TextCtrl(self.tablePanel, 2, pos = (90, 1), size = (30, 23))
        self.cityNrCtrl.SetValue("30")
        self.cityNrBtn = wx.Button(self.tablePanel, 3, "Apply", pos = (125, 1), size = (50, 23))
        self.cityNrBtn.Bind(wx.EVT_BUTTON, self.cityNrChange)
        #self.grid = wx.Grid(parent, wx.ID_ANY)
        self.grid = wx.grid.Grid(self.tablePanel, 1010,  pos = (0, 35), size = (995, 596))
        self.grid.CreateGrid(30, 30)
        self.grid.SetDefaultColSize(30, True)
        self.grid.SetDefaultRowSize(30, True)
        self.grid.DisableDragGridSize()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.grid.SetRowLabelSize(30)

        for i in range(30):
            self.grid.SetColLabelValue(i, str(i+1))
            self.grid.SetRowLabelValue(i, str(i+1))
            self.grid.SetCellBackgroundColour(i,i, wx.Colour(245, 245, 245))


        #Graph Plot(Panel)-----------------------------------------------------
        self.graphPlot = wx.Panel(self.graphPanel, pos=(0,100), size=(1000, 530))
        self.graphPlot.Bind(wx.EVT_PAINT, self.OnPaintGraph)

        m_text = wx.StaticText(self.graphPanel, 10, "Colony size:", pos=(5,5))
        m_text = wx.StaticText(self.graphPanel, 13, "ants", pos=(115,5))
        m_text = wx.StaticText(self.graphPanel, 11, "Random initial pheromone", pos=(25,30))
        m_text = wx.StaticText(self.graphPanel, 12, "Ants can move back", pos=(25,55))
        m_text = wx.StaticText(self.graphPanel, 14, "times can revisit one spot.", pos=(55,80))
        m_text = wx.StaticText(self.graphPanel, 15, "Parameters:", pos=(250,5))
        m_text = wx.StaticText(self.graphPanel, 16, "alpha:", pos=(270,30))
        m_text = wx.StaticText(self.graphPanel, 19, "influence of pheromone", pos=(340,30))
        m_text = wx.StaticText(self.graphPanel, 17, "beta:", pos=(270,55))
        m_text = wx.StaticText(self.graphPanel, 20, "influence of travel costs", pos=(340,55))
        m_text = wx.StaticText(self.graphPanel, 18, "p:", pos=(270,80))
        m_text = wx.StaticText(self.graphPanel, 21, "pheromone evaporation", pos=(340,80))
        self.colonySizeCtrl = wx.TextCtrl(self.graphPanel, 30, pos = (70, 1), size = (40, 20))
        self.allowedLoopsCtrl = wx.TextCtrl(self.graphPanel, 33, pos = (25,77), size = (25, 20))
        self.aParamCtrl = wx.TextCtrl(self.graphPanel, 34, pos = (305,27), size = (29, 20))
        self.bParamCtrl = wx.TextCtrl(self.graphPanel, 35, pos = (305,52), size = (29, 20))
        self.pParamCtrl = wx.TextCtrl(self.graphPanel, 36, pos = (305,77), size = (29, 20))
        self.colonySizeCtrl.SetValue("1000")
        self.allowedLoopsCtrl.SetValue("5")
        self.aParamCtrl.SetValue("1")
        self.bParamCtrl.SetValue("5")
        self.pParamCtrl.SetValue("0.5")
        self.randomInitPheroChB = wx.CheckBox(self.graphPanel, 31, pos = (5, 30))
        self.canWalkBackChB = wx.CheckBox(self.graphPanel, 32, pos = (5, 55))

        self.calcBtn = wx.Button(self.graphPanel, 3, "Calculate", pos = (500, 1), size = (70, 30))
        self.calcBtn.Bind(wx.EVT_BUTTON, self.OnCalculate)

        self.statusbar = self.CreateStatusBar()
        self.Show(True)


    #Menu actions
    def OnAbout(self,e):
        d= wx.MessageDialog( self, " Bleble \n"
                            " Ble", wx.OK)# Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.cityNrCtrl.SetFocus()
        self.Close(True)  # Close the frame.

    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.asm", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.dataPath = os.path.join(self.dirname,self.filename)
            f=open(os.path.join(self.dirname,self.filename),'r')
            costMap = f.read()
            f.close()
            if(self.antSystem.readMap(costMap)):
                self.costMap = costMap

                #Updating grid------------------------------------------------------
                self.grid.DeleteCols(0, self.grid.GetNumberCols())
                self.grid.DeleteRows(0, self.grid.GetNumberRows())
                self.grid.AppendCols(len(self.antSystem.costMap))
                self.grid.AppendRows(len(self.antSystem.costMap))
                self.cityNrCtrl.SetValue(str(len(self.antSystem.costMap)))
                for i in range(len(self.antSystem.costMap)):
                    for j in range(len(self.antSystem.costMap)):
                        if self.antSystem.costMap[i][j] != ant_system.PosInf:
                            self.grid.SetCellValue(i, j, str(self.antSystem.costMap[i][j]))
                    self.grid.SetColLabelValue(i, str(i+1))
                    self.grid.SetRowLabelValue(i, str(i+1))
                    self.grid.SetCellBackgroundColour(i,i, wx.Colour(245, 245, 245))
                self.OnTable(None)
            else:
                d= wx.MessageDialog( self, "Excuse me Sir, Your map does not represent square matrix\nwith tab as a separator.", "Blarg!", wx.OK)
                d.ShowModal()
                d.Destroy()
            #self.pointCtrl.SetValue(f.read())

        dlg.Destroy()

    def OnSave(self,e):
        """ Save a file"""
        self.costMap = ""
        for i in range(self.grid.GetNumberRows()):
            for j in range(self.grid.GetNumberCols()):
                val = self.grid.GetCellValue(i, j)
                if val == "":
                    val = "."
                self.costMap += val
                if j < self.grid.GetNumberCols()-1:
                    self.costMap += "\t"
            self.costMap += "\n"

        if len(self.costMap) == 0:
            d= wx.MessageDialog( self, "Excuse me Sir, You haven't created map yet.", "Blarg!", wx.OK)
            d.ShowModal()
            d.Destroy()
        else:
            self.dirname = ''
            dlg = wx.FileDialog(self, "Choose a path", self.dirname, "", "*.asm", wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename=dlg.GetFilename()
                self.dirname=dlg.GetDirectory()
                self.dataPath = os.path.join(self.dirname,self.filename)
                f=open(os.path.join(self.dirname,self.filename),'w')
                f.write(self.costMap)
                f.close()
            dlg.Destroy()

    def OnTable(self,e):
        self.graphPanel.Show(False)
        self.tablePanel.Show(True)


    def OnGraph(self,e):
        #Transfer data to the AntSystem object
        self.antSystem.costMap = [[0]*self.grid.GetNumberRows() for i in range(self.grid.GetNumberRows())]
        for i in range(self.grid.GetNumberRows()):
            for j in range(self.grid.GetNumberCols()):
                val = self.grid.GetCellValue(i, j)
                if val == "":
                    self.antSystem.costMap[i][j] = PosInf
                else:
                    self.antSystem.costMap[i][j] = float(str(val))

        self.graphPanel.Show(True)
        self.tablePanel.Show(False)
        self.OnCalculate(None)

    #Grid panel events-----------------------------------------------------------
    def cityNrChange(self, e):
        oldSize = self.grid.GetNumberCols()
        newSize = int(self.cityNrCtrl.GetValue())
        diff = abs(oldSize - newSize)
        if oldSize < newSize:
            self.grid.AppendCols(diff)
            self.grid.AppendRows(diff)
        elif oldSize > newSize:
            self.grid.DeleteCols(newSize, diff)
            self.grid.DeleteRows(newSize, diff)

        for i in range(newSize):
            self.grid.SetColLabelValue(i, str(i+1))
            self.grid.SetRowLabelValue(i, str(i+1))
            self.grid.SetCellBackgroundColour(i,i, wx.Colour(245, 245, 245))



    #Plot panel events-------------------------------------------------------------
    def OnCalculate(self, e):
        self.antSystem.randomInitPhero = bool(self.randomInitPheroChB.GetValue())
        self.antSystem.colonySize = float(self.colonySizeCtrl.GetValue())
        self.antSystem.canWalkBack = bool(self.canWalkBackChB.GetValue())
        self.antSystem.allowedLoops = float(self.allowedLoopsCtrl.GetValue())
        self.antSystem.pParam = float(self.pParamCtrl.GetValue())
        self.antSystem.aParam = float(self.aParamCtrl.GetValue())
        self.antSystem.bParam = float(self.bParamCtrl.GetValue())
        self.antSystem.execute()
        self.graphPlot.Refresh()

    def OnPaintGraph(self, e):
        dc = wx.PaintDC(self.graphPlot)
        dc.SetPen(wx.Pen('gray', 1))
        rect = wx.Rect(5, 5, 984, 525)
        dc.DrawRectangleRect(rect)

        nrOfCities = len(self.antSystem.costMap)
        cityPerCol = math.sqrt(nrOfCities-2)
        cityColSpace = int(rect.width/(math.ceil(cityPerCol)+3))
        cityRowSpace = int(rect.height/(math.ceil(cityPerCol)+2))
        nrOfCol = 1
        posTable = [[0]*2 for i in range(nrOfCities)]

        #Calculate positions
        for i in range(nrOfCities):
            posX = 0
            posY = 0
            if i == 0:
                posX = rect.x+cityColSpace
                posY = rect.y+(int(rect.height/2))
            elif i == nrOfCities-1:
                posX = rect.x+rect.width-cityColSpace
                posY = rect.y+(int(rect.height/2))
            else:
                posX = rect.x+((nrOfCol+1)*cityColSpace)
                posY = rect.y+((i-math.floor(cityPerCol*(nrOfCol-1))))*cityRowSpace
                if cityPerCol*(nrOfCol) < i+1:
                    nrOfCol += 1
            posTable[i][0] = posX+random()*(cityColSpace/3)
            posTable[i][1] = posY+random()*(cityRowSpace/3)


        #Draw lines
        dc.SetPen(wx.Pen((160, 160, 160), 1, wx.DOT))#wx.SHORT_DASH))
        for i in range(nrOfCities):
            for j in range(i, nrOfCities):
                if self.antSystem.costMap[i][j] != PosInf:
                    #dc.DrawLine(posTable[i][0]+random()*4, posTable[i][1]+random()*4, posTable[j][0]+random()*4, posTable[j][1]+random()*4)
                    dc.DrawLine(posTable[i][0], posTable[i][1], posTable[j][0], posTable[j][1])

        #If possible, draw most optimal line
        dc.SetPen(wx.Pen((120, 120, 180), 2))#wx.SHORT_DASH))
        if self.antSystem.finalPath != None:
            dc.DrawText("Path: "+" -> ".join(map(lambda a: str(a), self.antSystem.finalPath)), 10, 10)
            dc.DrawText("Costs: "+" + ".join(map(lambda a: str(a), self.antSystem.finalCostsList)), 10, 30)
            dc.DrawText("Total cost: "+str(self.antSystem.finalCost), 10, 50)
            dc.DrawText("Execution time: "+str(self.antSystem.time)+"s", 10, 490)
            dc.DrawText("Dead ants: "+str(self.antSystem.deadAnts), 10, 510)

            for i in range(len(self.antSystem.finalPath)-1):
                #finalCostsList
                dc.DrawLine(posTable[self.antSystem.finalPath[i]][0], posTable[self.antSystem.finalPath[i]][1], posTable[self.antSystem.finalPath[i+1]][0], posTable[self.antSystem.finalPath[i+1]][1])
                dc.DrawText(str(self.antSystem.finalCostsList[i]), (posTable[self.antSystem.finalPath[i]][0]+posTable[self.antSystem.finalPath[i+1]][0])/2, (posTable[self.antSystem.finalPath[i]][1]+posTable[self.antSystem.finalPath[i+1]][1])/2)

        #Draw circles
        dc.SetPen(wx.Pen((140, 140, 140), 1))
        dc.SetBrush(wx.Brush((245,245,245)))
        for i in range(nrOfCities):
            if self.antSystem.finalPath.count(i) > 0:
                dc.SetBrush(wx.Brush((220,220,250)))
                dc.DrawCircle(posTable[i][0], posTable[i][1], 14)
            else:
                dc.SetBrush(wx.Brush((245,245,245)))
                dc.DrawCircle(posTable[i][0], posTable[i][1], 14)
            dc.DrawText(str(i+1), posTable[i][0]-6, posTable[i][1]-7)


app = wx.PySimpleApp()
frame = MainWindow(None, -1, "Ants System")
app.MainLoop()