import pyxray
import matplotlib.pyplot as plt
import numpy as np
import easygui
import pandas
import tkinter
from numbers import Number
TypesOfLines = easygui.enterbox("Which x-ray lines? Seperated by comma eg. Ka1, Kb1, La1, Ll etc")
ListOfElements = easygui.enterbox("Which elements? Seperated by comma eg. Fe, Mg etc")
TypesOfLines = TypesOfLines.split(",")
ListOfElements = ListOfElements.split(",")
NoOfFiles = easygui.integerbox("Number of spectra to load")
maxvalue=0
for x in range(NoOfFiles):
    spectrafile=tkinter.filedialog.askopenfile()
    FileLabel=easygui.enterbox("Enter label for spectra")
    df = pandas.read_csv(spectrafile, header=None,sep=',')
    plt.plot(df[0],df[1],label=FileLabel)
    spectrafile.close()
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
plt.show()