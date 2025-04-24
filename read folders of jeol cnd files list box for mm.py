#file reading
import pandas as pd
import tkinter
import tkinter.filedialog
import tkinter.simpledialog
import os
import datetime
import re
#plotting
import pyxray
import matplotlib.pyplot as plt
import numpy as np
import easygui
from numbers import Number
CrystalSelection = easygui.enterbox("Which crystal? LDE1, LDE2, TAP, PET, LIF")
folder_dir = tkinter.filedialog.askdirectory(title="Select directory containing exported wavescan files")
csvlocation = []
csvroot=[]
csvfile=[]
plotfiles=[]
plottitles=[]
commenttitle=[]
listcounter = 0
userwindow = tkinter.Tk()
userwindow.geometry('200x400')
Lb1 = tkinter.Listbox(userwindow, width=40, height=10, selectmode=tkinter.MULTIPLE)
for root, dirs, files in os.walk(folder_dir):
    for file in files:
        if file.endswith(".csv"):
            #print(root)
            #print(os.path.getmtime(root+'/'+file))
            #print(file)
            if '_mm' in file:
                try:
                    file2 = file.split('_mm.csv')[0]+'.cnd'
                    cnd=pd.read_csv(root+'/'+file2,names=["attribute"],header=None)
                    cnd[['attribute','value']]=cnd["attribute"].str.split(" ", n=1,expand=True)
                    cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]]
                    cnd['value'][cnd[cnd['attribute'].str.contains('ACQ_DATE')].index[0]]
                    cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]
                    if CrystalSelection in cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]:
                        print(cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('ACQ_DATE')].index[0]])
                        listcounter=listcounter+1
                        print (listcounter)
                        Lb1.insert(listcounter,cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('ACQ_DATE')].index[0]])
                        csvlocation.append(root+'/'+file)
                        csvroot.append(root)
                        csvfile.append(file)
                        commenttitle.append(cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]])
                except:
                    print(file+"an error occurred")
def selected_item():    
    for i in Lb1.curselection():
        print(i)
        print(csvlocation[i])
        print(csvroot[i])
        print(csvfile[i])
        #plotfiles.append(csvroot[i]+'/'+csvfile[i].split('.cnd')[0]+'_eV.csv')
        plotfiles.append(csvlocation[i])
        #print("selected items")
        #print(commenttitle)
        plottitles.append(commenttitle[i])
    plot_files()
def plot_files():
    print("Plot Files")
    print(plotfiles)
    TypesOfLines = easygui.enterbox("Which x-ray lines? Seperated by comma eg. Ka1, Kb1, La1, Ll etc")
    NoOfInterf = easygui.integerbox("How many orders of interference to plot? eg. 1,2 etc")
    ListOfElements = easygui.enterbox("Which elements? Seperated by comma eg. Fe, Mg etc")
    TypesOfLines = TypesOfLines.split(",")
    ListOfElements = ListOfElements.split(",")
    NoOfFiles = len(plotfiles)
    maxvalue=1
    LowerValue=62
    UpperValue=256
    for x in range(NoOfFiles):
        spectrafile=plotfiles[x]
        print(commenttitle)
        print(commenttitle[x])
        print(plottitles)
        FileLabel=plottitles[x]
        df = pd.read_csv(spectrafile, header=None,sep=',')
        plt.plot(df[0],df[1],label=FileLabel)
        #spectrafile.close()
        if df[1].max() > maxvalue:
            maxvalue=df[1].max()
        if df[0].min() < LowerValue:
            LowerValue=df[0].min()
        if df[0].max() > UpperValue:
            UpperValue=df[0].max()
    for x in range(len(TypesOfLines)):
        for xx in range(len(ListOfElements)):
            xrayline = pyxray.xray_line(ListOfElements[xx].strip(), TypesOfLines[x].strip())
            if isinstance(xrayline.relative_weight, Number):
                lineInMM = xrayline.energy_eV/1000
            else:
                lineInMM = 1
            if CrystalSelection.upper()=='LDE1':
                lineInMM = 57.861082*lineInMM**-0.999205
            if CrystalSelection.upper()=='TAP':
                dspace = 25.757
                lineInMM = ((12.398/lineInMM)*140/dspace)*2
            if CrystalSelection.upper()=='PET':
                dspace = 8.742
                lineInMM = ((12.398/lineInMM)*140/dspace)*2
            if CrystalSelection.upper()=='LIF':
                dspace = 4.027
                lineInMM = ((12.398/lineInMM)*140/dspace)*2
            for xxx in range(NoOfInterf):
                lineInMMn = lineInMM*(xxx+1)
                xpoints = np.array([lineInMMn, lineInMMn])
                StoreRelWeight=xrayline.relative_weight
                print(StoreRelWeight)
                if isinstance(xrayline.relative_weight, Number):
                    ypoints = np.array([0, StoreRelWeight*maxvalue/(xxx+1)])
                    ElementPlusLine = ListOfElements[xx]+TypesOfLines[x]+'-'+str(xxx+1)
                    LabelElementPlusLine ='_'+ElementPlusLine
                    if LowerValue <= lineInMMn <= UpperValue:
                        plt.rcParams.update({'font.size': 8})
                        plt.plot(xpoints,ypoints, label = LabelElementPlusLine,color='black',linewidth=0.5)
                        plt.text(lineInMMn,StoreRelWeight*maxvalue/(xxx+1),ElementPlusLine)
    if NoOfFiles > 0:
        plt.rcParams.update({'font.size': 12})
        plt.legend()
        plt.xlabel('L-value (mm)')
        plt.ylabel('Intensity')
        plt.show()
btn = tkinter.Button(userwindow, text='Plot Selected', command=selected_item)
btn.pack(side='bottom')
Lb1.pack()
userwindow.mainloop()