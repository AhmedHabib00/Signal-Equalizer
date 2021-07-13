import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import functools
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Menu, Button
from tkinter import LEFT, TOP, X, FLAT, RAISED
import tkinter as tk
from matplotlib import backend_bases
import scipy
import scipy.fftpack
import numpy as np
from tkinter.filedialog import askopenfilename
import threading
import csv
import math
from itertools import zip_longest
#------------------------------- SYNTHETIC ------------------------
'''
srate = 1000
time = np.arange(0,2,1/srate)
no_pnts = len(time)
x = 1.5*np.sin(2*math.pi*4000*time) + 2.5*np.sin(2*math.pi*6000*time) + 3.5*np.sin(2*math.pi*2000*time) + 5*np.sin(2*math.pi)

d = [time,x]
data = zip_longest(*d,fillvalue='')
with open('data.csv','w',encoding='ISO-8859-1',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(("Elapsed time","vals"))
    writer.writerows(data)
f.close()
'''
backend_bases.NavigationToolbar2.toolitems = (
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
        (None, None, None, None),
      )
window = Tk()
window.geometry('500x400')
window.resizable(0, 0)

#------------------------ LOADING THE DATA--------------------------

ECG = pd.read_csv('ECG.csv')
signals = [ECG]

#----------------------- LOAD DATA --------------------------------

window.title('signal viewer')
fig = plt.figure(figsize=(8.0, 5.0), linewidth=30.0)
ax = fig.add_subplot(111)
fig2 = plt.figure(figsize=(8.0, 5.0), linewidth=30.0)
ax3 = fig2.add_subplot(111)


x_min, x_max = ax.get_xlim()
y_min, y_max = ax.get_ylim()

frame = tk.Frame(master=window,highlightbackground="black", highlightcolor="black", highlightthickness=2)
frame.place(height =397, width =497, x = 0, y=0)
frame.config(background="white")


is_zoomed = False
def zoom(x):
    global is_zoomed
    is_zoomed = True
    if is_zoomed:
        ax.set_xlim(x_min * x, x_max / x)
        ax.set_ylim(y_min, y_max / x)
        ax3.set_xlim(x_min * x, x_max / x)
        ax3.set_ylim(y_min, y_max / x)
        fig2.canvas.draw()
    fig.canvas.draw()


c =0

colorlist = ['plasma', 'inferno', 'viridis', 'magma', 'cividis']
colorbar = StringVar()
colorbar.set(colorlist[0])  # set the default option
colorbar.get()


sliders = []
spectrosliders = []

spectro = plt.figure(figsize=(10, 2))
ax.set_facecolor('#efefef')
ax2 = spectro.add_subplot(111)
ax2.set_facecolor('#efefef')

def update(x):
    global c
    ax.cla()
    ax3.cla()
    ax2.cla()
    plot(c)
def spec(x):
    plt.clf()
    plt.specgram(x=x,NFFT=1024,noverlap=400,Fs=10,cmap=colorbar.get())
    plt.tight_layout()
    print('aloo')
    ax2.set_ylim(0,spectrosliders[0].get())
    ax2.set_xlim(0,spectrosliders[1].get())
    plt.draw()
    spectro.canvas.draw()



def plot(x):
    global signals
    global c
    c=x
    ax.cla()
    ax3.cla()
    temp = np.array(signals[x]['vals'])
    fourier_list = scipy.fftpack.fft(temp)
    fourier_phase = fourier_list.imag
    freqs = np.linspace(0,10000,len(signals[x]['Elapsed time']))
    for idx in range(len(freqs)):
        if freqs[idx] > 0 and freqs[idx] < 1000:
            fourier_list[idx] = fourier_list[idx].real * sliders[0].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 1000 and freqs[idx] < 2000:
            fourier_list[idx] = fourier_list[idx].real * sliders[1].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 2000 and freqs[idx] < 3000:
            fourier_list[idx] = fourier_list[idx].real * sliders[2].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 3000 and freqs[idx] < 4000:
            fourier_list[idx] = fourier_list[idx].real * sliders[3].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 4000 and freqs[idx] < 5000:
            fourier_list[idx] = fourier_list[idx].real * sliders[4].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 5000 and freqs[idx] < 6000:
            fourier_list[idx] = fourier_list[idx].real * sliders[5].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 6000 and freqs[idx] < 7000:
            fourier_list[idx] = fourier_list[idx].real * sliders[6].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 7000 and freqs[idx] < 8000:
            fourier_list[idx] = fourier_list[idx].real * sliders[7].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 8000 and freqs[idx] < 9000:
            fourier_list[idx] = fourier_list[idx].real * sliders[8].get() + fourier_phase[idx] * 1j
        if freqs[idx] > 9000 and freqs[idx] < 10000:
            fourier_list[idx] = fourier_list[idx].real * sliders[9].get() + fourier_phase[idx] * 1j

    inv = scipy.fftpack.ifft(fourier_list)
    spec(inv)
    ax.plot(signals[x]['Elapsed time'], signals[x]['vals'])
    ax3.plot(signals[x]['Elapsed time'], inv.real)

    fig.canvas.draw()
    fig2.canvas.draw()


def newWindow(x):
    xref = 15
    yref = 15
    spectrosliderrefx = 160
    spectrosliderrefy = 15
    new_window = Toplevel(window)
    new_window.geometry("1800x950")
    frmnewind = tk.Frame(master=new_window, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    frmnewind.place(height=550, width=1800, x=235, y=50)
    frmnewind.config(background="white")
    frmnewind2 = tk.Frame(master=new_window, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    frmnewind2.place(height=400, width=1800, x=235, y=505)
    frmnewind2.config(background="white")

    SliderHeader = tk.Text(frmnewind2)
    SliderHeader.place(height=30, width=100, x=180, y=5)
    SliderHeader.insert(tk.END, "Slider Bars")
    frameslider = tk.Frame(master=frmnewind2, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    frameslider.place(height=150, width=350, x=50, y=55)
    frameslider.config(background="white")

    framespectro = tk.Frame(master=frmnewind2, highlightbackground="black", highlightcolor="black",
                            highlightthickness=2)
    framespectro.place(height=150, width=300, x=950, y=230)
    framespectro.config(background="white")
    spectroHeader = tk.Text(frmnewind2)
    spectroHeader.place(height=30, width=200, x=1010, y=200)
    spectroHeader.insert(tk.END, "Spectrogram Settings")

    new_win_open_frame = tk.Frame(master=new_window, highlightbackground="black", highlightcolor="black",
                                  highlightthickness=2)
    new_win_open_frame.place(height=950, width=230, x=0, y=50)
    new_win_open_frame.config(background="white")

    Browsebutton = Button(new_win_open_frame, height=2, width=25, text='Open File', command=load_signal)
    Browsebutton.pack(side=TOP, padx=0, pady=(250, 12))

    new_toolbar_Frame = tk.Frame(master=new_window, highlightbackground="black", highlightcolor="black",
                                 highlightthickness=2)
    new_toolbar_Frame.place(height=40, width=1800, x=0, y=8)
    new_toolbar_Frame.config(bg="grey")

    zomin = ImageTk.PhotoImage(Image.open("zoom.png"))
    zoomit = Button(new_toolbar_Frame, command=functools.partial(zoom,2), image=zomin)
    zoomit.pack(side=LEFT, padx=8, pady=0)

    zomout = ImageTk.PhotoImage(Image.open("zoom_out.png"))
    zooooom = Button(new_toolbar_Frame, command=functools.partial(zoom,0.5), image=zomout)
    zooooom.pack(side=LEFT, padx=8, pady=0)

    for idx in range(10):
        sliders.append(Scale(master=frameslider, from_=1, to=5, orient=VERTICAL, command=update))
        # sliders[idx].set(1)
        sliders[idx].place(x=xref, y=yref)
        xref += 30

    for idx in range(2):
        spectrosliders.append(Scale(framespectro, from_=1, to=5, orient=VERTICAL, command=update))
        # spectrosliders[idx].set(1)
        spectrosliders[idx].place(x=spectrosliderrefx, y=spectrosliderrefy)
        spectrosliderrefx += 80

    canvas = FigureCanvasTkAgg(fig, frmnewind)
    canvas.get_tk_widget().place(height=450, width=800, x=0, y=5)

    fighead = tk.Text(frmnewind)
    fighead.place(height=20, width=100, x=360, y=20)
    fighead.insert(tk.END, "Old Signal")

    canvas2 = FigureCanvasTkAgg(fig2, frmnewind)
    canvas2.get_tk_widget().place(height=450, width=800, x=770, y=5)

    colordrop = OptionMenu(framespectro, colorbar, *colorlist, command=update)
    Label(framespectro, text="Choose a color").place(x=10, y=25)
    colordrop.place(x=20, y=60)

    figuphead = tk.Text(frmnewind)
    figuphead.place(height=20, width=100, x=1125, y=20)
    figuphead.insert(tk.END, "New Signal")

    canvas3 = FigureCanvasTkAgg(spectro, frmnewind2)
    canvas3.get_tk_widget().place(x=510, y=5)



def ecg_button():
    newWindow(0)
    ax.cla()
    plot(0)

t1 = threading.Thread(target=functools.partial(newWindow,2))
t2 = threading.Thread(target=functools.partial(newWindow,3))
"""
def emg_button():
    t1.start()
    ax.cla()
    plot(1)
def voice_button():
    t2.start()
    ax.cla()
    plot(2)

"""
def load_signal():
    global signals
    filename = askopenfilename()
    df = pd.read_csv(filename)
    signals.append(df)
    print(len(signals))
    print(type(signals[len(signals)-1]))
    print('aloo ',type(signals[0]))
    #t = threading.Thread(target=functools.partial(newWindow,len(signals)-1))
    #t.start()
    newWindow(len(signals)-1)
    plot(len(signals)-1)

ecgplot = Button(frame, height=2, width=25, text='ECG', command=ecg_button)
ecgplot.pack(side=TOP, padx = 0, pady= (12))

"""emgplot = Button(frame, height=2, width=25, text='EMG', command=emg_button)
emgplot.pack(side=TOP, padx = 0, pady= 12)
voiceplot = Button(frame, height=2, width=25, text='Voice', command=voice_button)
voiceplot.pack(side=TOP, padx = 0, pady= 12)


"""

window.mainloop()