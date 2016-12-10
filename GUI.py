import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from tkinter import *
import tkinter as tk
from StockPrediction.stock import Stock
import sys
import os
import urllib.request
import random
import itertools


LARGE_FONT = ("Verdana", 20)

class Page(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # frame = F(container, self)
            # self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, classname):
        '''Returns an instance of a page given it's class name as a string'''
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None


#First Home page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="STOCK V.1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="START",
                           command=lambda: controller.show_frame("PageOne"))
        button.pack()
        # Close Button
        close_button = Button(self, text="Close", command=self.quit)
        close_button.pack()

#Calculation Page
class PageOne(tk.Frame):
    Google = Stock()
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.grid()
        label = tk.Label(self, text="CALCULATION", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # Second Page Button
        pageTwo_button = tk.Button(self, text='Graph', command=lambda: controller.show_frame("PageTwo"))
        pageTwo_button.place(x=250, y=260)

        # Back to Start button
        button_back = tk.Button(self, text="Back to Start",
                            command=lambda: controller.show_frame("StartPage"))
        button_back.place(x=350, y=260)

        # Restart Button
        restart_button = tk.Button(self, text='Restart', command=restart)
        restart_button.place(x=500, y=260)

        # Label Ticker Symbol Input from user
        self.user_input_tickerSymbol = tk.Label(self, text="Enter Ticker Symbol: ")
        self.user_input_tickerSymbol.place(x=40, y=90)

        # Ticker Symbol Input from user
        self.tickerSymbol = StringVar(self)
        self.entry_tickerSymbol = tk.Entry(self, textvariable=self.tickerSymbol)
        self.entry_tickerSymbol.place(x=180, y=90, width=100)

        self.selectionButtons()

        # calculate button
        # self.button_calculate = tk.Button(self, text="Calculate", command=combine_funcs(self.average, self.get_TickerSymbol))
        self.button_calculate = tk.Button(self, text="Calculate", command=combine_funcs(self.averageTesting, self.displayUpdate))
        self.button_calculate.pack()
        self.button_calculate.place(x=120, y=260)

    def show_entry_TickerSymbol(self):
        print(self.tickerSymbol.get())
        self.entry_tickerSymbol.delete(0, END)

    # selection buttons
    def selectionButtons(self):
        # Selection calculation list
        selectionButton = tk.Label(self, text="What would you like to calculate?")
        selectionButton.place(x=450, y=80)
        # average open check box
        self.average_open = IntVar()
        Checkbutton(self, text="Average Open", variable=self.average_open).place(x=450, y=100)
        # average high check box
        self.average_high = IntVar()
        Checkbutton(self, text="Average High", variable=self.average_high).place(x=450, y=125)
        # average low check box
        self.average_low = IntVar()
        Checkbutton(self, text="Average Low", variable=self.average_low).place(x=450, y=150)
        # average close check box
        self.average_close = IntVar()
        Checkbutton(self, text="Average Close", variable=self.average_close).place(x=450, y=175)
        # average volume check box
        self.average_volume = IntVar()
        Checkbutton(self, text="Average Volume", variable=self.average_volume).place(x=450, y=200)

        # self.button_list = ["Average Open", "Average High", "Average Low"]
        # c = 0
        # self.averageBoxes = []
        # for button in self.button_list:
        #     self.v = IntVar()
        #     self.averageBoxes.append(self.v)
        #     average_Button = Checkbutton(self, text=button, variable=self.v).place(x=450, y=125 + c)
        #     c += 25

    def refresh_hit(self):
        self.average_open.set(0)
        self.average_low.set(0)
        self.average_high.set(0)
        self.entry_tickerSymbol.delete(0, 'end')

    # get ticker symbol function
    def get_TickerSymbol(self):
        # first Instance of Stock Class
        self.Google.user_input(self.tickerSymbol.get())
        print("Ticker Symbol Entered: " + self.tickerSymbol.get())


    # Execute TicketSymbol and Average Calculation
    def averageTesting(self):
        self.get_TickerSymbol()
        self.average()

    def displayUpdate(self):
        # label for user entered Ticker Symbol
        # user_ticker_symbol = StringVar()
        # new_label = tk.Label(self, textvariable=user_ticker_symbol)
        # new_label.place(x=425, y=380, anchor="center")
        #user_ticker_symbol.config("Ticker Symbol: " + self.tickerSymbol.get())

        v = StringVar()
        tickerLabel = Label(self, textvariable=v)
        tickerLabel.place(x=500, y=380, anchor="center")
        label1 = Label(self, text="Ticker Symbol Entered: ")
        label1.place(x=380, y=380, anchor="center")
        v.set(self.tickerSymbol.get())

    # Calculating the average(s)
    def average(self):
        # label for Results
        resultMsg = tk.Label(self, text="RESULTS", font=LARGE_FONT)
        resultMsg.place(x=425, y=350, anchor="center")

        #self.display_ticketSymbolResults()

        open = self.Google.average_open()
        high = self.Google.average_high()
        low = self.Google.average_low()
        close = self.Google.average_close()
        volume = self.Google.average_volume()

        if self.average_open.get() and self.average_low.get() and self.average_high.get() and self.average_close.get() \
                and self.average_volume.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Low Average:' {2} \n 'Close Average:' {3} \n " \
                       "'Volume Average: {4}".format(round(open, 5), round(high,5), round(low,5), round(close,5), round(volume,5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get() and self.average_high and self.average_close.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Low Average:' {2} \n " \
                       "'Close Average:' {3} \n ".format(round(open, 5), round(high, 5), round(low, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get() and self.average_high and self.average_volume.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Low Average:' {2} \n " \
                       "'Volume Average:' {3} \n ".format(round(open, 5), round(high, 5), round(low, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_close.get() and self.average_low.get() and self.average_high and self.average_volume.get():
            joinText = "'High Average:' {0} \n 'Low Average:' {1} \n 'Close Average:' {2} \n " \
                       "'Volume Average:' {3} \n ".format(round(high, 5), round(low, 5), round(close, 5),
                                                          round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get() and self.average_high.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Low Average:' " \
                       "{2} \n ".format(round(open, 5), round(high, 5), round(low, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_high.get() and self.average_close.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Close Average:' " \
                       "{2} \n ".format(round(open, 5), round(high, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_high.get() and self.average_volume.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Volume Average:' " \
                       "{2} \n ".format(round(open, 5), round(high, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get() and self.average_volume.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n 'Volume Average:' " \
                       "{2} \n ".format(round(open, 5), round(low, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get() and self.average_close.get():
            joinText = "'Open Average:' {0} \n 'Low Average:' {1} \n 'Close Average:' " \
                       "{2} \n ".format(round(open, 5), round(low, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_close.get() and self.average_volume.get():
            joinText = "'Open Average:' {0} \n 'Close Average:' {1} \n 'Volume Average:' " \
                       "{2} \n ".format(round(open, 5), round(close, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get() and self.average_low.get() and self.average_close.get():
            joinText = "'High Average:' {0} \n 'Low Average:' {1} \n 'Close Average:' " \
                       "{2} \n ".format(round(high, 5), round(low, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get() and self.average_close.get() and self.average_volume.get():
            joinText = "'High Average:' {0} \n 'Close Average:' {1} \n 'Volume Average:' " \
                       "{2} \n ".format(round(high, 5), round(close, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_low.get() and self.average_close.get() and self.average_volume.get():
            joinText = "'Low Average:' {0} \n 'Close Average:' {1} \n 'Volume Average:' " \
                       "{2} \n ".format(round(low, 5), round(close, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get():
            open = self.Google.average_open()
            low = self.Google.average_low()
            joinText = "'Open Average:' {0} \n 'Low Average:' {1} \n ".format(round(open, 5), round(low, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_high.get():
            joinText = "'Open Average:' {0} \n 'High Average:' {1} \n ".format(round(open, 5), round(high, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_low.get():
            joinText = "'Open Average:' {0} \n 'Low Average:' {1} \n ".format(round(open, 5), round(low, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_close.get():
            joinText = "'Open Average:' {0} \n 'Close Average:' {1} \n ".format(round(open, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get() and self.average_volume.get():
            joinText = "'Open Average:' {0} \n 'Volume Average:' {1} \n ".format(round(open, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get() and self.average_low.get():
            joinText = "'High Average:' {0} \n 'Low Average:' {1} \n ".format(round(high, 5), round(low, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get() and self.average_close.get():
            joinText = "'High Average:' {0} \n 'Close Average:' {1} \n ".format(round(high, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get() and self.average_volume.get():
            joinText = "'High Average:' {0} \n 'Volume Average:' {1} \n ".format(round(high, 5), round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_low.get() and self.average_close.get():
            joinText = "'Low Average:' {0} \n 'Close Average:' {1} \n ".format(round(low, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_low.get() and self.average_high.get():
            joinText = "'Low Average:' {0} \n 'High Average:' {1} \n ".format(round(low, 5), round(high, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get() and self.average_close.get():
            joinText = "'High Average:' {0} \n 'Close Average:' {1} \n ".format(round(high, 5), round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_open.get():
            joinText = "'Open Average:' {0} \n".format(round(open, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_low.get():
            joinText = "'Low Average:' {0} \n".format(round(low, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_close.get():
            joinText = "'Close Average:' {0} \n".format(round(close, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_high.get():
            joinText = "'High Average:' {0} \n".format(round(high, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        elif self.average_volume.get():
            joinText = "'Volume Average:' {0} \n".format(round(volume, 5))
            msg = Label(self, text=joinText)
            self.place_Average(msg)
        else:
            msg = Label(self, text="No Results")
            self.place_Average(msg)

    def answer_box(self, query):
        return query

    def place_Average(self, msg):
        msg.place(x=400, y=450, anchor="center")

#Display Page
class PageTwo(PageOne):
    Apple = Stock()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="GRAPH", font=LARGE_FONT)
        label.pack(side="top", fill="x", pady=10)

        button_back = tk.Button(self, text="Start Page",
                            command=combine_funcs(lambda: controller.show_frame("StartPage"), self.clear_Canvas))
        button_back.place(x=50, y =50)

        # self.button_calculate = tk.Button(self, text="Calculate", command=combine_funcs(self.average, self.get_TickerSymbol))

        # button_pageOne = tk.Button(self, text="Go Back")
        # button_pageOne.place(x=150, y =50)

        self.button2 = tk.Button(self, text='Print Graph', command=self.print_it)
        self.button2.place(x=250, y=50)

        self.f = Figure(figsize=(6, 6), dpi=110)
        self.p = self.f.gca()

        self.selectionButtons()

    def print_it(self):
        page_one = self.controller.get_page("PageOne")
        open = page_one.average_open.get()
        high = page_one.average_high.get() + 2
        low = page_one.average_low.get() + 4
        close = page_one.average_close.get() + 6
        volume = page_one.average_volume.get() + 8

        page_one = self.controller.get_page("PageOne")
        ticker_symbol = page_one.entry_tickerSymbol.get()

        #Clearing Buttons/Selection
        self.clear_Buttons()

        print("page two:", ticker_symbol, type(ticker_symbol))

        self.Apple.validate_file(ticker_symbol)

        choices = {open: self.createOpen, high: self.createHigh, low: self.createLow, close: self.createClose, volume: self.createVolume}
        print(open, high, low, close, volume)
        print("keys:", choices.keys())
        if {1,3,5,7,9}.issubset(choices):
            self.createHigh()
            self.createOpen()
            self.createLow()
            self.createClose()
            self.createVolume()
            self.createCanvas(self.f)
        elif {0,3,5,7,9}.issubset(choices):
            self.createHigh()
            self.createLow()
            self.createClose()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 5, 7, 9}.issubset(choices):
            self.createOpen()
            self.createLow()
            self.createClose()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 3, 7, 9}.issubset(choices):
            self.createOpen()
            self.createHigh()
            self.createClose()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 3, 5, 9}.issubset(choices):
            self.createOpen()
            self.createHigh()
            self.createLow()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 3, 5, 7}.issubset(choices):
            self.createOpen()
            self.createHigh()
            self.createLow()
            self.createClose()
            self.createCanvas(self.f)
        elif {5, 7, 9}.issubset(choices):
            self.createVolume()
            self.createLow()
            self.createClose()
            self.createCanvas(self.f)
        elif {3, 7, 9}.issubset(choices):
            self.createHigh()
            self.createVolume()
            self.createClose()
            self.createCanvas(self.f)
        elif {3, 5, 9}.issubset(choices):
            self.createVolume()
            self.createLow()
            self.createHigh()
            self.createCanvas(self.f)
        elif {3, 5, 7}.issubset(choices):
            self.createHigh()
            self.createLow()
            self.createClose()
            self.createCanvas(self.f)
        elif {3, 7, 9}.issubset(choices):
            self.createHigh()
            self.createVolume()
            self.createClose()
            self.createCanvas(self.f)
        elif {1, 7, 9}.issubset(choices):
            self.createOpen()
            self.createClose()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 5, 9}.issubset(choices):
            self.createOpen()
            self.createLow()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 5, 7}.issubset(choices):
            self.createOpen()
            self.createLow()
            self.createClose()
            self.createCanvas(self.f)
        elif {1, 3, 9}.issubset(choices):
            self.createHigh()
            self.createOpen()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 3, 7}.issubset(choices):
            self.createOpen()
            self.createHigh()
            self.createClose()
            self.createCanvas(self.f)
        elif {1, 5, 3}.issubset(choices):
            self.createOpen()
            self.createLow()
            self.createHigh()
            self.createCanvas(self.f)
        elif {7,9}.issubset(choices):
            self.createClose()
            self.createHigh()
            self.createCanvas(self.f)
        elif {5, 9}.issubset(choices):
            self.createVolume()
            self.createLow()
            self.createCanvas(self.f)
        elif {5, 7}.issubset(choices):
            self.createClose()
            self.createLow()
            self.createCanvas(self.f)
        elif {3, 9}.issubset(choices):
            self.createVolume()
            self.createHigh()
            self.createCanvas(self.f)
        elif {3, 7}.issubset(choices):
            self.createClose()
            self.createHigh()
            self.createCanvas(self.f)
        elif {3, 5}.issubset(choices):
            self.createClose()
            self.createLow()
            self.createCanvas(self.f)
        elif {1, 9}.issubset(choices):
            self.createOpen()
            self.createVolume()
            self.createCanvas(self.f)
        elif {1, 7}.issubset(choices):
            self.createOpen()
            self.createClose()
            self.createCanvas(self.f)
        elif {1, 5}.issubset(choices):
            self.createOpen()
            self.createLow()
            self.createCanvas(self.f)
        elif {1, 3}.issubset(choices):
            self.createOpen()
            self.createHigh()
            self.createCanvas(self.f)
        elif {9}.issubset(choices):
            self.createVolume()
            self.createCanvas(self.f)
        elif {7}.issubset(choices):
            self.createClose()
            self.createCanvas(self.f)
        elif {5}.issubset(choices):
            self.createLow()
            self.createCanvas(self.f)
        elif {3}.issubset(choices):
            self.createHigh()
            self.createCanvas(self.f)
        elif {1}.issubset(choices):
            self.createOpen()
            self.createCanvas(self.f)


    def createHigh(self):
        # create High histogram
        histoHigh = self.Apple.pageTwo_High(self.days.get())
        lengthHigh = self.Apple.pageTwo_lengthHigh(self.days.get())
        meanHistoHigh = np.mean(histoHigh)
        self.createHistogram(histoHigh, lengthHigh, meanHistoHigh, 'High')

    def createOpen(self):
        # create Open histogram
        histoOpen = self.Apple.pageTwo_Open(self.days.get())
        lengthOpen = self.Apple.pageTwo_lengthOpen(self.days.get())
        meanHistoOpen = np.mean(histoOpen)
        self.createHistogram(histoOpen, lengthOpen, meanHistoOpen, 'Open')

    def createLow(self):
        # create Low histogram
        histoLow = self.Apple.pageTwo_Low(self.days.get())
        lengthLow = self.Apple.pageTwo_lengthLow(self.days.get())
        meanHistoLow = np.mean(histoLow)
        self.createHistogram(histoLow, lengthLow, meanHistoLow, 'Low')

    def createClose(self):
        # create Close histogram
        histoClose = self.Apple.pageTwo_Close(self.days.get())
        lengthClose = self.Apple.pageTwo_lengthClose(self.days.get())
        meanHistoClose = np.mean(histoClose)
        self.createHistogram(histoClose, lengthClose, meanHistoClose, 'Close')

    def createVolume(self):
        # create Volume histogram
        histoVolume = self.Apple.pageTwo_Volume(self.days.get())
        lengthVolume = self.Apple.pageTwo_lengthVolume(self.days.get())
        meanHistoVolume = np.mean(histoVolume)
        self.createHistogram(histoVolume, lengthVolume, meanHistoVolume, 'Volume')

    def createHistogram(self, histoList, lengthList, meanHistoList, histoLabel):
        colorHistoList = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'teal', 'orange', 'maroon', 'coral', 'cyan',
                     'orchid', 'lightpink', 'steelblue', 'midnightblue', 'gold', 'darkred', 'saddlebrown', 'black', 'dimgrey', 'peru']
        averageColorList = ['gold', 'darkred', 'saddlebrown', 'black', 'dimgrey', 'peru', 'aliceblue', 'yellowgreen',
                            'skyblue', 'darkblue', 'indigo']

        self.p.hist(histoList, lengthList, color=random.choice(colorHistoList), alpha=1.0, histtype='stepfilled', label=histoLabel)
        self.p.axvline(meanHistoList, color=random.choice(averageColorList), linewidth=2)
        self.p.set_xlabel('Daily Open', fontsize=15)
        self.p.set_ylabel('Frequency', fontsize=15)
        self.p.legend(loc='upper right')

    def createCanvas(self, f):
        self.canvas = FigureCanvasTkAgg(f)
        self.canvas.get_tk_widget().place(x=100, y=120)
        self.canvas.show()
        self.toolbar = NavigationToolbar2TkAgg(self.canvas)
        self.toolbar.update()
        self.canvas._tkcanvas.place(x=100, y=140)

    def clear_Canvas(self):
        self.canvas.get_tk_widget().place_forget()

    # selection buttons
    def selectionButtons(self):
        # Selection calculation list
        self.days = IntVar()
        self.selectionButton = tk.Label(self, text="How many days would you like to graph?")
        self.selectionButton.place(x=400, y=50)
        self.button30 = Radiobutton(self, text="30 Days", variable=self.days, value=30, command=self.selectedValue)
        self.button30.place(x=450, y=75)
        self.button60 = Radiobutton(self, text="60 Days", variable=self.days, value=60, command=self.selectedValue)
        self.button60.place(x=450, y=100)
        self.button90 = Radiobutton(self, text="90 Days", variable=self.days, value=90, command=self.selectedValue)
        self.button90.place(x=450, y=125)

    def clear_Buttons(self):
        self.selectionButton.place_forget()
        self.button30.place_forget()
        self.button60.place_forget()
        self.button90.place_forget()

    def selectedValue(self):
        self.daysVariable = int(self.days.get())
        print("You selected the option ", self.daysVariable)



        # Extra method(s)
# Function to Combine methods
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

# Function to Restart the entire program
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


if __name__ == "__main__":
    root = Page()
    root.geometry('850x850')
    root.title("STOCK V.1")
    root.mainloop()
