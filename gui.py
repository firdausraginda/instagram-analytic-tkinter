# from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from getJSON import mainProgramGetJSON, getVeryPositiveComments, automateIgScraper, format1, format2, format3

root = tk.Tk()
root.geometry("900x500")
#root.attributes('-fullscreen', True)

def mainProg(account, qtyPost, qtyAcc):
    global valProgBar

    accOwner = automateIgScraper(account, qtyPost)
    valProgBar += 40
    progBar.after(500, progress(valProgBar))
    progBar.update()

    statusParam, hasilScrapingComAcc, hasilGetPost, hasilSortLike, hasilSortComment, curAcc = mainProgramGetJSON(accOwner, qtyAcc)
    valProgBar += 30
    progBar.after(500, progress(valProgBar))
    progBar.update()

    if statusParam == 'done':
        arrKeyComAcc, arrQtyComAcc = format1(hasilScrapingComAcc)
        valProgBar += 5
        progBar.after(500, progress(valProgBar))
        progBar.update()

        arrKeyGetPostLike, arrQtyGetPostLike = format2(hasilGetPost, 'like')
        valProgBar += 5
        progBar.after(500, progress(valProgBar))
        progBar.update()

        arrKeyGetPostComment, arrQtyGetPostComment = format2(hasilGetPost, 'comment')
        valProgBar += 5
        progBar.after(500, progress(valProgBar))
        progBar.update()

        return statusParam, arrKeyComAcc, arrQtyComAcc, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, hasilSortLike, hasilSortComment, curAcc
    else:
        valProgBar += 25
        progBar.after(500, progress(valProgBar))
        progBar.update()
        arrKeyComAcc = arrQtyComAcc = arrKeyGetPostLike = arrQtyGetPostLike = arrKeyGetPostComment = arrQtyGetPostComment = None
        return statusParam, arrKeyComAcc, arrQtyComAcc, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, hasilSortLike, hasilSortComment, curAcc

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

    figure = plt.Figure(figsize=(3,4), dpi=90)
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side=tk.LEFT, ipadx=100)
    df.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
    ax.set_title(explanation)

def listBox(data1, data2):
    # scrollbar = tk.Scrollbar(root)
    # scrollbar.pack( side = tk.RIGHT, fill = tk.Y )

    mylist = tk.Listbox(root, font=1)
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
    global valProgBar

    statusParam, arrKeyComAcc, arrQtyComAcc, arrKeyGetPostLike, arrQtyGetPostLike, arrKeyGetPostComment, arrQtyGetPostComment, hasilSortLike, hasilSortComment, curAcc = mainProg(nama, 15, 5)
    valProgBar += 5
    progBar.after(500, progress(valProgBar))
    progBar.update()

    if statusParam == 'done':
        if len(arrKeyComAcc) != 0: 
            barChartHorizontal('Username', 'Comments', arrKeyComAcc, arrQtyComAcc, 'account that comment the most')
            valProgBar += 2
            progBar.after(500, progress(valProgBar))
            progBar.update()

        if len(arrKeyGetPostLike) != 0: 
            lineChart('oldest post --> latest post', 'Likes', arrKeyGetPostLike, arrQtyGetPostLike, 'Number of Likes')        
            valProgBar += 1
            progBar.after(500, progress(valProgBar))
            progBar.update()

        if len(arrKeyGetPostComment) != 0: 
            lineChart('oldest post --> latest post', 'Comments', arrKeyGetPostComment, arrQtyGetPostComment, 'Number of Comments')
            valProgBar += 1
            progBar.after(500, progress(valProgBar))
            progBar.update()

        if len(hasilSortLike) != 0 and len(hasilSortComment) != 0:
            listBox(hasilSortLike, hasilSortComment)
            valProgBar += 1
            progBar.after(500, progress(valProgBar))
            progBar.update()
    else:
        messagebox.showerror("Error", statusParam)

def getInputan():
    global valProgBar

    inputan = entry_1.get()
    if inputan != '':
        label_1.pack_forget()
        entry_1.pack_forget()
        button_1.pack_forget()
        
        valProgBar += 5
        progBar.after(500, progress(valProgBar))
        progBar.update()

        igScraping(inputan)
    else:
        messagebox.showerror("Error", 'please input username')

def progress(currentValue):
    progBar["value"]=currentValue

def closeWindow():
    root.destroy()

# -------------- main program --------------
label_1 = tk.Label(root, text="Input Username")
entry_1 = tk.Entry(root)
button_1 = tk.Button(root, text='start analyzing', command=getInputan, bg="green", fg="white")
button_close = tk.Button(root, text='exit', command=closeWindow, bg='red', fg="white")

button_close.pack()
label_1.pack(pady=10)
entry_1.pack(pady=5)
button_1.pack()

progBar = ttk.Progressbar(root,orient ="horizontal",length = 200, mode ="determinate")
progBar.pack(pady=10)

valProgBar = 0
progBar["maximum"] = 100
progBar["value"] = valProgBar

root.mainloop()