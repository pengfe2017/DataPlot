# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 16:13:39 2018

@author: 李鹏飞
"""
#%%
import matplotlib
from matplotlib import _pylab_helpers
from matplotlib.rcsetup import interactive_bk as _interactive_bk
#matplotlib.use('Qt4agg')
import matplotlib.pyplot as plt
import numpy as np
import time
import itertools
from Class_Simple_Function_Collections import SimpleFunctionCollections

#%%
class MyTimer:
    def __init__(self):
        self.TimeOrgn = time.perf_counter()
    def GetCrrnTime(self):
        self.CrrnSec = time.perf_counter()
        self.DeltaTime = self.CrrnSec - self.TimeOrgn
        return self.DeltaTime

#%%
class FuncCollect:
    def __init__(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2
    
    def CosX(self):
        self.arg1 = self.arg1 + 0.1
        OutputY = np.cos(self.arg1)
        return OutputY
    
    def cos_v0(self,x):
        return np.cos(x*2)
    
    def sin_v0(self,x):
        return np.sin(x*2)
    
    def avg_cos_sin(self,x):
        avg = np.cos(x)+np.sin(x)
        return avg
#%%    
class DataPlotvsTime:
    def __init__(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def SetXTicks(self, ax_obj, XRange = 40, Xmax = 40):
        Xmin = Xmax - XRange
        ax_obj.set_xlim(Xmin,Xmax)
        ax_obj.set_xticks(np.linspace(Xmin,Xmax,6))
                
    def pause(self,interval, focus_figure=False):
        """
        Pause for *interval* seconds.
        If there is an active figure it will be updated and displayed,
        and the GUI event loop will run during the pause.
        If there is no active figure, or if a non-interactive backend
        is in use, this executes time.sleep(interval).
        This can be used for crude animation. For more complex
        animation, see :mod:`matplotlib.animation`.
        This function is experimental; its behavior may be changed
        or extended in a future release.
        """
        backend = matplotlib.rcParams['backend']
        if backend in _interactive_bk:
            figManager = _pylab_helpers.Gcf.get_active()
            if figManager is not None:
                canvas = figManager.canvas
                if canvas.figure.stale:
                    canvas.draw()
                if focus_figure:
                    plt.show(block=False)
                canvas.start_event_loop(interval)
                return    
        # No on-screen figure is active, so sleep() is all we need.
        import time
        time.sleep(interval)
        
#%%        
    def DynamicPlot(self,GetCurrentTimeFunc,ReservedFunc=1,*args):
        #make sure all passing arguments are methods.
        #Define counters and constants
        DataPointCounter = 0
        NumberofData = len(args)
        print("You have {} of arbituary arguments.".format(NumberofData))
        FileNameExt = time.strftime("%d%m%Y_%H-%M-%S")
        SFC_obj = SimpleFunctionCollections()
        Limit_LengthofVectors = 500
        TemperatureLimit = 120
                
        #Define variables
        TimerVector = []#for time
        DataMatrix_ListType = [[] for idx in range(NumberofData)]#for all other data
        
        #prepare plot
        figure1, ax1 = plt.subplots(1,1,sharey = True)
        #figure1.canvas.manager.window.attributes('-topmost', 0)

        plt.ion()
        plt.show(block = False)                                      
        
        while(1):
            time.sleep(.1)
            #Counter increment
            DataPointCounter = DataPointCounter + 1
                       
            #Read Timer and Data
            CurrentTime = GetCurrentTimeFunc()
            CurrentReservedVariable = ReservedFunc            
            
            CurrentData = []
            for idx in range(NumberofData):
                CurrentData.append(args[idx](CurrentTime))
            
            LengthofTimerVector = len(TimerVector)
            #%%save all data
            #1. save time
            TimerVector.append(CurrentTime)
            #2. save all other data
            for idx in range(NumberofData):
                DataMatrix_ListType[idx].append(CurrentData[idx])
            #print(DataMatrix_ListType)

            #%%Plot Timer and Data, don't forget to clear data plot after 200 points to plot faster
            #otherwise the plot process will slow down the entire process
            XTickMax = CurrentTime
            XRange = 40
            ax1.autoscale(enable = True)
            self.SetXTicks(ax1, XRange, int(XTickMax))
            
            markers = itertools.cycle(("+","*","o"))
            for idx in range(NumberofData):
                
                ax1.plot(CurrentTime,CurrentData[idx],linestyle = "-", linewidth = 2,
                         color = "red",marker = next(markers), markersize = 16,
                         markerfacecolor = "yellow",markeredgecolor = "blue")
            plt.draw()
            #plt.pause(1e-6)
            self.pause(1e-6)
            #%% Reserved space for other scripts
            
            #%%Save TimerVector and DataVector into Excel file, with periodic saving                
            if LengthofTimerVector > Limit_LengthofVectors:
                #np.save("npvariable",DataMatrix_ListType)
                #np.save("Time",TimerVector)
                DataMatrix_ListType.append(TimerVector)
                DataMatrix_npy_array = np.array(DataMatrix_ListType)
                #DataMatrix_npy_array.reshape((len(TimerVector),5))#notice this is wrong
                DataMatrix_npy_array = np.transpose(DataMatrix_npy_array)
                
                SFC_obj.Save_Matrix2CSV_with_TimeStamp("DataMatrix_npy_array",DataMatrix_npy_array)
                
                TimerVector = []#for time
                LengthofTimerVector = len(TimerVector)
                DataMatrix_ListType = [[] for idx in range(NumberofData)]#for all other data
                ax1.clear()
                
            
            #%%Turn off 
            with open("ProgramStopFlag.txt","r") as f:
                ProgramStopFlag = f.read()
                ProgramStopFlag = int(ProgramStopFlag)
                
            if TemperatureLimit > 130 or abs(ProgramStopFlag - 1 )<1e-6:
                #np.save("npvariable",DataMatrix_ListType)
                #np.save("Time",TimerVector)
                DataMatrix_ListType.append(TimerVector)
                DataMatrix_npy_array = np.array(DataMatrix_ListType)
                DataMatrix_npy_array = np.transpose(DataMatrix_npy_array)
                
                SFC_obj.Save_Matrix2CSV_with_TimeStamp("DataMatrix_npy_array",DataMatrix_npy_array)
                
                TimerVector = []#for time
                LengthofTimerVector = len(TimerVector)
                DataMatrix_ListType = [[] for idx in range(NumberofData)]#for all other data
                #ax1.clear()
                
                print("You manually stopped the app, and all data is saved, you can leave~")
                break
            
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
    ReservedFunc = np.cos
    DynamicPlt.DynamicPlot(Timer1.GetCrrnTime,ReservedFunc,np.sin,np.cos,DataGen.avg_cos_sin,DataGen.cos_v0)

    
