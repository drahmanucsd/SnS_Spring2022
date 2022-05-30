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
def tier_costs(tier,e1,e2,e3,e4,e5,e6,vl):
    if (tier == 1):
        return np.round(tier1_cost(e1,e6,e2,e3),2)
    elif (tier == 2):
        return np.round(tier2_cost(e1,e2,e5,e6,e4,e3),2)
    else:
        return np.round(tier3_cost(vl,e2,e6,e6,e4,e5,e3),2)

# returns cost of a practitioner or concierge
def worker_cost(cost, travel_dist, travel_rate):
    return cost + travel_dist*travel_rate

# returns cost for tier 1 events
def tier1_cost(prac_cost, conc_cost, travel_dist, travel_rate):
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
def tier3_cost(consum_lst, num_participants, prac_cost1, prac_cost2, conc_cost, travel_dist, travel_rate):
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

    return np.sum(consum_array * consum_costs)




#  GUI


window = tk.Tk()
root = window

window.title("Pricing Model")
window.geometry('600x700')
window.config(bg='#ffffff')

# declaring string variable
# for storing name and password
var1=tk.StringVar()
var2=tk.StringVar()
var3=tk.StringVar()
var4=tk.StringVar()
var5=tk.StringVar()
var6=tk.StringVar()
var7=tk.StringVar()
var8=tk.StringVar()
var9=tk.StringVar()
var10=tk.StringVar()
var11=tk.StringVar()
var12=tk.StringVar()
var13=tk.StringVar()
tier_var = tk.StringVar()
t_o_var = tk.StringVar()




frame1 = tk.Frame(master=window, width=600, height=100, bg="#3b84f8")
frame1.pack()
frame2 = tk.Frame(master=window, width=600, height=600, bg="white")
frame2.pack()
# defining a function that will
# get the name and password and
# print them on the screen
def submit():
    outlabel.config(text='')
    failtxt = 'Incorrect input, Try Again'
    vl=()
    if tier_var.get() == 'Tier 1':
        t = 1
        v1= var1.get()
        v4 = '0'
        v5 = '0'
    elif tier_var.get() == 'Tier 2':
        t =2
        v1 = t_o_var.get()
        v4= var4.get()
        v5 = var5.get()
        if v1 == 'Herb Garder: Food As Medicine':
            v1 = '0'
        elif v1 == 'Botanical Beverages':
            v1 ='1'
        elif v1 == 'Therapuetic Truffles':
            v1 = '2'
        elif v1 == 'Seasonal Cooking Class':
            v1 = '3'
        elif v1 == 'Modern Medicine Tea Blending':
            v1 = '4'
        elif v1 == 'Aromatherapy':
            v1 = '5'
        elif v1 == 'Candle Making':
            v1 = '6'
        else:
            failtxt = 'Incorrect Kit Quanity'
    else:
        t=3
        v1 = '0'
        v4= var4.get()
        v5 = var5.get()
        try:
            v7 = int(var7.get())
            v8 = int(var8.get())
            v9 = int(var9.get())
            v10 = int(var10.get())
            v11 = int(var11.get())
            v12 = int(var12.get())
            v13 = int(var13.get())
            vl = (v7,v8,v9,v10,v11,v12,v13)
        except:
            failtxt = "Incorrect Kit Quantity"
    if v1 == '' or var2.get() == '' or var3.get()=='' or v4 =='' or v5==''or failtxt =='Incorrect Kit Quanity' or var6.get() == '':
        outtxt.config(text=failtxt, fg='red')
    else:
        a= (tier_costs(t,int(v1),int(var2.get()),float(var3.get()),int(v4),int(v5),int(var6.get()),vl))
        outlabel.config(text= a)
        outtxt.config(text='Estimated Cost:',fg = 'black')
    outtxt.grid(row=15, column=0,pady='10')


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
    label6.grid(row=a+12,column=0,pady = '5')
    entry6.grid(row=a+13,column=0)
    label7.grid_remove()
    entry7.grid_remove()
    label8.grid_remove()
    entry8.grid_remove()
    label9.grid_remove()
    entry9.grid_remove()
    label10.grid_remove()
    entry10.grid_remove()
    label11.grid_remove()
    entry11.grid_remove()
    label12.grid_remove()
    entry12.grid_remove()
    label13.grid_remove()
    entry13.grid_remove()
    t_options.grid_remove()
    tv = tier_var.get()
    if tv == 'Tier 1':
        label1.config(text = 'Practitioner Rate:')
        var1.set('65')
        label2.config(text='Travel Distance:')
        var2.set('')
        label3.config(text='Travel Rate (/mile):')
        var3.set('0.585')
        label6.config(text='Concierge Cost:')
        var6.set(25)
        label4.grid_remove()
        entry4.grid_remove()
        label5.grid_remove()
        entry5.grid_remove()
    elif tv == 'Tier 2':
        label1.config(text = 'Type of Kits:')
        entry1.grid_remove()
        t_options.grid(row=a+3,column=0)
        label2.config(text='# of Participants:')
        var2.set('')
        label3.config(text='Travel Rate (/mile):')
        var3.set('0.585')    
        label4.config(text='Travel Distance:')
        var4.set('')
        label5.config(text='Practitioner Rate:')
        var5.set(65)
        label6.config(text='Concierge Cost:')
        var6.set(25)
    else:
        label1.config(text= 'Medical Consumables:')
        label1.grid(row = a+1, column = 1,pady='5')
        entry1.grid_remove()
        var1.set('')
        label2.config(text ='# of Participants')
        var2.set('')
        label3.config(text='Travel Rate:')
        var3.set('0.585')
        label4.config(text='Concierge Cost:')
        var4.set('25')
        label5.config(text='Travel Distance:')
        var5.set('')
        label6.config(text='Practitioner Cost:')
        var6.set('25')
        label7.config(text='Accupuncture Supplies')
        label7.grid(row=a+2,column=1,pady = '5')
        entry7.grid(row=a+3, column=1)
        label8.config(text='B12 Shots')
        label8.grid(row=a+4,column=1,pady = '5')
        entry8.grid(row=a+5, column=1)
        label9.config(text='Vitamin Shots')
        label9.grid(row=a+6,column=1,pady = '5')
        entry9.grid(row=a+7, column=1)
        label10.config(text='IV Bag')
        label10.grid(row=a+8,column=1,pady = '5')
        entry10.grid(row=a+9, column=1)
        label11.config(text='Ear Seed Supplies')
        label11.grid(row=a+10,column=1,pady = '5')
        entry11.grid(row=a+11, column=1)
        label12.config(text='Acu Sup for Group')
        label12.grid(row=a+12,column=1,pady = '5')
        entry12.grid(row=a+13, column=1)
        label13.config(text='Acu Sup for Pop up Lounge')
        label13.grid(row=a+14,column=1,pady = '5')
        entry13.grid(row=a+15, column=1)

    
	
# creating a label for
# name using widget Label
lbl_title = Label(master=frame1,font=('Arial',25,'bold'),text='Corporate Pricing Model',fg='white',bg='#3b84f8')
lbl_title.place(x=110,y =25)
t_o = ('Herb Garder: Food As Medicine','Botanical Beverages','Therapuetic Truffles','Seasonal Cooking Class','Modern Medicine Tea Blending','Aromatherapy','Candle Making')
tier_list = ('Tier 1','Tier 2', 'Tier 3')
option_menu = ttk.OptionMenu(frame2, tier_var,tier_list[0], *tier_list, command = option_changed)
t_options = ttk.OptionMenu(frame2, t_o_var,t_o[0], *t_o)
tier_var.set('Select Tier')



label1 = tk.Label(frame2, text = 'Leave Blank', font=('calibre',10, 'bold'),bg = 'white',fg ='black')
entry1 = tk.Entry(frame2,textvariable = var1, font=('calibre',10,'normal'),justify='center',bg = 'white',fg ='black')

label2 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry2=tk.Entry(frame2, textvariable = var2, font = ('calibre',10,'normal'),justify='center',bg = 'white',fg ='black')

label3 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry3=tk.Entry(frame2, textvariable = var3, font = ('calibre',10,'normal'),justify='center',bg = 'white',fg ='black')

label4 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry4=tk.Entry(frame2, textvariable = var4, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label5 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry5=tk.Entry(frame2, textvariable = var5, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label6 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry6=tk.Entry(frame2, textvariable = var6, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')


label7 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry7=tk.Entry(frame2, textvariable = var7, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label8 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry8=tk.Entry(frame2, textvariable = var8, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label9 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry9=tk.Entry(frame2, textvariable = var9, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label10 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry10=tk.Entry(frame2, textvariable = var10, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label11 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry11=tk.Entry(frame2, textvariable = var11, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label12 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry12=tk.Entry(frame2, textvariable = var12, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')

label13 = tk.Label(frame2, text = 'Leave Black', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
entry13=tk.Entry(frame2, textvariable = var13, font = ('calibre',10,'normal'), justify='center',bg = 'white',fg ='black')



outtxt =tk.Label(frame2, text = 'Estimated Cost:', font = ('calibre',10,'bold'),bg ='white',fg ='black')
outlabel =tk.Label(frame2, text = '', font = ('calibre',10,'bold'),bg = 'white',fg ='black')
# creating a button using the widget
# Button that will call the submit function
sub_btn=tk.Button(frame2,text = 'Calculate', command = submit)




# placing the label and entry in
# the required position using grid
# method
a = 0

option_menu.grid(row= a+1, column=0,pady='10')
sub_btn.grid(row=a+14,column=0,pady='20')

outlabel.grid(row=a+16, column=0)

# performing an infinite loop
# for the window to display

root.mainloop()
