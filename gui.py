# from tkinter import *
import tkinter as tk
from mainProgram import mainProg

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
# root.geometry("900x500")
root.attributes('-fullscreen', True)

def barChartVertikal(keyName, valueName, keyData, valueData, explanation):
    Data = {keyName: keyData,
    valueName: valueData
    }

    df = DataFrame(Data, columns= [keyName, valueName])
    df = df[[keyName, valueName]].groupby(keyName).sum()

    figure = plt.Figure(figsize=(3,4), dpi=65)
    ax = figure.add_subplot(111)
    bar = FigureCanvasTkAgg(figure, root)
    bar.get_tk_widget().pack(side=tk.LEFT, ipady=150, ipadx=100)
    df.plot(kind='bar', legend=True, ax=ax, fontsize=10)
    ax.set_title(explanation)

def barChartHorizontal(keyName, valueName, keyData, valueData, explanation):
    Data = {keyName: keyData,
    valueName: valueData
    }

    df = DataFrame(Data, columns= [keyName, valueName])
    df = df[[keyName, valueName]].groupby(keyName).sum()

    figure = plt.Figure(figsize=(3,4), dpi=70)
    ax = figure.add_subplot(111)
    bar = FigureCanvasTkAgg(figure, root)
    bar.get_tk_widget().pack(ipadx=3000, pady=10, padx=30)
    df.plot(kind='barh', legend=True, ax=ax, fontsize=10)
    ax.set_title(explanation)

def lineChart(keyName, valueName, keyData, valueData, explanation):
    Data = {keyName: keyData,
    valueName: valueData
    }

    df = DataFrame(Data, columns= [keyName, valueName])
    df = df[[keyName, valueName]].groupby(keyName).sum()

    figure = plt.Figure(figsize=(3,4), dpi=80)
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side=tk.LEFT, ipadx=200, padx=30)
    df.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
    ax.set_title(explanation)

def igScraping(nama):
    if type(mainProg(nama, 10, 5)) != str:
        arrKeyComAcc, arrQtyComAcc, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, curAcc = mainProg(nama, 10, 5)
        barChartHorizontal('Username', 'Comments', arrKeyComAcc, arrQtyComAcc, 'account that comment the most')
        lineChart('oldest post --> latest post', 'Likes', arrKeyGetPostLike, arrQtyGetPostLike, 'Number of Likes per Post')        
        lineChart('oldest post --> latest post', 'Comments', arrKeyGetPostComment, arrQtyGetPostComment, 'Number of Comments per Post')
    else:
        tk.messagebox.showerror("Error", mainProg(nama, 10, 5))

def getInputan():
    inputan = entry_1.get()
    if inputan != '':
        igScraping(inputan)
    else:
        tk.messagebox.showerror("Error", 'text field cannot be empty')

label_1 = tk.Label(root, text="Input Username")
entry_1 = tk.Entry(root)
button_1 = tk.Button(root, text='start analyzing', command=getInputan, bg="green", fg="white")

label_1.pack(pady=10)

entry_1.pack(pady=5)
button_1.pack()

root.mainloop()