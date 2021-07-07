import tkinter as tk
from tkinter import ttk

def makeWindow():
    values = []
    def returnEntries(entries, boolEntries):
        canContinue = True
        for entry in entries:
            values.append(entry.get())
        for boolEntry in boolEntries:
            values.append(boolEntry.get())
        if (values[0] == '' or values[1] == '' or values[2] == '' or values[3] == '' or values[4] == '' or values[5] == '' or values[6] == ''):
            canContinue = False
        if values[10] == True and values[7] == '':
            canContinue = False
        if canContinue == True:
            window.destroy()

    window = tk.Tk()

    titleLabel = tk.Label(window, text="Diffusion\Reaction Model")
    titleLabel.config(font=("Courier", 26))
    titleLabel.grid(row=0, column = 0, padx = 5, pady = 5, columnspan = 8)

    gridSizeText = tk.Label(window, text="Grid Size:")
    gridSizeText.grid(row=3, column=1, sticky='e')

    gridSizeEntryCol = tk.Entry(window, width = 5)
    gridSizeEntryCol.grid(row=3, column = 2)
    gridSizeEntryCol.insert(0, 50)

    gridSizeX = tk.Label(window, text='X')
    gridSizeX.grid(row=3, column=3)

    gridSizeEntryRow = tk.Entry(window, width = 5)
    gridSizeEntryRow.grid(row=3, column = 4)
    gridSizeEntryRow.insert(0, 50)

    separator1 = ttk.Separator(window, orient='horizontal')
    separator1.grid(row=4, column = 0, columnspan = 8, sticky='ew', pady=5)

    diffCoeffText = tk.Label(window, text="Diffusion coefficients")
    diffCoeffText.config(font=('Courier', 22))
    diffCoeffText.grid(row=5, column = 1, padx = 5, pady = 5, columnspan=6)

    diffCoeffTextS1 = tk.Label(window, text="Source 1")
    diffCoeffTextS1.grid(row=6, column = 0, columnspan = 2)

    diffCoeffEntryS1 = tk.Entry(window, width = 5)
    diffCoeffEntryS1.grid(row=7, column = 0, columnspan = 2)
    diffCoeffEntryS1.insert(0, 0.8)

    diffCoeffTextS2 = tk.Label(window, text="Source 2")
    diffCoeffTextS2.grid(row=6, column = 2, columnspan = 2)

    diffCoeffEntryS2 = tk.Entry(window, width = 5)
    diffCoeffEntryS2.grid(row=7, column = 2, columnspan = 2)
    diffCoeffEntryS2.insert(0, 0.8)

    diffCoeffTextB1 = tk.Label(window, text="Boundary 1")
    diffCoeffTextB1.grid(row=6, column = 4, columnspan = 2)

    diffCoeffEntryB1 = tk.Entry(window, width = 5)
    diffCoeffEntryB1.grid(row=7, column = 4, columnspan = 2)
    diffCoeffEntryB1.insert(0, 0.8)

    diffCoeffTextB2 = tk.Label(window, text="Boundary 2")
    diffCoeffTextB2.grid(row=6, column = 6, columnspan = 2)

    diffCoeffEntryB2 = tk.Entry(window, width = 5)
    diffCoeffEntryB2.grid(row=7, column = 6, columnspan = 2)
    diffCoeffEntryB2.insert(0, 0)

    separator2 = ttk.Separator(window, orient='horizontal')
    separator2.grid(row=8, column = 0, columnspan = 8, sticky='ew', pady=5)

    timeEntryLabel = tk.Label(window, text="End time")
    timeEntryLabel.grid(row=9, column=1)

    timeEntry = tk.Entry(window, width = 5)
    timeEntry.grid(row=9, column = 2)
    timeEntry.insert(0, 100)

    toggleSourceBoolLabel = tk.Label(window, text="Continuous Sources")
    toggleSourceBoolLabel.grid(row=10, column = 1)

    toggleSourceBoolVar = tk.BooleanVar()
    toggleSourceBool = tk.Checkbutton(window, variable = toggleSourceBoolVar, offvalue = False)
    toggleSourceBool.grid(row=10, column=2)
    toggleSourceBool.select()

    animationBoolLabel = tk.Label(window, text="Animation")
    animationBoolLabel.grid(row=11, column=1)

    animationBoolVar = tk.BooleanVar()
    animationBool = tk.Checkbutton(window, variable = animationBoolVar, offvalue = False)
    animationBool.grid(row=11, column=2)
    animationBool.select()

    filenameBoolLabel = tk.Label(window, text='From File')
    filenameBoolLabel.grid(row=12, column=1)

    filenameBoolVar = tk.BooleanVar()
    filenameBool = tk.Checkbutton(window, variable = filenameBoolVar, offvalue = False)
    filenameBool.grid(row=12, column=2)
    filenameBool.select()

    filenameEntryLabel = tk.Label(window, text="Filename:")
    filenameEntryLabel.grid(row=13, column=1)

    filenameEntry = tk.Entry(window)
    filenameEntry.grid(row=13, column=2, columnspan = 3)
    filenameEntry.insert(0, 'ResearchInternship/sampleGrid2.txt')

    entries = [gridSizeEntryCol, gridSizeEntryRow, diffCoeffEntryS1, diffCoeffEntryS2, diffCoeffEntryB1, diffCoeffEntryB2, timeEntry, filenameEntry]
    boolEntries = [toggleSourceBoolVar, animationBoolVar, filenameBoolVar]

    continueButton = tk.Button(window, text="Continue", command =lambda:returnEntries(entries, boolEntries))
    continueButton.grid(row=14, column=3, columnspan=2, padx = 5, pady =5)

    tk.mainloop()

    return values