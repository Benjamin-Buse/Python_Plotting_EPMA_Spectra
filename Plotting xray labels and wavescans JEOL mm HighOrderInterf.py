import pyxray
import matplotlib.pyplot as plt
import numpy as np
import easygui
import pandas
import tkinter
from numbers import Number
CrystalSelection = easygui.enterbox("Which crystal? LDE1, TAP, PET, LIF")
TypesOfLines = easygui.enterbox("Which x-ray lines? Seperated by comma eg. Ka1, Kb1, La1, Ll etc")
NoOfInterf = easygui.integerbox("How many orders of interference to plot? eg. 1,2 etc")
ListOfElements = easygui.enterbox("Which elements? Seperated by comma eg. Fe, Mg etc")
TypesOfLines = TypesOfLines.split(",")
ListOfElements = ListOfElements.split(",")
NoOfFiles = easygui.integerbox("Number of spectra to load")
maxvalue=1
LowerValue=62
UpperValue=256
for x in range(NoOfFiles):
    spectrafile=tkinter.filedialog.askopenfile()
    FileLabel=easygui.enterbox("Enter label for spectra")
    df = pandas.read_csv(spectrafile, header=None,sep=',')
    plt.plot(df[0],df[1],label=FileLabel)
    spectrafile.close()
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
                    plt.plot(xpoints,ypoints, label = LabelElementPlusLine,color='black')
                    plt.text(lineInMMn,StoreRelWeight*maxvalue/(xxx+1),ElementPlusLine)
if NoOfFiles > 0:
    plt.legend()
plt.xlabel('L-value (mm)')
plt.ylabel('Intensity')
plt.show()