from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter.ttk import Progressbar
from tkinter.ttk import Scrollbar
import os
import csv
import ntpath
import pandas as pd



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
window.geometry('600x300')
window.config(bg='#ffffff')

# frames
frame1 = Frame(bg='#3b84f8') # holds the title
frame1.pack(fill='x')
frame6 = Frame(bg='#ffffff') # holds the interactive message
frame6.pack()
frame2 = Frame(bg='#ffffff') # holds the choose file, preview, and start buttons
frame2.pack()
frame3 = Frame(bg='#ffffff') # holds the progress bar
frame3.pack(fill='x')
# frame5 = Frame(bg='#ffffff') # holds the scroll bar and frame 4
# frame5.pack()

# scroll bar and preview file frame
def scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=600,height=200,bg='#ffffff')

# canvas=Canvas(master=frame5,bg='#ffffff')
# frame4 = Frame(master=canvas,borderwidth=3,relief=SOLID) # holds the preview
# scroll_bar = Scrollbar(master=frame5,orient="horizontal",command=canvas.xview)
# canvas.configure(xscrollcommand=scroll_bar.set)
# scroll_bar.pack(fill="x")
# canvas.pack(side='left')
# canvas.create_window((0,0),window=frame4,anchor='nw')
# frame4.bind("<Configure>",scroll)

# initialize xfile as a global variable
xfile = None
csv_file = None

# handler for 'Choose File' button click event
def open_xfile():
    global xfile
    xfile = filedialog.askopenfilename(title='open a file',filetypes=(('excel files','*.xls'),('excel files','*.xlsx')))
    filename = ''
    # if len(ntpath.basename(xfile)) > 25:
    #     filename = ntpath.basename(csv_file)[:25]+'...'
    # else:
    #     filename = ntpath.basename(xfile)
    filename = ntpath.basename(xfile)
    lbl_filename.config(text=filename,fg='grey')
    start()
    
# handler for 'Start' button click event
def start(): 
    if is_file_uploaded() == False:
        return None
    # if verify_columns() == False:
    #     lbl_message.config(text='Incorrect file format',fg='red')
    #     return None
    categorize_revenue()
    #btn_download.pack(padx=10,pady=10)
    
# checks if a file has been uploaded
def is_file_uploaded():
    if xfile != None:
        lbl_message.config(text='Click \'Download\' to save your file',fg='green')
        return True
    else:
        lbl_message.config(text='You need to upload a file first',fg='red')
        return False
        
        
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


def categorize_revenue():
    global xfile
    output = xfile
    xfile = pd.read_excel(xfile)
    # xfile.to_excel('temp.xlsx', index = None, header = True)
    
    xfile.insert(5, 'Item Type', ['empty']*xfile.shape[0])
    item_name = xfile[xfile.columns[4]]
    item_type = xfile[xfile.columns[5]]
    
    #catgeories for item names
    members = ['(M)','12 services', '24 services', 'Transcend Annual Non-Medical Combo Credit', 'Transcend Annual Medical Combo Credit', 'Nourish Annual Medical Credit']
    
    appoints = ['(A)', 'Service Credit', 'Acupuncture', '2 services', '1 service', 'Complimentary Consultation', 'Appointment', 'Sacred Sunday Members']
    
    events = ['(E)', 'Moon Circle', 'Sunset Horseback Riding', 'Sunset Turtle Releasing Ceremony', 'Getaway', 'Drop In', 'Reiki', 'Sacred Sunday Drop In', 'Sacred Sunday Non-Member']
    
    retails = ['(R)', '(S)']
    
    corps = ['(C)']
    
    consults = ['Client Consultation']
    
    deletions = ['(D)', 'Internal Meeting Non Member', '$150 Membership Pricing', '$125 Membership Pricing', '$100 Membership Pricing']
    
    # print(item_name)
    #categorize based on lists above
    for index in range(len(item_name)):
        service = item_name[index]
        # print()
        print(service)
        if any(cat in service for cat in members):
            id = xfile[xfile.columns[1]]
            if xfile.at[index, 'Client ID'] in member_IDs:
                #xfile[xfile.columns[5]][index] = 'Membership - Renewal'
                xfile.at[index, 'Item Type'] = 'Membership - Renewal'
                 
            else:
                member_IDs.append(id)
                #xfile[xfile.columns[5]][index] = 'Membership - New'
                xfile.at[index, 'Item Type'] = 'Membership - New'
                
            
        elif any(cat in service for cat in appoints):
            # xfile[xfile.columns[5]][index] = 'Appointment'
            xfile.at[index, 'Item Type'] = 'Appointment'
            
            
        elif any(cat in service for cat in events):
            # xfile[xfile.columns[5]][index] = 'Event'
            xfile.at[index, 'Item Type'] = 'Event'
            
        elif any(cat in service for cat in retails):
            # xfile[xfile.columns[5]][index] = 'Retail'
            xfile.at[index, 'Item Type'] = 'Retail'
        
        elif any(cat in service for cat in corps):
            # xfile[xfile.columns[5]][index] = 'Corporate Event'
            xfile.at[index, 'Item Type'] = 'Corporate Event'
            
        elif any(cat in service for cat in deletions):
            # xfile[xfile.columns[5]][index] = 'DELETE'
            xfile.at[index, 'Item Type'] = 'DELETE'
            #xfile = xfile.drop(xfile.index[index])
            #print(xfile.loc[index, xfile.columns[4]])
        
        elif any(cat in service for cat in consults):
            # xfile[xfile.columns[5]][index] = 'Consultation'
            xfile.at[index, 'Item Type'] = 'Consultation'
    
        else:
            # xfile[xfile.columns[5]][index] = 'UNCATEGORIZED'
            xfile.at[index, 'Item Type'] = 'UNCATEGORIZED'
        
        
    # categorized = pd.DataFrame(columns = xfile.columns)
    # 
    # for row in range(xfile.shape[0]):
    #     if xfile.at[row, 'Item Type'] != 'DELETE':
    #         categorized = categorized.append(xfile.iloc[row])
    # 
    #print(categorized)
    
    print(xfile[xfile.columns[5]])
    #write out new member ID data
    with open('membership_data.txt','w') as f:
            for elem in member_IDs:
                f.write(elem + '\n')
    xfile.to_excel(output, index = None, header = True)           
    print(xfile)
    
# handler for 'Download' button click
def download():
    save_path = filedialog.asksaveasfilename(filetypes=(('excel files' ,'*.xls'))) + '.xls'
    
    final = pd.read_csv(xfile)
    final.to_excel(save_path, index = None, header=True)
        

# create widgets (labels, buttons, progress bar, scroll bar)3b84f8
lbl_title = Label(master=frame1,font=('Arial',25,'bold'),text='Revenue Categorization Script',fg='white',bg='#3b84f8')
lbl_filename = Label(master=frame2,text='No File Chosen',fg='grey',width=20,anchor='w')
lbl_message = Label(master=frame6,text='*Please upload a file',bg='white', fg='#3b84f8')

btn_choosefile = Button(master=frame2,text='Choose File',command=open_xfile, fg = "white", font = "Future 10", bg="#3b84f8")
# btn_start = Button(master=frame2,text='Start',command=start)
# btn_preview = Button(master=frame2,text='Preview',command=preview)
# btn_download = Button(master=frame3,text='Download',command=download)

progress_bar = Progressbar(master=frame3, orient=HORIZONTAL, length=500, mode='determinate')

# scroll_bar = Scrollbar(master=frame5, orient='horizontal')

# pack widgets
lbl_title.pack(padx=20,pady=20)
lbl_filename.grid(sticky='w',row=0,column=1,padx=10,pady=10)
lbl_message.pack(pady=5)

btn_choosefile.grid(sticky='w',row=0,column=0,padx=10,pady=10)
# btn_start.grid(sticky='w',row=1,column=1,padx=10,pady=10)
# btn_preview.grid(sticky='w',row=1,column=0,padx=10,pady=10)

progress_bar.pack(padx=10,pady=20,expand=True)

# execute
window.mainloop() 