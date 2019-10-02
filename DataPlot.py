# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 16:13:39 2018

@author: 李鹏飞
"""
import matplotlib.pyplot as plt
import numpy as np
import time



class MyTimer:
    def __init__(self):
        self.TimeOrgn = time.perf_counter()
    def GetCrrnTime(self):
        self.CrrnSec = time.perf_counter()
        self.DeltaTime = self.CrrnSec - self.TimeOrgn
        return self.DeltaTime


class FuncCollect:
    def __init__(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2
    
    def CosX(self):
        self.arg1 = self.arg1 + 0.1
        OutputY = np.cos(self.arg1)
        return OutputY
    
class DataPlotvsTime:
    def __init__(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def SetXTicks(self, ax_obj, XRange = 40, Xmax = 40):
        Xmin = Xmax - XRange
        ax_obj.set_xlim(Xmin,Xmax)
        ax_obj.set_xticks(np.linspace(Xmin,Xmax,6))
        
    def DynamicPlot(self,func1,func2):
        #Define counters 
        DataPointCounter = 0
        #Define variables
        timerVector = []
        DataVector = []
        FileNameExt = time.strftime("%d%m%Y_%H-%M-%S")
        #prepare plot
        figure1, ax1 = plt.subplots(1,1,sharey = True)
        plt.ion()
        plt.show()                                      
        
        while(1):
            #Counter increment
            DataPointCounter = DataPointCounter + 1
                       
            #Read Timer and Data
            CurrentTime = func1()
            #CurrentData = func2()
            CurrentData = func2(CurrentTime)

            #%%Plot Timer and Data, don't forget to clear data plot after 200 points to plot faster
            #otherwise the plot process will slow down the entire process
            XTickMax = CurrentTime
            XRange = 40
            Xmax = CurrentTime
            ax1.autoscale(enable = True)
            self.SetXTicks(ax1, XRange, int(XTickMax))
            ax1.plot(CurrentTime,CurrentData,linestyle = "-", linewidth = 2,
                     color = "red",marker = ".", markersize = 16,
                     markerfacecolor = "yellow",markeredgecolor = "blue")
            plt.pause(1e-6)
            plt.draw()
            #%%
            
            #%%Collect TimerVector and DataVector
            
            #%%Save TimerVector and DataVector into Excel file
            
            
            #%%Save TimerVector and DataVector into numpy data format, and clear the datavectors to avoid
            #super large vectors
            if DataPointCounter > 500:
                ax1.clear()
                DataPointCounter = 0
                
            
            
if __name__ == "__main__":
    Timer1 = MyTimer()
    DataGen = FuncCollect(1,2)
    DynamicPlt = DataPlotvsTime(1,2)
    #DynamicPlt.DynamicPlot(Timer1.GetCrrnTime,DataGen.CosX)
    DynamicPlt.DynamicPlot(Timer1.GetCrrnTime,np.cos)

    
