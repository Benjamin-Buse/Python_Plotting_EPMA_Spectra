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
            print(file)
            if '_eV' in file:
                file2 = file.split('_eV.csv')[0]+'.cnd'
                cnd=pd.read_csv(root+'/'+file2,names=["attribute"],header=None)
                cnd[['attribute','value']]=cnd["attribute"].str.split(" ", n=1,expand=True)
                cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]]
                cnd['value'][cnd[cnd['attribute'].str.contains('ACQ_DATE')].index[0]]
                cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]
                print(cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('ACQ_DATE')].index[0]])
                listcounter=listcounter+1
                Lb1.insert(listcounter,cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('CRYSTAL_NAME')].index[0]]+" "+cnd['value'][cnd[cnd['attribute'].str.contains('ACQ_DATE')].index[0]])
                csvlocation.append(root+'/'+file)
                csvroot.append(root)
                csvfile.append(file)
                commenttitle.append(cnd['value'][cnd[cnd['attribute'].str.contains('AP_COMMENT%0')].index[0]])
def selected_item():    
    for i in Lb1.curselection():
        print(i)
        print(csvlocation[i])
        print(csvroot[i])
        print(csvfile[i])
        #plotfiles.append(csvroot[i]+'/'+csvfile[i].split('.cnd')[0]+'_eV.csv')
        plotfiles.append(csvlocation[i])
        plottitles.append(commenttitle[i])
    plot_files()
def plot_files():
    print("Plot Files")
    print(plotfiles)
    TypesOfLines = easygui.enterbox("Which x-ray lines? Seperated by comma eg. Ka1, Kb1, La1, Ll etc")
    ListOfElements = easygui.enterbox("Which elements? Seperated by comma eg. Fe, Mg etc")
    TypesOfLines = TypesOfLines.split(",")
    ListOfElements = ListOfElements.split(",")
    NoOfFiles = len(plotfiles)
    maxvalue=0
    for x in range(NoOfFiles):
        FileLabel=plottitles[x]
        df = pd.read_csv(plotfiles[x], header=None,sep=',')
        plt.plot(df[0],df[1],label=FileLabel)
        #spectrafile.close()
        if df[1].max() > maxvalue:
            maxvalue=df[1].max()
    for x in range(len(TypesOfLines)):
        for xx in range(len(ListOfElements)):
            xrayline = pyxray.xray_line(ListOfElements[xx].strip(), TypesOfLines[x].strip())
            xpoints = np.array([xrayline.energy_eV, xrayline.energy_eV])
            StoreRelWeight=xrayline.relative_weight
            print(StoreRelWeight)
            if isinstance(xrayline.relative_weight, Number):
                ypoints = np.array([0, StoreRelWeight*maxvalue])
                ElementPlusLine = ListOfElements[xx]+TypesOfLines[x]
                LabelElementPlusLine ='_'+ElementPlusLine
                plt.plot(xpoints,ypoints, label = LabelElementPlusLine,color='black')
                plt.text(xrayline.energy_eV,StoreRelWeight*maxvalue,ElementPlusLine)
    plt.legend()
    plt.xlabel('Energy (eV)')
    plt.ylabel('Intensity')
    plt.show()
btn = tkinter.Button(userwindow, text='Plot Selected', command=selected_item)
btn.pack(side='bottom')
Lb1.pack()
userwindow.mainloop()