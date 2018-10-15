from glob import glob
import os
from tkinter import *
from getopt import getopt
import subprocess

## TODO:
##  fill iAmTheOwner for each job
##  open/select more than one item
##  search keywords(with AND/OR options) in title/content
##  support directories

#Struct for JobInfo
#from collections import namedtuple
#JobInfo = namedtuple("JobInfo", "SR, JobID, Title, System, Content, Solution, FilePaths, FileContents, ImTheOwner")

class JobInfo(object):
    def __init__(self):
        self.sr = ""
        self.jobId = ""
        self.title = ""
        self.system = ""
        self.content = ""
        self.solution = ""
        self.filePaths = None
        self.fileContents = None
        self.iAmTheOwner = True
        self.completed = True

class JobsReaper(object):
    def __init__(self, dataPath="Jobs"):
        self.dataPath = dataPath
        self.jobsList = []
        self.foundResults = None
        self.UpdateFilePaths()
        self.UpdateList()

        self.cmdMap={'showsr': self.CMDshowsr,\
                     'showjob': self.CMDshowjob,\
                     'open': self.CMDopen,\
                     'select': self.CMDselect,\
                     'exit': self.CMDexit}

    def UpdateList(self):
        for file in self.inputPaths:
            newJob = JobInfo()
            filename = os.path.split(file)[1][0:-4]
            if filename[0] == '-':
                filename = filename[1:]
                newJob.completed = False
            parts = [ part.strip() for part in filename.split('-')]
            newJob.sr = parts[0].split(' ')[0][-6:]
            newJob.jobId = parts[0].split(' ')[1]
            newJob.system = parts[1]
            newJob.title = parts[2:]
            newJob.filePaths = [file]
            with open(file) as fileContent:
                newJob.fileContents = fileContent.read()
            # TODO newJob.iAmTheOwner
            self.jobsList += [newJob]

    def UpdateFilePaths(self):
        # Import TXT and SQL jobs
        self.inputPaths = glob(self.dataPath+"\\*.txt") + glob(self.dataPath+"\\*.sql") + glob(self.dataPath+"\\_Other\\*.txt") + glob(self.dataPath+"\\_Other\\*.sql")

        # Import jobs with multiple files (diredtories)
        #print([x[0] for x in os.walk('.')]) # good solution but is recurrent
        self.inputDirPaths = [o for o in os.listdir(self.dataPath+'\\') if os.path.isdir(self.dataPath+'\\'+o) and o[0] != '_']
        self.inputDirPaths += [o for o in os.listdir(self.dataPath+'\\_Other\\') if os.path.isdir(self.dataPath+'\\_Other\\'+o)]

    def CMDRun(self):
        while True:
            cmd = input("$> ").split()
            
            # Validate data
            if not cmd or len(cmd) < 2:
                continue
            
            mainCmd = cmd[0].lower()

            if(mainCmd.startswith("exit")):
                self.cmdMap['exit'](*cmd[1:])
                break #Should save all changes
            elif(mainCmd in self.cmdMap.keys()):
                self.cmdMap[mainCmd](*cmd[1:])

    def CMDshowall(self, *args):
        self.foundResults = self.jobsList[:] # make a copy just in case
        self.CMDPrintResults()

    def CMDshowsr(self, *args):
        self.foundResults = [x for x in self.jobsList if args[0] in x.sr or args[0] == "*"]
        self.CMDPrintResults()

    def CMDshowjob(self, *args):
        self.foundResults = [x for x in self.jobsList if args[0].lower() in x.jobId.lower() or args[0] == "*"]
        self.CMDPrintResults()

    def CMDselect(self, *args):
        itemId = int(args[0])
        if itemId > 0 and itemId <= len(self.foundResults):
            #print("Selecting: {0}".format(self.foundResults[itemId-1].filePaths[0]))
            subprocess.call("explorer /select, \""+self.foundResults[itemId-1].filePaths[0]+"\"", shell=True)
        else:
            print("No such result.")

    def CMDopen(self, *args):
        itemId = int(args[0])
        if itemId > 0 and itemId <= len(self.foundResults):
            #print("Opening: {0}".format(self.foundResults[itemId-1].filePaths[0]))
            subprocess.Popen("notepad \""+self.foundResults[itemId-1].filePaths[0]+"\"", shell=True)
        else:
            print("No such result.")

    def CMDexit(self):
        pass # Do nothing at the moment
                    
    def CMDPrintResults(self):
        if self.foundResults:
            for x in range(len(self.foundResults)):
                print("{1:3d}. {0.sr} {0.jobId}\t{0.system} - {0.title}".format(self.foundResults[x], x+1))
            


jr = JobsReaper()
jr.CMDRun()


# Interface
##
##class Application(Frame):
##    def say_hi(self):
##        print("hi there, everyone!")
##
##    def createWidgets(self):
##        self.QUIT = Button(self)
##        self.QUIT["text"] = "QUIT"
##        self.QUIT["fg"] = "red"
##        self.QUIT["command"] = self.quit
##
##        self.QUIT.pack({"side": "left"})
##
##        self.hi_there = Button(self)
##        self.hi_there["text"] = "Hello",
##        self.hi_there["command"] = self.say_hi
##
##        self.hi_there.pack({"side": "left"})
##
##    def __init__(self, master=None):
##        Frame.__init__(self, master)
##        self.pack()
##        self.createWidgets()
##
##root = Tk()
##app = Application(master=root)
##app.mainloop()
##root.destroy()
##
