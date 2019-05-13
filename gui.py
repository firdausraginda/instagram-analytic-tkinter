# from tkinter import *
import tkinter as tk
from mainProgram import mainProg

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.geometry("900x500")
# root.attributes('-fullscreen', True)

def barChart(keyName, valueName, keyData, valueData, explanation, colom2):
    Data = {keyName: keyData,
    valueName: valueData
    }

    df = DataFrame(Data, columns= [keyName, valueName])
    df = df[[keyName, valueName]].groupby(keyName).sum()

    figure = plt.Figure(figsize=(3,4), dpi=70)
    ax = figure.add_subplot(111)
    bar = FigureCanvasTkAgg(figure, root)
    if colom2 == True:
        bar.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, pady=10)
    else:
        bar.get_tk_widget().pack(fill=tk.BOTH, pady=10)
    df.plot(kind='barh', legend=True, ax=ax, fontsize=10)
    ax.set_title(explanation)

def lineChart(keyName, valueName, keyData, valueData, explanation):
    Data = {keyName: keyData,
    valueName: valueData
    }

    df = DataFrame(Data, columns= [keyName, valueName])
    df = df[[keyName, valueName]].groupby(keyName).sum()

    figure = plt.Figure(figsize=(5,4), dpi=70)
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    df.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
    ax.set_title(explanation)

def igScraping(nama):
    if type(mainProg(nama, 10, 5)) != str:
        arrKeyComAcc, arrQtyComAcc, arrKeyMenByUser, arrQtyMenByUser, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, curAcc = mainProg(nama, 10, 5)
        barChart('Username', 'Comments', arrKeyComAcc, arrQtyComAcc, 'account that comment the most', False)
        barChart('Username', 'Mentioned', arrKeyMenByUser, arrQtyMenByUser, 'account that mentioned by %s the most' % (curAcc), False)
        barChart('Post Time', 'Likes', arrKeyGetPostLike, arrQtyGetPostLike, 'Number of Likes per Post', False)
        barChart('Post Time', 'Comments', arrKeyGetPostComment, arrQtyGetPostComment, 'Number of Comments per Post', False)
    else:
        labelNama["text"] = mainProg(nama, 10, 5)

def getInputan():
    inputan = entry_1.get()
    if inputan != '':
        igScraping(inputan)
    else:
        labelNama["text"] = 'inputan kosong'

label_1 = tk.Label(root, text="Input Username")
entry_1 = tk.Entry(root)
button_1 = tk.Button(root, text='analyzed', command=getInputan, bg="green", fg="white")
labelNama = tk.Label(root)

label_1.pack(pady=10)
entry_1.pack(pady=3)
button_1.pack(pady=3)
labelNama.pack(pady=3)

root.mainloop()