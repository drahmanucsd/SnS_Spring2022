from cProfile import label
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.ttk import Progressbar
from tkinter.ttk import Scrollbar
import os
import ntpath
import pandas as pd

# returns function that calcualtes cost based on tier
def tier_costs(tier,e1,e2,e3,e4,e5):
    if (tier == 1):
        return tier1_cost(e1,25,e2,e3)
    elif (tier == 2):
        return tier2_cost(e1,e2,e5,23,e3,e4)
    else:
        return tier3_cost

# returns cost of a practitioner or concierge
def worker_cost(cost, travel_dist, travel_rate):
    return cost + travel_dist*travel_rate

# returns cost for tier 1 events
def tier1_cost(prac_cost=65, conc_cost=25, travel_dist=0, travel_rate=0.585):
    travel_rate = 0.585
    prac_cost = worker_cost(prac_cost, travel_dist, travel_rate) 
    conc_cost =  worker_cost(conc_cost, travel_dist, travel_rate)
    
    return prac_cost + conc_cost 

# returns cost for tier 2 events
def tier2_cost(kit, num_participants, prac_cost, conc_cost, travel_dist, travel_rate):
    kits = kits_cost(kit, num_participants)
    prac_cost = worker_cost(prac_cost, travel_dist, travel_rate)
    conc_cost = worker_cost(conc_cost, travel_dist, travel_rate)

    return kits + prac_cost + conc_cost

# returns total cost of all kits given type of kit and num people
def kits_cost(kit, num_participants):
    """
    kits are encoded as numbers in the same order as on the corporate pricing 
    breakdown sheet.
    """
    kit_prices = {
        0 : 30,
        1 : 42,
        2 : 31, 
        3 : 40,
        4 : 38,
        5 : 57,
        6 : 70
    }

    return kit_prices[kit] * num_participants

# returns cost for tier 3 events: 2 practitioners, 1 concierge, med consumables
def tier3_cost(consum_lst, num_participants, prac_cost1=65, prac_cost2=65, conc_cost=25, travel_dist=0, travel_rate=0.585):
    """
    consum_lst: number of medical consumables of each type
    """
    prac1 = worker_cost(prac_cost1, travel_dist, travel_rate) 
    prac2 = worker_cost(prac_cost2, travel_dist, travel_rate) 
    conc = worker_cost(prac_cost2, travel_dist, travel_rate) 

    return prac1 + prac2 + med_consum(consum_lst)

# returns total cost of medical consumables
def med_consum(consum_lst):
    """
    both arrays must have the consumables listed in the same order
    """
    consum_array = np.array(consum_lst)
    consum_costs = np.array([5, 6, 12, 25, 1, 2, 3.5])

    return consum_array * consum_costs




#  GUI


window = tk.Tk()
root = window

window.title("Pricing Model")
window.geometry('400x600')
window.config(bg='#ffffff')

# declaring string variable
# for storing name and password
var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
tier_var = tk.StringVar()




frame1 = tk.Frame(master=window, width=400, height=100, bg="#3b84f8")
frame1.pack()
frame2 = tk.Frame(master=window, width=400, height=600, bg="white")
frame2.pack()
# defining a function that will
# get the name and password and
# print them on the screen
def submit():
    outlabel.config(text='')
    failtxt = 'Incorrect input, Try Again'
    if tier_var.get() == 'Tier 1':
        t = 1
        v4 = '0'
        v5 = '0'
    elif tier_var.get() == 'Tier 2':
        t =2
        v4= var4.get()
        v5 = var5.get()
        if var1.get() == '' or int(var1.get())>6:
            failtxt = 'Incorrect Kit Quanity'
    else:
        t=3
        v4= var4.get()
        v5 = var5.get()
    if var1.get() == '' or var2.get() == '' or var3.get()=='' or v4 =='' or v5==''or failtxt =='Incorrect Kit Quanity':
        outtxt.config(text=failtxt, fg='red')
    else:
        a= (tier_costs(t,int(var1.get()),int(var2.get()),float(var3.get()),int(v4),int(v5)))
        outlabel.config(text= a)
        outtxt.config(text='Estimated Cost:',fg = 'black')
    outtxt.grid(row=13, column=0,pady='10')


def option_changed(*args):
    outtxt.config(text='')
    outlabel.config(text='')
    label1.grid(row=a+2,column=0,pady = '5')
    entry1.grid(row=a+3,column=0)
    label2.grid(row=a+4,column=0,pady = '5')
    entry2.grid(row=a+5,column=0)
    label3.grid(row=a+6,column=0,pady = '5')
    entry3.grid(row=a+7,column=0)
    label4.grid(row=a+8,column=0,pady = '5')
    entry4.grid(row=a+9,column=0)
    label5.grid(row=a+10,column=0,pady = '5')
    entry5.grid(row=a+11,column=0)
    tv = tier_var.get()
    if tv == 'Tier 1':
        label1.config(text = 'Practitioner Rate:')
        var1.set('65')
        label2.config(text='Travel Distance:')
        var2.set(0)
        label3.config(text='Travel Rate (/mile):')
        var3.set('0.585')
        label4.grid_remove()
        entry4.grid_remove()
        label5.grid_remove()
        entry5.grid_remove()
    elif tv == 'Tier 2':
        label1.config(text = '# of Kits:')
        label2.config(text='# of Participants:')
        var2.set(65)
        label3.config(text='Travel Rate (/mile):')
        var3.set('0.585')    
        label4.config(text='Travel Distance:')
        label5.config(text='Practitioner Rate:')
        var5.set(65)
    else:
        label1.config(text= '# of Kits')
        label2.config(text = '# of Participants')
    
	
# creating a label for
# name using widget Label
lbl_title = Label(master=frame1,font=('Arial',25,'bold'),text='Corporate Pricing Model',fg='white',bg='#3b84f8')
lbl_title.place(x=5,y =25)

tier_list = ('Tier 1','Tier 2', 'Tier 3')
option_menu = ttk.OptionMenu(frame2, tier_var,tier_list[0], *tier_list, command = option_changed)
tier_var.set('Select Tier')



label1 = tk.Label(frame2, text = 'Leave Blank', font=('calibre',10, 'bold'),bg = 'white')
entry1 = tk.Entry(frame2,textvariable = var1, font=('calibre',10,'normal'),justify='center')

label2 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white')
entry2=tk.Entry(frame2, textvariable = var2, font = ('calibre',10,'normal'),justify='center')

label3 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white')
entry3=tk.Entry(frame2, textvariable = var3, font = ('calibre',10,'normal'),justify='center')

label4 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white')
entry4=tk.Entry(frame2, textvariable = var4, font = ('calibre',10,'normal'), justify='center')

label5 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white')
entry5=tk.Entry(frame2, textvariable = var5, font = ('calibre',10,'normal'), justify='center')




outtxt =tk.Label(frame2, text = 'Estimated Cost:', font = ('calibre',10,'bold'),bg ='white')
outlabel =tk.Label(frame2, text = '', font = ('calibre',10,'bold'),bg = 'white')
# creating a button using the widget
# Button that will call the submit function
sub_btn=tk.Button(frame2,text = 'Calculate', command = submit)




# placing the label and entry in
# the required position using grid
# method
a = 0

option_menu.grid(row= a+1, column=0,pady='10')
sub_btn.grid(row=a+12,column=0,pady='10')

outlabel.grid(row=a+14, column=0)

# performing an infinite loop
# for the window to display

root.mainloop()
