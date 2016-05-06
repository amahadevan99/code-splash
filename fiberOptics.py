##Python 2.7.11 (v2.7.11:6d1b6a68f775, Dec  5 2015, 12:54:16) 
##[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
##Type "copyright", "credits" or "license()" for more information.
##>>> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable.
##Visit http://www.python.org/download/mac/tcltk/ for current information.

usage = "fiberOptics [--options]"
description = "the greatest code in the world"
author = "Reed Essick and Alvaro Fernandez"

#---------------------------------------------------------------------

import time

import numpy #numeric python

import datetime

import matplotlib
matplotlib.use("Agg")
#from matplotlib import pyplot as plt
import pylab as plt

#---------------------------------------------------------------------

global known_columns
global known_columns_types

#SETUPS
known_setups = ["F","FF","FT","FFF","FTF"] #the list of possible setups F = Fiber and T = Feedthrough

kc_F = ["day", "month", "year", "hour", "minute", "redPower(mW)", "greenPowerIn(mW)", "coupler", \
"fiberFirstConnector", "fiber", "greenPowerOut1(mW)"] ###the list of columns that each data point MUST have
kc_setup_F = ["coupler", "fiberFirstConnector", "fiber"] ###the list of columns that define
kct_F = [int, int, int, int, int, float, float, str, str, str, float]
#the types for the columns. THE ORDER MATTERS and this must have the same length as known_columns

kc_FF = ["day", "month", "year", "hour", "minute", "redPower(mW)", "greenPowerIn(mW)", "coupler", "fiber1FirstConnector", \
"fiber1", "greenPowerOut1(mW)", "sleeve", "fiber2FirstConnector", "fiber2", "greenPowerOut2(mW)"]
kc_setup_FF = ["coupler", "fiber1FirstConnector", "fiber1", "sleeve", "fiber2FirstConnector", "fiber2"]
kct_FF = [int, int, int, int, int, float, float, str, str, str, float, str, str, str, float]

kc_FT = ["day", "month", "year", "hour", "minute", "redPower(mW)", "greenPowerIn(mW)", "coupler", "fiber1FirstConnector", \
"fiber1", "greenPowerOut1(mW)", "sleeve", "feedthroughFirstConnector", "feedthroguh", "greenPowerOut2(mW)"]
kc_setup_FT = ["coupler", "fiber1FirstConnector", "fiber1", "sleeve", "feedthroughFirstConnector", "feedthroguh"]
kct_FT = [int, int, int, int, int, float, float, str, str, str, float, str, str, str, float]

kc_FFF = ["day", "month", "year", "hour", "minute", "redPower(mW)", "greenPowerIn(mW)", "coupler", "fiber1FirstConnector", \
"fiber1", "greenPowerOut1(mW)", "sleeve1", "fiber2FirstConnector", "fiber2", "greenPowerOut2(mW)", "sleeve2", \
"fiber3FirstConnector", "fiber3", "greenPowerOut3(mW)"]
kc_setup_FFF = ["coupler", "fiber1FirstConnector", "fiber1", "sleeve1", "fiber2FirstConnector", "fiber2", "sleeve2", \
"fiber3FirstConnector", "fiber3"]
kct_FFF = [int, int, int, int, int, float, float, str, str, str, float, str, str, str, float, str, str, str, float]

kc_FTF = ["day", "month", "year", "hour", "minute", "redPower(mW)", "greenPowerIn(mW)", "coupler", "fiber1FirstConnector", \
"fiber1", "greenPowerOut1(mW)", "sleeve1", "feedthroughFirstConnector", "feedthroguh", "greenPowerOut2(mW)", "sleeve2", \
"fiber3FirstConnector", "fiber3", "greenPowerOut3(mW)"]
kc_setup_FTF = ["coupler", "fiber1FirstConnector", "fiber1", "sleeve1", "feedthroughFirstConnector", "feedthroguh", \
"sleeve2", "fiber3FirstConnector", "fiber3"]
kct_FTF = [int, int, int, int, int, float, float, str, str, str, float, str, str, str, float, str, str, str, float]

kc_dict = {'STOP':["STOP"], 'F': kc_F, 'FF': kc_FF, 'FFF': kc_FFF, 'FT': kc_FT, 'FTF': kc_FTF}
kct_dict = {'STOP':[str], 'F': kct_F, 'FF': kct_FF, 'FFF': kct_FFF, 'FT': kct_FT, 'FTF': kct_FTF}
kc_setup_dict = {'F': kc_setup_F, 'FF': kc_setup_FF, 'FFF': kc_setup_FFF, 'FT': kc_setup_FT, 'FTF': kc_setup_FTF}

#COUPLERS
known_couplers = ["A", "B", "C"]
color_couplers = {'A': "b", 'B':"g", 'C':"m" }
couplers = dict([('A', "New coupler"), ('B', "Old coupler"), ('C', "Broken coupler")])

#FIBERS
known_fibers = ["1A", "1B", "1C", "5A", "5B", "5C", "5D", "5E", "5F"]
fibers = dict([('A', "New coupler"), ('B', "Old coupler"), ('C', "Broken coupler")])
known_fibers_setup = ["fiber1", "fiber2", "fiber3"]

#FEEDTHROUGHS
known_feedthroughs = ["A", "B", "C"]
#feedthroughs = dict([('A', "New coupler"), ('B', "Old coupler"), ('C', "Broken coupler")])

#SLEEVES
known_sleeves = ["A", "B", "C", "D", "E"]
line_sleeves = {'A': "r", 'B': "c", 'C': '0.75', 'D': "y", 'E': "0.5"}
#sleeves = dict([('A', "New coupler"), ('B', "Old coupler"), ('C', "Broken coupler")])

#CONNECTORS DICTIONARY
line_connectors = {'A': '-', 'B': '--'}

#ACTIONS
known_actions = ["enterData", "printData", "makeFigure", "save", "load", "notifyStop", "exit"]

#POWER DICTIONARY
powerList = [{'name': "Very High Power", 'min': 250, 'max': 350}, {'name': "High Power", 'min': 200, 'max': 250}, \
{'name': "Medium Power", 'min': 100, 'max': 200}, {'name': "Low Power", 'min': 50, 'max': 100}, \
{'name': "Very Low Power", 'min': 0, 'max': 50}]

#---------------------------------------------------------------------

class dataPoint(object):

    def __init__(self, name):
        self.name = name
        self.setup = None
        #self.data = dict((col, None) for col in known_columns)
        self.data = dict() #equivalently, self.data = {}

    #sychronizes self.data with setupDictionary according to the appropriate setup of fibers and feedthroughs
    def completeSetup(self, setup, setupDictionary):
        self.setup = setup
        for col in kc_dict[setup]:
            if col in setupDictionary:
                self.data[col] = setupDictionary[col]
            else:
                self.data[col] = None

    #reads in columns from the command line
    def readFromTerminal(self):
        #iterate over the known columns and read stuff in from the terminal
        #we "zip" together the column names and their types to make the iteration "simpler"
        for cast2type, col in zip(known_columns_types, known_columns):
            if self.data[col] == None:
                self.data[col] = cast2type(raw_input("what is the value for  "+col+" : "))
            else:
                pass

    #prints to terminal
    def printToTerminal(self):
        print str(self.name) + " " + str(self.setup)
        for col in kc_dict[self.setup]:
            print "    value stored for "+col+" : "+str(self.data[col])

#---------------------------------------------------------------------

def readSetup(setup):
    setupDictionary[setup] = setup
    for col in kc_setup_dict[setup]:
        setupDictionary[col] = str(raw_input("what is the value for  "+col+" : "))  
    return setupDictionary
    #a, b = makeMommaProud(1,1)

def save(dataPoints):
    if not dataPoints:
        "There is nothing to save"

    else:
        filename = raw_input("what filename do you want to use to save the data?")
        file_obj = open(filename, "w")
        #print >> file_obj, "name " + "setup " +" ".join(known_columns)
        for thisDataPoint in dataPoints:
            #print str(thisDataPoint.name)
            #print str(thisDataPoint.setup)
            #print " ".join(str(thisDataPoint.data[col]) for col in kc_dict[thisDataPoint.setup])
            print >> file_obj, str(thisDataPoint.name) + " " + str(thisDataPoint.setup) + \
            " " + " ".join(str(thisDataPoint.data[col]) for col in kc_dict[thisDataPoint.setup])
        file_obj.close()

def assignNumber(fiber):
    return int(list(fiber)[5])

def getTime (dataPoint):
    print dataPoint.data['minute']
    return datetime.datetime(dataPoint.data['year'], dataPoint.data['month'], dataPoint.data['day'], \
        dataPoint.data['hour'], dataPoint.data['minute'])

def definePower (inPower):
    power = None
    for range in powerList:
        if inPower>= range['min'] and inPower< range['max']:
            power = range['name']
        if not power:
            print "This is power is out of the range. Power = "+inPower+" !!"
            #print str(inPower)
    return power

#given a position and a dataPoint, gets the information about the fiber in this position
def getFiberInfo(position, dataPoint):
    info = {}
    if position == 1:
        info = {'time': getTime(dataPoint), 'pos': position, 'coupler': dataPoint.data['coupler'], 'firstConnector': \
        dataPoint.data["fiber"+str(position)+"FirstConnector"], 'transmission': \
        dataPoint.data['greenPowerOut1(mW)']/dataPoint.data['greenPowerIn(mW)'], 'power': \
        definePower(dataPoint.data['greenPowerIn(mW)'])}
    elif position == 2 or position==3:
        info = {'time': getTime(dataPoint), 'pos': position, 'sleeve': dataPoint.data["sleeve"+str(position-1)], \
        'firstConnector': dataPoint.data["fiber"+str(position)+"FirstConnector"], 'transmission': \
        dataPoint.data["greenPowerOut"+str(position)+"(mW)"]/dataPoint.data["greenPowerOut"+str(position-1)+"(mW)"], \
        'power': definePower(dataPoint.data["greenPowerOut"+str(position-1)+"(mW)"])}
    else:
        print "This position of the fiber is not possible"

    return info

#returns a dictionary with the information (time, position, etc.) of a particular fiber, given the fiber and a data point.
#returns and empty dictionary otherwise.
def getFiberInDataPoint(dataPoint, fiber):
    fiberInDataPointInfo = {}
    if fiber not in known_fibers:
        print "Sorry I do not recognize this fiber"

    else:
        for fib in known_fibers_setup:
            if fib in dataPoint.data.keys() and dataPoint.data[fib] == fiber:
                fiberInDataPointInfo = getFiberInfo(assignNumber(fib), dataPoint)
            else:
                pass

    return fiberInDataPointInfo

#goes through a list of dataPoints extracting the information pertaining to a particular fiber
def getFiberHistory (fiber, dataPoints):
    fiberInfo = [] #list of dictionaries
    actualFiber = {}
    if fiber not in known_fibers:
        print "Sorry I do not recognize this fiber"
    else:
        for point in dataPoints:
            if point.setup == "STOP":
                fiberInfo.append({'NOT': "NOT"})
            else:
                actualFiber = getFiberInDataPoint(point, fiber)
                if not actualFiber:
                    fiberInfo.append({'NOT': "NOT"})
                else:
                    fiberInfo.append(actualFiber)
    return fiberInfo


#sets the type/color/etc. of lines of the plots
def defineArgs(point):
    selectedColor = 'k'
    selectedStyle = ':'
    selectedWidth = 0
    if 'coupler' in point:
        selectedColor = line_couplers[point['coupler']]
    else:
        selectedColor = color_couplers[point['sleeve']]
    selectedWidth = -2*point['position']+8
    selectedStyle = line_connectors[point['firstConnector']]
    return {'color': selectedColor,'linestyle':selectedStyle, 'markerstyle':"none", 'label':None, 'linewidth':selectedWidth}

#defines the plot to be drawn according to the power level
def selectedPlot(power, listOfPlots):
    for i, plot in listOfPlots:
        if power >= powerList[i]['min'] and power < powerList[i]['max']:
            break
    return plot

#sets the labels of the plots according to the list of power
def setPlotLabels(listOfPlots):
    for i, plots in listOfPlots:
        plots.set_ylabel(powerList[i]['name'] + "Trans")
        plots.set_xlabel("Time")


#defines and sets the list of plots according to the list of power
def createPlots():
    plotsList = []
    lenght = len(powerList)
    i = 1
    while i<=lenght:
        newPlot = plt.subplot(lenght,1,i)
        plotsList.append(newPlot)
        i = i+1
    return plotsList

#---------------------------------------------------------------------

def plotMe(data):
    fig = plt.figure()
    plotList = createPlots()
    #ax_H = plt.subplot(2,1,1) #2 rows, 1 column, 1 at panel
    #ax_L = plt.subplot(2,1,2)
    #plotList = [ax_H, ax_L]
    selectedPlot = None
    passing = True
    totalTime = datetime.timedelta()
    totalHTime = datetime.timedelta()
    totalLTime = datetime.timedelta()
    timeDifference = datetime.timedelta()
    previousTime = data[0]['time']
    actualTime = datetime.timedelta(1991,7,18)
    actualPower = None
    previousPower = data[0]['power']
    x = []
    y = []
    for point in data:
        if 'NOT' in point:
            if not passing:
                passing = True
                kwargs = defineArgs(point)
                selectPlot(previousPower, plotList).plot(x,y,**kwargs)
        else:
            actualPower = definePower(point['power'])
            actualTime = point['time']
            if passing:
                passing = False
                previousPower = actualPower
                previousTime = actualTime
            if actualPower != previousPower:
                kwargs = defineArgs(point)
                selectPlot(previousPower, plotList).plot(x,y,**kwargs)
                #if passing:
                    #x.add(timeToValue(totalTime))
                    #else:
            timeDifference = actualTime - previousTime
            totalTime =+ timeDifference
            x.add(timeToValue(totalTime))
            y.add(point['transmission'])
            previousTime = actualTime
            previousPower = actualPower
            #ax_H.plot(x,y,color=asignedColor,linestyle=asignedStyle, markerstyle="none", label=None, linewidth=asignedWidth)

    xmin = numpy.infty
    xmax = - numpy.infty
    for x in plotList:
        xlim = x.get_xlim()
        if xlim[0]<xmin:
            xmin=xlim[0]
        else:
            pass
        if xlim[1]>xmax:
            xmax=xlim[1]
    for x in plotList:
        x.set_xlim(xmin=xmin, xmax=xmax)
        x.set_ylim(ymin=0, ymax=100)
        #x.grid(True)

    setPlotLabels(plotList)
    '''
    ax_H.set_ylabel("High Power Trans")
    ax_L.set_ylabel("Low Power Trans")
    ax_H.set_xlabel("Time")
    ax_L.set_xlabel("Time")
    ax_H.legend(loc="best") #best location
    '''
    plt.savefig("FIGURE1.png") #jpg pdf ...
    plt.show()
    plt.close(fig)

#---------------------------------------------------------------------

#perform the main loop

dataPoints = [] #instantiate an empty list object
setup = "No defined setup"
setupDictionary = {}
'''
file_obj = open("fiber.txt", "r")
    #       cols = file_obj.readline().strip().split()[1:]
    #if cols != known_columns:
    #   print "whoops! looks like the columns don't match what I expected"
    #else:
for line in file_obj:
    line = line.strip().split()
    newDataPoint = dataPoint(float(line[0]))
    newDataPoint.setup = str(line[1])
    for ind, (cast2type, col) in enumerate(zip(kct_dict[newDataPoint.setup], kc_dict[newDataPoint.setup])):
        newDataPoint.data[col] = cast2type(line[ind+2])
    dataPoints.append(newDataPoint)
setup = newDataPoint.setup
file_obj.close()

plotMe(getFiberHistory("1A", dataPoints))
'''

#---------------------------------------------------------------------

#USER INTERFACE
while True:

    #figure out what user wants to do
    action = raw_input("what do you want to do? You can say one of ["+"/".join(known_actions)+"] ")
    while action not in known_actions:
        action = raw_input("I don't understand that. You can say one of ["+"/".join(known_actions)+"] ")

    #fork program based on what we want to do
    if action == "enterData":
        isSameSetup = raw_input("is it the same layout as before (%s)? y/n " %(setup))

        if isSameSetup == "n":
            #save(dataPoints)
            setup = raw_input("which setup are you using ["+"/".join(known_setups)+"] ")

            if setup in known_setups:
                known_columns = kc_dict[setup]
                known_columns_types = kct_dict[setup]
            else:
                raise ValueError("I don't understand your setup (%s)."%(setup))

            setupDictionary = readSetup(setup)

        elif isSameSetup == "y":
            pass

        else:
            print "I do not understand your answer, please say y/n"
        
        newDataPoint = dataPoint(time.time())
        newDataPoint.completeSetup(setup, setupDictionary)
        newDataPoint.readFromTerminal()
        dataPoints.append(newDataPoint)

    elif action == "printData":
        for dataPoint in dataPoints:
            dataPoint.printToTerminal()

    elif action == "makeFigure":
        fiberToPlot = raw_input("which fiber do you want to plot? You can say one of ["+"/".join(known_fibers)+"] ")
        plotMe(getFiberHistory(fiberToPlot, dataPoints))

    elif action == "save":
        save(dataPoints)

    elif action == "load":
        filename = raw_input("what filename do you want to load?")
        file_obj = open(filename, "r")
        #cols = file_obj.readline().strip().split()[1:]
        #if cols != known_columns:
           #print "whoops! looks like the columns don't match what I expected"
        #else:
        for line in file_obj:
            line = line.strip().split()
            newDataPoint = dataPoint(float(line[0]))
            newDataPoint.setup = str(line[1])
            for ind, (cast2type, col) in enumerate(zip(kct_dict[newDataPoint.setup], kc_dict[newDataPoint.setup])):
                    newDataPoint.data[col] = cast2type(line[ind+2])
            dataPoints.append(newDataPoint)
        setup = newDataPoint.setup
        file_obj.close()

    elif action == "notifyStop":
        newDataPoint = dataPoint(time.time())
        newDataPoint.setup = "STOP"
        newDataPoint.data = {'STOP': "STOP"}
        dataPoints.append(newDataPoint)

    elif action == "exit":
        print "goodbye"
        break
        
    time.sleep(1) #sleep for 1 second before continuing the loop 

'''
        print "by \"makeFigure\" I assume you mean make a histogram of the values of \"b\" recorded"
        figname = raw_input("what do you want to call your figure?")
        
        fig = plt.figure()
        ax = fig.gca() ###get current axis

        ###extract the data I want toTHan plot
        data = [d.data["b"] for d in dataPoints]

        ax.hist(data, bins=10, label="b")        

        ax.set_xlabel("b")
        ax.set_ylabel("count")

        ax.grid(True)

        ax.legend(loc='upper right')

        fig.savefig(figname)
        plt.close(fig)
''' 