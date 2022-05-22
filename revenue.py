from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.ttk import Progressbar
from tkinter.ttk import Scrollbar
import os
import csv
import ntpath
import pandas as pd

# variables
new_rows = []
item_type = []
correct_format1 = ['Sale Date', 'Client ID', 'Client', 'Sale ID', 'Item name', 'Batch #', 'Sales Notes', 'Location', '', 'Color', 'Size', 'Item price', 'Quantity', 'Subtotal', 'Discount %', 'Discount amount', 'Tax', 'Item Total', 'Total Paid w/ Payment Method', 'Payment Method']
correct_format2 =['\ufeffSale Date', 'Client ID', 'Client', 'Sale ID', 'Item name', 'Batch #', 'Sales Notes', 'Location', '', 'Color', 'Size', 'Item price', 'Quantity', 'Subtotal', 'Discount %', 'Discount amount', 'Tax', 'Item Total', 'Total Paid w/ Payment Method', 'Payment Method']
has_previewed = False
member_IDs = ['100008243', '834', '1,288', '100008192', '100008373', '6,705', '3,173', '100003950', '4,984', '4,464', 
    '100006795', '6,381', '6,407', '5,861', '100006443', '5,895', '3,841', '4,213', '7,070', '100007059', '100007093', 
    '3,955', '100008002', '5,278', '12,851', '100007602', '4,851', '100008341', '6,427', '2,135', '5,092', '100006683', 
    '100006665', '5,127', '4,644', '100006997', '100006753', '3,332', '6,608', '100005254', '100007329', '6,663', '3,734', 
    '6,506', '5,915', '4,554', '100006313', '6,785', '100006707', '3,742', '100006616', '100007855', '100008033', '100007361', 
    '100006885', '100006968', '2,134', '100006880', '100007857', '1,276', '100006713', '100007827', '100005810', '100006677', 
    '100007753', '2021121512573526186920', '100006779', '100007895', '100008285', '3,921', '100007314', '2,137', '6,433', 
    '100008328', '4,047', '100008221', '100006819', '5,540', '5,542', '6,523', '3,157', '100007934', '100007006', '6,361', 
    '2,963', '100006686', '5,734', '100007303', '100006979', '3,089', '4,206', '100007345', '6,336', '100006731', '3,043', 
    '1,284', '100007079', '2,346', '100007028', '5,903', '100007821', '5,637', '4,598', '100007584', '100007925', '5,119', 
    '100007805', '100006808', '883', '6,039', '100007283', '100008035', '5,884', '2021121006063212158218', '5,395', '100001062', 
    '3,849', '100007603', '873', '6,769', '7,310', '3,142', '5,561', '6,952', '3,842', '5,740', '100007908', '100007469', 
    '100007065', '100007250', '5,968', '4,968', '7,168', '100006625', '100006907', '6,762', '3,010', '100007325', '6,375', 
    '6,823', '100008249', '100007552', '100006733', '100006846', '100006978', '100008113', '100006663', '100006837', '3,738', 
    '100006775', '100007952', '100007265', '6,448', '6,621', '2,521', '100007978', '4,676', '100007020', '100007078', '100007667', 
    '100008140', '100006874', '100007132', '3,641', '7,159', '2,440', '100006701', '100007571', '5,602', '100007979', '100006676', 
    '2,804', '5,622', '6,168', '3,014', '5,438', '4,957', '100007313', '100008205', '5,656', '100007902', '6,613', '5,532', 
    '4,158', '6,945', '3,475', '100007580', '5,508', '4,065', '6,805', '3,017', '3,833', '100006809', '5,783', '100006872', 
    '5,356', '4,311', '6,835']
file_exists = os.path.exists('membership_data.txt')

#write membership IDs data to text file
if file_exists == False:
    with open('membership_data.txt','w') as f:
        for elem in member_IDs:
            f.write(elem + '\n')
else:
    with open('membership_data.txt','r') as f:
        data = f.read().splitlines()
        member_IDs = []
        for elem in data:
            member_IDs.append(elem)

#main window
window = Tk()
window.title("Revenue Categorization")
window.geometry('700x480')

# frames
frame1 = Frame(bg='#4CB963') # holds the title
frame1.pack(fill='x')
frame6 = Frame() # holds the interactive message
frame6.pack()
frame2 = Frame() # holds the choose file, preview, and start buttons
frame2.pack()
frame3 = Frame(bg='#D3D3D3') # holds the progress bar
frame3.pack(fill='x')
frame5 = Frame() # holds the scroll bar and frame 4
frame5.pack()

# scroll bar and preview file frame
def scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=600,height=200)

canvas=Canvas(master=frame5)
frame4 = Frame(master=canvas,borderwidth=3,relief=SOLID) # holds the preview
scroll_bar = Scrollbar(master=frame5,orient="horizontal",command=canvas.xview)
canvas.configure(xscrollcommand=scroll_bar.set)
scroll_bar.pack(fill="x")
canvas.pack(side='left')
canvas.create_window((0,0),window=frame4,anchor='nw')
frame4.bind("<Configure>",scroll)

# initialize csv_file as a global variable
csv_file = None

# handler for 'Choose File' button click event
def open_csv():
    global csv_file
    csv_file = filedialog.askopenfilename(title='open a file',filetypes=(('csv files','*.csv'),))
    filename = ''
    if len(ntpath.basename(csv_file)) > 25:
        filename = ntpath.basename(csv_file)[:25]+'...'
    else:
        filename = ntpath.basename(csv_file)
    lbl_filename.config(text=filename,fg='grey')

# handler for 'Start' button click event
def start(): 
    if is_file_uploaded() == False:
        return None
    if verify_columns() == False:
        lbl_message.config(text='Incorrect file format',fg='red')
        return None
    categorize_revenue()
    btn_download.pack(padx=10,pady=10)

# verifies that the input CSV is in the correct format
def verify_columns():
    with open(csv_file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        file_format = list(csv_reader)[0]
        if file_format != correct_format1 and file_format != correct_format2:
            return False
        else:
            return True

# handler for 'Start' button click event
def preview():
    if is_file_uploaded() == False:
        return None
    else:
        lbl_message.config(text='Click \'Start\' to run the script',fg='green')
    global has_previewed
    if has_previewed == True:
        clearFrame(frame4)
    with open(csv_file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        rows = [row for row in csv_reader]
        line_count = 0
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if line_count == 0:
                    frame_individual = Frame(master=frame4)
                    frame_individual.grid(row=i,column=j,sticky='w')
                    bold_font = font.Font(weight='bold')
                    lbl_row = Label(master=frame_individual,text=str(rows[i][j]),font=bold_font)
                    lbl_row.pack()
                else:
                    frame_individual = Frame(master=frame4)
                    frame_individual.grid(row=i,column=j,sticky='w')
                    lbl_row = Label(master=frame_individual,text=str(rows[i][j]))
                    lbl_row.pack()
            line_count+=1
            if line_count == 6:
                break
    if has_previewed == False:
        has_previewed = True

# revenue categorization function
def categorize_revenue():
    with open(csv_file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        rows = [row for row in csv_reader] #turns CSV into a list
        line_count = 0
        for row in rows:
            if line_count == 0:
                item_type.append("Item Type")
                line_count += 1
            else:
                if '(M)' in str(row[4]) or '12 services' in str(row[4]) or '24 services' in str(row[4])\
                    or 'Transcend Annual Non-Medical Combo Credit' in str(row[4]) or 'Transcend Annual Medical Combo Credit' in str(row[4])\
                    or 'Nourish Annual Medical Credit' in str(row[4]):
                        if str(row[1]) in member_IDs:
                            item_type.append('Membership - Renewal')
                        else:
                            item_type.append('Membership - New')
                            member_IDs.append(str(row[1]))
                elif '(A)' in str(row[4]) or 'Service Credit' in str(row[4]) or 'Acupuncture' in str(row[4])\
                    or '2 services' in str(row[4]) or '1 service' in str(row[4]) \
                    or 'Complimentary Consultation' in str(row[4]) or 'Appointment' in str(row[4])\
                    or 'Sacred Sunday Members' in str(row[4]): #need to double check sacred sunday
                    item_type.append('Appointment')
                elif '(E)' in str(row[4]) or 'Moon Circle' in str(row[4]) or 'Sunset Horseback Riding' in str(row[4])\
                    or 'Sunset Turtle Releasing Ceremony' in str(row[4]) or 'Getaway' in str(row[4])\
                    or 'Drop In' in str(row[4]) or 'Reiki'  in str(row[4])\
                    or 'Sacred Sunday Drop In' in str(row[4]) or 'Sacred Sunday Non-Member' in str(row[4]): #need to double check sacred sunday
                    item_type.append('Event')
                elif '(R)' in str(row[4]) or '(S)' in str(row[4]):
                    item_type.append('Retail')
                elif '(C)' in str(row[4]):
                    item_type.append('Corporate Event')
                elif '(D)' in str(row[4]) or 'Internal Meeting Non Member' in str(row[4]) or '$150 Membership Pricing' in str(row[4])\
                    or '$125 Membership Pricing' in str(row[4]) or '$100 Membership Pricing' in str(row[4]):
                    item_type.append('DELETE')
                elif str(row[4]) == 'Client Consultation':
                    item_type.append('Consultation')
                else:
                    item_type.append('UNCATEGORIZED')
                line_count += 1
            new_rows.append(row[0:4] + [item_type[line_count-1]] + row[4:])
            progress_bar['value'] += (1/len(rows))*100
    #write out new member ID data
    with open('membership_data.txt','w') as f:
            for elem in member_IDs:
                f.write(elem + '\n')
    
    xfile = pd.read_csv(csv_file)
    xfile.to_excel(csv_file, index = None, header=True)
    
    print(xfile)
    

# handler for 'Download' button click
def download():
    save_path = filedialog.asksaveasfilename(filetypes=(('excel files', '*.xls'), ('excel files', '*.xlsx'))) + '.xls'
    with open(save_path,mode='w') as new_csv_file:
        new_data = csv.writer(new_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in new_rows:
            if i[4] != 'DELETE':
                new_data.writerow(i)
    

# checks if a file has been uploaded
def is_file_uploaded():
    if csv_file != None:
        lbl_message.config(text='Click \'Download\' to save your file',fg='green')
        return True
    else:
        lbl_message.config(text='You need to upload a file first',fg='red')
        return False

def clearFrame(frm):
    for widgets in frm.winfo_children():
        widgets.destroy()

# create widgets (labels, buttons, progress bar, scroll bar)
lbl_title = Label(master=frame1,font=('Arial',25,'bold'),text='Revenue Categorization Script',fg='black',bg='#4CB963')
lbl_filename = Label(master=frame2,text='No File Chosen',fg='grey',width=20,anchor='w')
lbl_message = Label(master=frame6,text='*Please upload a file')

btn_choosefile = Button(master=frame2,text='Choose File',command=open_csv)
btn_start = Button(master=frame2,text='Start',command=start)
btn_preview = Button(master=frame2,text='Preview',command=preview)
btn_download = Button(master=frame3,text='Download',command=download)

progress_bar = Progressbar(master=frame3, orient=HORIZONTAL, length=250, mode='determinate')

scroll_bar = Scrollbar(master=frame5, orient='horizontal')

# pack widgets
lbl_title.pack(padx=20,pady=20)
lbl_filename.grid(sticky='w',row=0,column=1,padx=10,pady=10)
lbl_message.pack(pady=5)

btn_choosefile.grid(sticky='w',row=0,column=0,padx=10,pady=10)
btn_start.grid(sticky='w',row=1,column=1,padx=10,pady=10)
btn_preview.grid(sticky='w',row=1,column=0,padx=10,pady=10)

progress_bar.pack(padx=10,pady=20,expand=True)

# execute
window.mainloop() 