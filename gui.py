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

    figure = plt.Figure(figsize=(5,4), dpi=70)
    ax = figure.add_subplot(111)
    bar = FigureCanvasTkAgg(figure, root)
    bar.get_tk_widget().pack(ipadx=450, pady=10, padx=30)
    df.plot(kind='barh', legend=True, ax=ax, fontsize=12)
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
    line.get_tk_widget().pack(side=tk.LEFT, ipadx=120)
    df.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
    ax.set_title(explanation)

def listBox(data1, data2):
    # scrollbar = tk.Scrollbar(root)
    # scrollbar.pack( side = tk.RIGHT, fill = tk.Y )

    mylist = tk.Listbox(root)
    for i in range(len(data1)):
        if i == 0:
            mylist.insert(tk.END, "TOP %s POSTS based on LIKES" % (len(data1)))
            mylist.insert(tk.END, "--------------------------------------")
        mylist.insert(tk.END, "POST #%s" % (i+1))
        mylist.insert(tk.END, "caption: " + data1[i]['caption'])
        mylist.insert(tk.END, "tags: " + data1[i]['tags'])
        mylist.insert(tk.END, "post time: " + data1[i]['time'])
        mylist.insert(tk.END, "likes: " + str(data1[i]['count like']))
        mylist.insert(tk.END, "")

        if i+1 == len(data1):
            mylist.insert(tk.END, "================================================================")
            mylist.insert(tk.END, "")
  
    for i in range(len(data2)):
        if i == 0:
            mylist.insert(tk.END, "TOP %s POSTS based on COMMENTS" % (len(data2)))
            mylist.insert(tk.END, "--------------------------------------")
        mylist.insert(tk.END, "POST #%s" % (i+1))
        mylist.insert(tk.END, "caption: " + data2[i]['caption'])
        mylist.insert(tk.END, "tags: " + data2[i]['tags'])
        mylist.insert(tk.END, "post time: " + data2[i]['time'])
        mylist.insert(tk.END, "comments: " + str(data2[i]['count comment']))
        mylist.insert(tk.END, "")

    mylist.pack(side=tk.RIGHT, fill=tk.BOTH, ipadx=600)
    # scrollbar.config( command = mylist.yview )

def igScraping(nama):
    if type(mainProg(nama, 15, 5)) != str:
        arrKeyComAcc, arrQtyComAcc, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, hasilSortLike, hasilSortComment, curAcc = mainProg(nama, 15, 5)

        barChartHorizontal('Username', 'Comments', arrKeyComAcc, arrQtyComAcc, 'account that comment the most')
        lineChart('oldest post --> latest post', 'Likes', arrKeyGetPostLike, arrQtyGetPostLike, 'Number of Likes')        
        lineChart('oldest post --> latest post', 'Comments', arrKeyGetPostComment, arrQtyGetPostComment, 'Number of Comments')

        listBox(hasilSortLike, hasilSortComment)
    else:
        tk.messagebox.showerror("Error", mainProg(nama, 15, 5))

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