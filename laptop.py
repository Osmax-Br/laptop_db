from tkinter.constants import FALSE, RIGHT
from guizero import *
from tksheet import Sheet
import tkinter as tk
import sqlite3
import webbrowser
import os,sys
import shutil
import ctypes
import socket
import struct
import time
import datetime 
conntected_to_internet = False
year = month = day = hour = minutes = sec = -1
week_day = ""
week_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
ctypes.windll.shcore.SetProcessDpiAwareness(1)
db = sqlite3.connect("laptop.db")
app = App(title= "hello",width= 815,height=430)

#app.tk.state('zoomed')

command = """ create table if not exists specs (
              barcode text primary key not null,
              manufacturer text not null,
              laptop_model text,
              catigory text not null,
              cpu_company text not null,
              cpu_family text not null,
              gen int not null,
              cpu_model text,
              ram_size int not null,
              ddr text not null,
              upgradable_ram int not null,
              integrated_gpu int not null,
              gpu_company text not null,
              gpu_model text,
              gpu_vram int,
              gpu_vram_upto int,
              storage_option_1_type text not null,
              storage_option_1_size int not null,
              storage_option_2_type text not null,
              storage_option_2_size int not null,
              storage_option_3_type text not null,
              storage_option_3_size int not null,
              screen_size text not null,
              resulotion text not null,
              refresh_rate text not null,
              touch int not null,
              rot360deg int not null,
              arabic_keyboard int not null,
              backlit int not null,
              rgb int,
              numpad int not null,
              os text,
              odd int not null,
              usb_ports int not null,
              usb3 int not null,
              typec int not null,
              thunderbolt int not null,
              ethernet int not null,
              hdmi int not null,
              headphone_jack int not null,
              sdcard int not null,
              buy_price int,
              sell_price int,
              revenue int,
              used int not null,
              condition text,
              quantity int not null
              );
              """
db.execute(command)
db.commit()
command = """Create table if not exists amd_cpus (amd_cpu text);"""
db.execute(command)
db.commit()
command = """Create table if not exists brands(brand text);"""
db.execute(command)
db.commit()   
command = """Create table if not exists intel_cpus (intel_cpu text);"""
db.execute(command)
db.commit()                 
selected_cpu = "intel"
selected_gen = "intel"
cpu_gen = 0
gen = 0
brand_options= ["Choose company","Asus","Dell","hp","lenovo","microsoft"]
cpus = ["choose cpu","Core 2 Duo","Celeron","Core i3","Core i5","Core i7","Core i9","Xeon"]
def init_cpu_data():
    command = """select intel_cpu from intel_cpus"""
    c = db.cursor()
    c.execute(command)
    cpu_data = c.fetchall()
    standard_cpus_intel = ["choose cpu","Core 2 Duo","Celeron","Core i3","Core i5","Core i7","Core i9","Xeon"]
    if not cpu_data :
        for i in range(len(standard_cpus_intel)):
            current_cpu = ""
            current_cpu = standard_cpus_intel[i]
            c.execute(f"""insert into intel_cpus values ("{current_cpu}") """)
            db.commit()
    ####
    command = """select amd_cpu from amd_cpus"""
    c1 = db.cursor()
    c1.execute(command)
    cpu_data2 = c1.fetchall()
    standard_cpus_amd = ["choose cpu","Ryzen 3","Ryzen 5","Ryzen 7","Ryzen 9","threadripper","a4","a6","a9","a12","athlon"]
    if not cpu_data2 :
        for i in range(len(standard_cpus_amd)):
            current_cpu = ""
            current_cpu = standard_cpus_amd[i]
            c.execute(f"""insert into amd_cpus values ("{current_cpu}") """)
            db.commit() 
    command = """select brand from brands"""
    c2 = db.cursor()
    c2.execute(command)
    brand_data = c2.fetchall()
    standard_brand_options= ["Choose company","Asus","Dell","hp","lenovo"]
    if not brand_data :
        for i in range(len(standard_brand_options)):
            current_brand = ""
            current_brand = standard_brand_options[i]
            c.execute(f"""insert into brands values ("{current_brand}") """)
            db.commit() 
def get_cpu_data():
    command = "Select * from intel_cpus"
    c = db.cursor()
    c.execute(command)
    current_cpu = c.fetchall()
    global cpus_intel
    cpus_intel = []
    for i in current_cpu:
        cpus_intel.append(i[0])
    #######
    command = "Select * from amd_cpus"
    c = db.cursor()
    c.execute(command)
    current_cpu = c.fetchall()
    global cpus_amd
    cpus_amd = []
    for i in current_cpu:
        cpus_amd.append(i[0])
    #########
    command = "Select * from brands"
    c = db.cursor()
    c.execute(command)
    current_cpu = c.fetchall()
    global brand_options
    brand_options = []
    for i in current_cpu:
        brand_options.append(i[0])
#
def RequestTimefromNtp(addr='pool.ntp.org'):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
    data =  time.ctime(t)
    data = time.strptime(data)
    return data
def en_model():
    maker.remove("Choose company")
def chg_comp():
    global selected_cpu
    cpu.enable()
    if(company.value == "intel"):
         selected_cpu = "intel"
         gen_amd.hide()
         gen_intel.show()
         cpus = cpus_intel
         cpu.clear()
         for i in cpus:
            cpu.append(i)   
    elif(company.value == "amd"):
         selected_cpu = "amd"
         gen_amd.show()
         gen_intel.hide()
         cpus = cpus_amd
         cpu.clear()
         for i in cpus:
            cpu.append(i)
def check_value(obj,max,text):
    value = obj.value
    value_int = 0
    try:
        if(value == ""):
           value = "0"
        value_int = int(value)
    except:
        info("hi","please put integer")
        obj.value = ""
    if(value_int >max):
        info("hi",f"yo we need resonable amount of {text}")
        obj.value = ""           
def chk_val_ram():
    check_value(ram_size,120,"ram")
def chk_val_vram():
    check_value(vram,32,"vram")
def chk_val_vram_upto():
    check_value(vram_upto,32,"vram")
def chk_ddr():
    global cpu_gen
    if(selected_cpu == "intel" and cpu.value != "Core 2 Duo"):
        selected_gen = "intel"
        cpu_gen = gen_intel.value
        if(cpu_gen > 5):
            ddr.value = "DDR4"
        else:
            ddr.value = "DDR3"
    elif(selected_cpu == "amd" and cpu.value != "athlon"):
        selected_gen = "amd"
        cpu_gen = gen_amd.value
    else:
        selected_gen = "n/a"
        cpu_gen = 0
def hi():
    global cpu_gen
    cpu.remove("choose cpu")
    if(cpu.value == "Core 2 Duo"):
        gen_intel.disable()
        gen_intel.bg = [160,160,160]
        gen_intel.value = "0"
        selected_gen = "n/a"
        cpu_gen = 0
    elif(cpu.value == "a4" or cpu.value == "a6" or cpu.value == "a9" or cpu.value == "a12" or cpu.value == "athlon"):
        gen_amd.disable()
        gen_amd.bg = [160,160,160]
        gen_amd.value = "0"
        cpu_gen = 0
    else:
        gen_amd.bg = None
        gen_intel.bg = None
        gen_amd.enable()
        gen_intel.enable()

def chk_val_op1():
    check_value(op1_size,9999,"storage")
def op2_na():
    if(storage_op2.value == "N/A"):
        op2_size.clear()
        op2_size.disable()
    else:
        op2_size.enable()
def chk_val_op2():
    check_value(op2_size,9999,"storage")
def chk_val_op3():
    check_value(op3_size,9999,"storage")
def op3_na():
    if(storage_op3.value == "N/A"):
        op3_size.clear()
        op3_size.disable()
    else:
        op3_size.enable()
def rgb_en():
    if(backlit.value == 1):
       rgb.enable()
       rgb.text_color = "red"
    else:
       rgb.value = 0
       rgb.disable()
def en_os():
    if(original.value == 1):
       op_sys.enable()
    else:
       op_sys.disable()
       op_sys.value = "N/A"
def regulate_buy():
    value = buy_price.value
    value_int = 0
    try:
        if(value == ""):
           value = "0"
           value_int = int(value)
        else:
           value_int = int(value) 
    except:
        info("hi","please put integer")
        buy_price.value = ""
    if(value_int >10000000):
        buy_price.text_color = "red"
    else:
        buy_price.text_color = None   
def regulate_sell():
    value = sell_price.value
    value_int = 0
    try:
        if(value == ""):
           value = "0"
           value_int = int(value)
        else:
           value_int = int(value)  
    except:
        info("hi","please put integer")
        sell_price.value = ""
    if(value_int >10000000):
        sell_price.text_color = "red"
    else:
        sell_price.text_color = None
    try:
        if(sell_price.value == "" or buy_price.value == ""):
            money.value = 0
        else:    
            money.value = int(sell_price.value) - int(buy_price.value)
    except:
        print("error")
        info("hi","error at price calculation!")
def en_condition():
    if(used.value == 1):
        condition.enable()
        condition.remove("new")
    else:
        condition.disable()
        condition.append("new")
        condition.value = "new"
def regulate_qt():
    value = quantity.value
    value_int = 0
    try:
        if(value == ""):
           value = "0"
           value_int = int(value)
        else: 
           value_int = int(value) 
    except:
        info("hi","please put integer")
        quantity.value = ""
    if(value_int >10):
        quantity.text_color = "red"
    else:
        quantity.text_color = None
def intergrated():
    if(integrated.value == 1):
        gpu_company.disable()
        if(selected_cpu == "intel"):
            gpu_company.value = "intel"
        else:
            gpu_company.value = "amd"            
    else:
        gpu_company.enable()        
def save():
    duplicate = False
    c = db.cursor()
    c.execute("""select barcode from specs where barcode = ? """,(barcode.value,))
    if c.fetchone():
        info("hi","duplicated barcode")
        barcode.value = ""     
    else:
         if(barcode.value == ""):
             info("hi","please fill barcode box")
         elif(maker.value == "Choose company"):
             info("hi","please fill laptop manufacturer box")
         elif(cpu.value == "choose cpu"):
             info("hi","please fill cpu box")
         elif(ram_size.value == ""):
             info("hi","please fill ram box")
         elif(quantity.value == ""):
             info("hi","please fill quantity box")
         else:
            try:
                db.execute( """
                          insert into specs values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(barcode.value,maker.value,model.value,catigory.value,company.value,
                          cpu.value,cpu_gen,cpu_model.value,ram_size.value,ddr.value,upgradable.value,integrated.value,gpu_company.value,gpu_model.value,
                          vram.value,vram_upto.value,storage_op1.value,op1_size.value,storage_op2.value,op2_size.value,storage_op3.value,op3_size.value,
                          screen_size.value,screen_resulotion.value,screen_refresh.value,touch.value,deg360.value,
                          arabic.value,backlit.value,rgb.value,numpad.value,op_sys.value,odd.value,Usb_num.value,usb3_supp.value,usb_typec.value,
                          thunderbolt_supp.value,ethernet_supp.value,hdmi_supp.value,headphonejack_supp.value,sdcard_supp.value,
                          buy_price.value,sell_price.value,money.value,used.value,condition.value,quantity.value))
                
                db.commit()
            except:
                info("hi","an error occurred during the save process")
def table(cmnd):
    c = db.cursor()
    c.execute(cmnd)
    data = c.fetchall()
    class demo(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            self.grid_columnconfigure(0, weight = 1)
            self.grid_rowconfigure(0, weight = 1)
            self.frame = tk.Frame(self)
            self.frame.grid_columnconfigure(0, weight = 1)
            self.frame.grid_rowconfigure(0, weight = 1)
            self.sheet = Sheet(self.frame,
                               page_up_down_select_row = True,
                               expand_sheet_if_paste_too_big = True,
                               column_width = 120,
                               startup_select = (0,1,"rows"),
                                data = [[f"Row {r}, Column {c}" for c in range(5)] for r in range(len(data))], #to set sheet data at startup
                                headers = ["barcode",
                                "manufacturer",
                                "laptop model",
                                "catigory",
                                "cpu company",
                                "cpu family",
                                "gen",
                                "cpu model",
                                "ram size",
                                "ddr",
                                "upgradable ram",
                                "integrated gpu",
                                "gpu company",
                                "gpu model",
                                "gpu vram",
                                "gpu vram up to",
                                "storage option 1 type",
                                "storage option 1 size",
                                "storage option_2 type",
                                "storage option_2 size",
                                "storage option_3 type",
                                "storage option_3 size",
                                "screen size",
                                "resulotion",
                                "refresh rate",
                                "touch",
                                "360 degree",
                                "arabic keyboard",
                                "backlit",
                                "rgb",
                                "numpad",
                                "os",
                                "odd",
                                "usb ports",
                                "usb3",
                                "typec",
                                "thunderbolt",
                                "ethernet",
                                "hdmi",
                                "headphone jack",
                                "sdcard",
                                "buy price",
                                "sell price",
                                "revenue",
                                "used",
                                "condition",
                               "quantity"],
                                theme = "dark blue",
                                height = 500, #height and width arguments are optional
                                width = 2000 #For full startup arguments see DOCUMENTATION.md
                                )
            self.sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                             "drag_select",   #enables shift click selection as well
                                        "select_all",
                                             "column_drag_and_drop",
                                             "row_drag_and_drop",
                                             "column_select",
                                             "row_select",
                                             "column_width_resize",
                                             "double_click_column_resize",
                                             "row_width_resize",
                                             "column_height_resize",
                                             "arrowkeys",
                                             "row_height_resize",
                                             "double_click_row_resize",
                                             "right_click_popup_menu",
                                             "rc_select",
                                             "copy"
                                             
                                             
                                             
                                        ))
            self.frame.grid(row = 0, column = 0, sticky = "nswe")
            self.sheet.grid(row = 0, column = 0, sticky = "nswe")
            #ur code here
            data_rows = len(data)
            #self.sheet.set_cell_data(1, 2, "NEW VALUE")
            for r in range(len(data)):
                #for i in data[r]
                self.sheet.set_row_data(r, values = (data[r][0],data[r][1],data[r][2],data[r][3],data[r][4],data[r][5],data[r][6],data[r][7],data[r][8],
                                                     data[r][9],data[r][10],data[r][11],data[r][12],data[r][13],data[r][14],data[r][15],data[r][16],
                                                     data[r][17],data[r][18],data[r][19],data[r][20],data[r][21],data[r][22],data[r][23],data[r][24],
                                                     data[r][25],data[r][26],data[r][27],data[r][28],data[r][29],data[r][30],data[r][31],data[r][32],
                                                     data[r][33],data[r][34],data[r][35],data[r][36],data[r][37],data[r][38],data[r][39],data[r][40],
                                                     data[r][41],data[r][42],data[r][43],data[r][44],data[r][45],data[r][46]))   
    app = demo()
    app.mainloop()
def search():
    table("""select * from specs """)
def search_barcode():
    try:
          barcodeval = barcode.value
          barcodeval = barcodeval.rstrip()
          command = """ select * from specs where barcode = "{}"  """.format(barcodeval)
          c  = db.cursor()
          c.execute(command)
          data = c.fetchall()
          chg_comp()
          maker.value = data[0][2-1]
          model.value= data[0][3-1]
          catigory.value= data[0][4-1]
          company.value= data[0][5-1]
          chg_comp()
          cpu.value= data[0][6-1]
          hi()
          cpu_gen= data[0][7-1]
          if(selected_cpu == "intel"):
              gen_intel.value = cpu_gen
          else:
              gen_amd.value = cpu_gen          
          cpu_model.value= data[0][8-1]
          ram_size.value= data[0][9-1]
          ddr.value= data[0][10-1]
          upgradable.value= data[0][11-1]
          integrated.value= data[0][12-1]
          if(integrated.value == 1):
                gpu_company.disable()
          else:
                gpu_company.enable()          
          gpu_company.value= data[0][13-1]
          gpu_model.value= data[0][14-1]
          vram.value= data[0][15-1]
          vram_upto.value= data[0][16-1]
          storage_op1.value= data[0][17-1]
          op1_size.value= data[0][18-1]
          storage_op2.value= data[0][19-1]
          op2_na()
          op2_size.value= data[0][20-1]
          storage_op3.value= data[0][21-1]
          op3_na()
          op3_size.value= data[0][22-1]
          screen_size.value= data[0][23-1]
          screen_resulotion.value= data[0][24-1]
          screen_refresh.value= data[0][25-1]
          touch.value= data[0][26-1]
          deg360.value= data[0][27-1]
          arabic.value= data[0][28-1]
          backlit.value= data[0][29-1]
          rgb_en()
          rgb.value= data[0][30-1]
          numpad.value= data[0][31-1]
          op_sys.value= data[0][32-1]
          op_sys.enable()
          odd.value= data[0][33-1]
          Usb_num.value= data[0][34-1]
          usb3_supp.value= data[0][35-1]
          usb_typec.value= data[0][36-1]
          thunderbolt_supp.value= data[0][37-1]
          ethernet_supp.value= data[0][38-1]
          hdmi_supp.value= data[0][39-1]
          headphonejack_supp.value = data[0][40-1]
          sdcard_supp.value= data[0][41-1]
          buy_price.value= data[0][42-1]
          sell_price.value= data[0][43-1]
          money.value= data[0][44-1]
          used.value= data[0][45-1]
          print(data[0][45-1])
          en_condition()                    
          condition.value= data[0][46-1]
          quantity.value= data[0][46]
    except :
          info("hi","barcode not found")
def reset():
      data = [['0', 'Choose company', '', 'business', 'intel', 'choose cpu', '0', '', '', 'DDR3', '0', '0', 'Nvidia', '',
                     '', '', 'HDD', '', 'N/A', '', 'N/A', '', '15,6', 'Full HD', '60', '0', '0', '1', '0', '0', '0', 'N/A', '0', '0', '0', '0',
                     '0', '0', '0', '0', '0', '', '', '', '0', 'new', '']]
      barcode.value = ""
      maker.value = data[0][2-1]
      model.value= data[0][3-1]
      catigory.value= data[0][4-1]
      company.value= data[0][5-1]
      chg_comp()
      cpu.value= data[0][6-1]
      cpu_gen= data[0][7-1]
      if(selected_cpu == "intel"):
          gen_intel.value = cpu_gen
      else:
          gen_amd.value = cpu_gen          
      cpu_model.value= data[0][8-1]
      ram_size.value= data[0][9-1]
      ddr.value= data[0][10-1]
      upgradable.value= data[0][11-1]
      integrated.value= data[0][12-1]
      gpu_company.value= data[0][13-1]
      gpu_model.value= data[0][14-1]
      vram.value= data[0][15-1]
      vram_upto.value= data[0][16-1]
      storage_op1.value= data[0][17-1]
      op1_size.value= data[0][18-1]
      storage_op2.value= data[0][19-1]
      op2_size.value= data[0][20-1]
      storage_op3.value= data[0][21-1]
      op3_size.value= data[0][22-1]
      screen_size.value= data[0][23-1]
      screen_resulotion.value= data[0][24-1]
      screen_refresh.value= data[0][25-1]
      touch.value= data[0][26-1]
      deg360.value= data[0][27-1]
      arabic.value= data[0][28-1]
      backlit.value= data[0][29-1]
      rgb_en()
      rgb.value= data[0][30-1]
      numpad.value= data[0][31-1]
      op_sys.value= data[0][32-1]
      odd.value= data[0][33-1]
      Usb_num.value= data[0][34-1]
      usb3_supp.value= data[0][35-1]
      usb_typec.value= data[0][36-1]
      thunderbolt_supp.value= data[0][37-1]
      ethernet_supp.value= data[0][38-1]
      hdmi_supp.value= data[0][39-1]
      headphonejack_supp.value = data[0][40-1]
      sdcard_supp.value= data[0][41-1]
      buy_price.value= data[0][42-1]
      sell_price.value= data[0][43-1]
      money.value= data[0][44-1]
      used.value= data[0][45-1]      
      en_condition()
      op2_na()
      op3_na()
      op_sys.disable()
      condition.value= data[0][46-1]
      quantity.value= data[0][46]
#

#
def about():
    about_window = Window(app, title="about",height =130,width =400)
    text = Text(about_window,text = "this program was made by osama",align="top",size = 10)
    Text(about_window,text = "you can contact me via whatsapp",align="top",size = 10)
    Text(about_window,text = "+963 951736966",align="top",size = 10)
    Text(about_window,text = """please visit my youtube channel "مختبرات اسامة" """,align="top",size = 10)
    Text(about_window,text = "copy right 2021",align="bottom",size = 7)
    text.text_color = "dark blue"
def youtube_visit():
    webbrowser.open("https://www.youtube.com/channel/UC8T0gVxomKWlioQnDDi7RJg/featured")
def ext():
    exit()
##############################################################
def search_advanced():
    adv_srch_win = Window(app,height= 150)
    menubt_box = Box(adv_srch_win,align = "top",border=3)
    maker_menu = tk.Menubutton(menubt_box.tk,text='Manufacturer', activebackground='blue')
    cpu_menu = tk.Menubutton(menubt_box.tk,text='cpu', activebackground='blue')
    ram_menu = tk.Menubutton(menubt_box.tk,text='ram', activebackground='blue')
    gpu_menu = tk.Menubutton(menubt_box.tk,text='gpu', activebackground='blue')
    storage_menu = tk.Menubutton(menubt_box.tk,text='storage', activebackground='blue')
    sql_command = ""
    def set_data():
        global sql_command
        cpu_gen = 1
        if(selected_cpu == "intel"):
              cpu_gen = gen_intel.value
        else:
            cpu_gen =  gen_amd.value    
        sql_command = "select * from specs Where "
        search_a = [[["manufacturer"],[maker.value],[int(srch_manufacturer.get())]],[["laptop_model"],[model.value],[srch_model.get()]]
                    ,[["cpu_family"],[cpu.value],[int(srch_cpu_family.get())]],[["cpu_model"],[cpu_model.value],[int(srch_cpu_model.get())]]
                    ,[["gen"],[cpu_gen],[int(srch_cpu_gen.get())]],[["ram_size"],[ram_size.value],[int(srch_ram_size.get())]]
                    ,[["ddr"],[ddr.value],[int(srch_ddr.get())]],[["upgradable_ram"],[upgradable.value],[int(srch_upgrade.get())]]
                    ,[["gpu_company"],[gpu_company.value],[int(srch_gpu_manufacturer.get())]],[["gpu_model"],[gpu_model.value],[int(srch_gpu_model.get())]]
                    ,[["gpu_vram"],[vram.value],[int(srch_vram.get())]]
                    ,[["storage_option_1_type"],[storage_op1.value],[int(srch_storage_op1_type.get())]],[["storage_option_1_size"],[op1_size.value],[int(srch_storage_op1_size.get())]]
                   ,[["storage_option_2_type"],[storage_op2.value],[int(srch_storage_op2_type.get())]],[["storage_option_2_size"],[op2_size.value],[int(srch_storage_op2_size.get())]]
                       ,[["storage_option_3_type"],[storage_op3.value],[int(srch_storage_op3_type.get())]],[["storage_option_3_size"],[op3_size.value],[int(srch_storage_op3_size.get())]]]               
        for item in range(0,len(search_a),1):
            gen_test = ''.join(map(str,search_a[item][0]))            
            test_var_value = ''.join(map(str,search_a[item][2]))
            test_var_sql = ''.join(map(str,search_a[item][0]))
            test_var_sql += r'= "'
            test_var_sql += ''.join(map(str,search_a[item][1]))
            test_var_sql += r'"'
            if(int(test_var_value) == 1):
                sql_command += test_var_sql
                sql_command += " and "
                if (selected_cpu == "amd" and srch_cpu_company == 1):
                    sql_command += """ cpu_company = "amd" and """
                elif (selected_cpu == "intel" and srch_cpu_company == 1):
                    sql_command += """ cpu_company = "intel" and """
        if (sql_command == "select * from specs Where "):
            sql_command = ""
        else:
            sql_command = sql_command[:-4]
        table(sql_command)    
        ####
    def how_to():
        info("hi","set your data in the main window then select what do you want to search about in advanced search window and click search")    
    button_box =Box(adv_srch_win)
    PushButton(button_box,command = set_data,text = "search",align = "left",padx= 100)
    PushButton(button_box,command = how_to,text = "help",align = "right")    
    #manufacturer    
    maker_menu.menu = tk.Menu(maker_menu, tearoff=0)
    maker_menu["menu"] = maker_menu.menu
    srch_manufacturer = tk.IntVar()
    srch_model = tk.IntVar()
    maker_menu.menu.add_checkbutton(label='Manufacturer', variable=srch_manufacturer)
    maker_menu.menu.add_checkbutton(label='model', variable=srch_model)
    #cpu
    cpu_menu.menu = tk.Menu(cpu_menu, tearoff=0)
    cpu_menu["menu"] = cpu_menu.menu
    srch_cpu_company = tk.IntVar()
    srch_cpu_family = tk.IntVar()
    srch_cpu_model = tk.IntVar()
    srch_cpu_gen = tk.IntVar()
    cpu_menu.menu.add_checkbutton(label='cpu company', variable=srch_cpu_company)
    cpu_menu.menu.add_checkbutton(label='cpu family', variable=srch_cpu_family)
    cpu_menu.menu.add_checkbutton(label='cpu model', variable=srch_cpu_model)
    cpu_menu.menu.add_checkbutton(label='cpu generation', variable=srch_cpu_gen)
    #ram
    ram_menu.menu = tk.Menu(ram_menu, tearoff=0)
    ram_menu["menu"] = ram_menu.menu
    srch_ram_size = tk.IntVar()
    srch_ddr = tk.IntVar()
    srch_upgrade = tk.IntVar()
    ram_menu.menu.add_checkbutton(label='ram size', variable=srch_ram_size)
    ram_menu.menu.add_checkbutton(label='DDRx', variable=srch_ddr)
    ram_menu.menu.add_checkbutton(label='upgadeable', variable=srch_upgrade)
    #gpu
    gpu_menu.menu = tk.Menu(gpu_menu, tearoff=0)
    gpu_menu["menu"] = gpu_menu.menu
    srch_gpu_manufacturer = tk.IntVar()
    srch_gpu_model = tk.IntVar()
    srch_vram = tk.IntVar()
    gpu_menu.menu.add_checkbutton(label='GPU Manufacturer', variable=srch_gpu_manufacturer)
    gpu_menu.menu.add_checkbutton(label='GPU model', variable=srch_gpu_model)
    gpu_menu.menu.add_checkbutton(label='GPU Vram', variable=srch_vram)
    #storage
    storage_menu.menu = tk.Menu(storage_menu, tearoff=0)
    storage_menu["menu"] = storage_menu.menu
    srch_storage_op1_type = tk.IntVar()
    storage_menu.menu.add_checkbutton(label='storage option 1 type', variable=srch_storage_op1_type)
    srch_storage_op1_size = tk.IntVar()
    storage_menu.menu.add_checkbutton(label='storage option 1 size', variable=srch_storage_op1_size)
    srch_storage_op2_type = tk.IntVar()
    storage_menu.menu.add_checkbutton(label='storage option 2 type', variable=srch_storage_op2_type)
    srch_storage_op2_size = tk.IntVar()
    storage_menu.menu.add_checkbutton(label='storage option 2 size', variable=srch_storage_op2_size)
    srch_storage_op3_type = tk.IntVar()
    storage_menu.menu.add_checkbutton(label='storage option 3 type', variable=srch_storage_op3_type)
    srch_storage_op3_size = tk.IntVar()
    storage_menu.menu.add_checkbutton(label='storage option 3 size', variable=srch_storage_op3_size)
    #
    menubt_box.add_tk_widget(maker_menu,align="left")
    menubt_box.add_tk_widget(cpu_menu,align="left")
    menubt_box.add_tk_widget(ram_menu,align="left")
    menubt_box.add_tk_widget(gpu_menu,align="left")
    menubt_box.add_tk_widget(storage_menu,align="left")
    adv_srch_win.show()
###############################################################
def delete_db():
    password = app.question("Hello", "enter password for verification")
    if password == "osama":
        try:
            os.remove("test.db")
        except:
            error("cannot delete db!")    
        info("hi","data base is deleted sucessfully")
    else:
        error("hi","wrong password")
def backup():
    dst = app.question("Hello", "Enter the location you want",initial_value=  r"D:\db" )
    print(dst)
    cwd = os.getcwd()
    if os.path.exists(dst) == False:
        try:
            info("hi","directory not found ..... making one ....")
            os.mkdir(dst)
        except:
            error("hi","cannot make directory")
    try:    
        shutil.copy2(cwd+r'\laptop.db',dst)
        info("hi","database is backed up")
    except :
         error("hi","cannot back up the data base!")
         raise

def open_db_dir():
    webbrowser.open(os.getcwd())

def get_time(type=""):
    global year , month , day , hour , minutes , sec , conntected_to_internet
    try:
        w = RequestTimefromNtp()
        #time.struct_time(tm_year=2021, tm_mon=10, tm_mday=2, tm_hour=17, tm_min=30, tm_sec=19, tm_wday=5, tm_yday=275, tm_isdst=-1)
        year = w[0]
        month = w[1]
        day = w[2]
        hour = w[3]
        minutes = w[4]
        sec = w[5]
        week_day = week_days[w[6]]
        conntected_to_internet = True
    except Exception as e:
        conntected_to_internet = False
        current_time = datetime.datetime.now()          
        year = current_time.year
        month  = current_time.month
        day = current_time.day
        week_day = week_days[current_time.weekday()]
        hour = current_time.hour 
        minutes =  current_time.minute 
        sec  = current_time.second
        if type != "silent":
            info("hi",f""" we couldnt get to the internet to have the time so we will \n use the internal clock make sure that it is correct so you dont have    error in your data base
            \n \n  current time     {year}/{month}/{day} {week_day}  {hour}:{minutes}:{sec}""")
    except:
        if type != "silent":
            info("hi","couldnt get the right time....")   
        exit()
    #print(f"{year}/{month}/{day} {week_day}  {hour}:{minutes}:{sec}")
def trial_vesion(end):
    get_time("silent")
    if(end <= year):
        error("hi","trail version ended plase call dev osama breman to re-activate \n 0951736966 whatsapp only")
        exit()
    elif(conntected_to_internet == False):
        error("hi","please connect to internet to check your version stats...")    
        exit()
def add_value_cpu_intel():
    global cpus_intel
    global intel_list
    global list_window
    if(add.value != ""):
        intel_list.append(add.value)
    else:
        error("hi","cant add empty value")   
        list_window.focus()
    add.value = ""    
    print(intel_list.items)
def remove_value_intel_cpu():
    global cpus_intel
    global intel_list
    if intel_list.value != None:
        for i in intel_list.value:
            intel_list.remove(i)   
    else:
        info("hi","No item(s) selected!")
        list_window.focus() 
def save_value_intel_cpu():
    global cpus_intel
    global intel_list
    db.execute("delete from intel_cpus") 
    db.commit()
    db.execute(""" insert into intel_cpus values ("choose cpu") """)
    db.commit()
    for i in intel_list.items:
       db.execute(f"""insert into intel_cpus values ("{i}")""")
       db.commit()              
def edit_intel_cpus():
    global cpus_intel
    global list_window
    list_window =  Window(app,width= 500 ,height= 500)
    lstbox = Box(list_window,align= "left",border= 2,height=500,width=200)
    global intel_list
    intel_list = ListBox(lstbox, items=cpus_intel[1:],scrollbar=True,height=500,width=200,multiselect=True)
    Box(list_window,align="left",width=90,height=500)
    add_box = Box(list_window,align="left")
    global add 
    add = TextBox(add_box,align= "top",width=15)
    add_button = PushButton(add_box,align="top",text = "add value",command = add_value_cpu_intel)
    delete_button = PushButton(add_box,align="top",text = "delet selection",command=remove_value_intel_cpu)
    save_button = PushButton(add_box,align="top",text = "save changes",command=save_value_intel_cpu)
    #add.tk.config(pady = 10) 
    
get_time()
init_cpu_data()
get_cpu_data()
#trial_vesion(2022)
Text(app,text ="Laptop Data Base -Osmax- Verison 0.2",align = "top",width="fill")
############################################################################################################
############################################################################################################
############################################################################################################
#menu
menu = MenuBar(app,toplevel = ["file","edit","search","advanced","about"]
               ,options=[
                   [["open db directory",open_db_dir],["exit",ext]],
                   [["edit intel cpus",edit_intel_cpus]],
                   [["search by barcode",search_barcode],["show all devices",search],["advanced search",search_advanced]],
                   [["delete data base",delete_db],["backup data base",backup]],
                   [["about",about],["visit my channel",youtube_visit]] ])
#manufacturer
Manufacture = Box(app,align ="top",width="fill",border = True)
Text(Manufacture,text ="laptop manfacturer  ", align="left")
maker = Combo(Manufacture,align= "left" ,options=brand_options,command = en_model)
Text(Manufacture,text ="laptop model  ", align="left")
model = TextBox(Manufacture,align="left",width = 15,enabled=True)
Text(Manufacture,align= "left",text = " Catigory : ")
catigory = Combo(Manufacture,align="left",options=["business","gaming","2 in 1","slim"])
#cpu
cpu_box = Box(app,align = "top",border = True,width="fill")
Text(cpu_box,"cpu model : ",align="left",size=10)
company = ButtonGroup(cpu_box,options=["intel","amd"],horizontal = True,align="left",command= chg_comp)
cpu = Combo(cpu_box,align="left",options=cpus,selected="choose cpu",enabled=False,command = hi)
Text(cpu_box,"gen",align = "left",size = 10)
gen_intel = Slider(cpu_box,align = "left",start=1,end=11,height=10,command=chk_ddr)
gen_intel.text_size= 8
gen_amd = Slider(cpu_box,align = "left",start=1,end=4,height=10,visible=False,command=chk_ddr)
gen_amd.text_size= 8
Text(cpu_box,"Model ",align="left",size=10)
cpu_model = TextBox(cpu_box,align="left",width=20)
cpu_model.text_size = 10
#ram
ram_box = Box(app,align = "top",border = True , width= "fill")
Text(ram_box,align = "left",text = "RAM : ")
ram_size = TextBox(ram_box,align = "left",width=3,command = chk_val_ram)
Text(ram_box,"   ",align = "left")
ddr = Combo(ram_box,align="left",options = ["DDR1","DDR2","DDR3","DDR4","DDR5"],selected="DDR3")
Text(ram_box,"   ",align= "left")
upgradable = CheckBox(ram_box,text = "Upgradable",align = "left")
#GPU
gpu_box = Box(app,align = "top",width="fill",border= True)
Text(gpu_box,"GPU : ",align = "left")
integrated = CheckBox(gpu_box,align="left",text = "integrated", command = intergrated)
gpu_company = ButtonGroup(gpu_box,align = "left" , options= ["Nvidia","amd","intel"], horizontal= True)
Text(gpu_box,align="left",text = " ")
gpu_model = TextBox(gpu_box,align= "left")
gpu_model.text_size = 10
Text(gpu_box,align = "left",text = " VRAM : ")
vram = TextBox(gpu_box,align= "left",width= 3,command = chk_val_vram)
Text(gpu_box,align="left",text = " Up to ")
vram_upto = TextBox(gpu_box,align= "left",width= 3,command = chk_val_vram_upto)
#Storage
storage_box = Box(app,align="top",border = True ,width="fill")
Text(storage_box,align= "left",text = "Storage : ")
optxt = Text(storage_box,align= "left",text = "Option 1 ")
optxt.text_size = 9
storage_op1 = Combo(storage_box,align = "left",options=["HDD","SATA SSD","M.2","NVME","OPTANE"])
Text(storage_box,align="left",text = " ")
op1_size = TextBox(storage_box,align = "left" , width = 4 , command = chk_val_op1)

optxt = Text(storage_box,align= "left",text = " Option 2 ")
optxt.text_size = 9
storage_op2 = Combo(storage_box,align = "left",options=["HDD","SATA SSD","M.2","NVME","OPTANE","N/A"],command = op2_na,selected = "N/A")
Text(storage_box,align="left",text = " ")
op2_size = TextBox(storage_box,align = "left" , width = 4 , command = chk_val_op2,enabled=False)

optxt = Text(storage_box,align= "left",text = " Option 3 ")
optxt.text_size = 9
storage_op3 = Combo(storage_box,align = "left",options=["HDD","SATA SSD","M.2","NVME","OPTANE","N/A"],command = op3_na,selected = "N/A")
Text(storage_box,align="left",text = " ")
op3_size = TextBox(storage_box,align = "left" , width = 4 , command = chk_val_op3,enabled=False)
#Screen
screen_box = Box(app,align = "top",border = True , width = "fill")
Text(screen_box,align = "left",text = "screen size : ",size = 13)
screen_size = Combo(screen_box,align="left",options = ["10,1","11,6","12.5","14,0","15,6","16,1","17,3"],selected = "15,6")
Text(screen_box,align = "left",text = " Resulotion ")
screen_resulotion = Combo(screen_box,align="left",options=["HD","HD+","Full HD","QHD","2K","4K"],selected = "Full HD")
Text(screen_box,align = "left",text = " Refresh Rate ")
screen_refresh = Combo(screen_box,align="left",options=["60","90","120","144","240"],selected = "60")
Text(screen_box,align = "left",text = "  ")
touch = CheckBox(screen_box,align = "left",text = "touch")
Text(screen_box,align = "left",text = " ")
deg360 = CheckBox(screen_box,align = "left",text = "360°")
#keyboard combo
keyboard_combo = Box(app,align = "top",width = "fill",border = True)
keyboard = Box(keyboard_combo,align = "left",border = True)
Text(keyboard,align = "left",text = "KeyBoard : ")
arabic = CheckBox(keyboard,align = "left",text = "arabic")
arabic.toggle()
backlit = CheckBox(keyboard,align = "left",text = "backlit",command = rgb_en)
rgb = CheckBox(keyboard,align = "left",text = "rgb",enabled=False)
numpad = CheckBox(keyboard,align = "left",text = "numpad")
#os
osx = Box(keyboard_combo,align="left",width= "fill",border=True)
Text(osx,align = "left",text = "OS : ")
original = CheckBox(osx,align = "left",text = "original",command = en_os)
op_sys = Combo(osx,align="left",options=["win 10","win 8.1","win 7","win xp","Ubuntu","Chrome OS","N/A"],selected="N/A",enabled=False)
#odd
odd =CheckBox(osx,align="left",text = "Optical Drive")
#ports
ports_box = Box(app,align = "top",width = "fill",border= True)
Text(ports_box,align= "left",text = "USB ports")
Usb_num = Slider(ports_box,align="left",start=0,end = 4,height=10)
Usb_num.text_size= 8
usb3_supp = CheckBox(ports_box,align="left",text = "Usb 3")
usb_typec = CheckBox(ports_box,align="left",text  = "Type C")
thunderbolt_supp = CheckBox(ports_box,align="left",text ="ThunderBolt")
ethernet_supp = CheckBox(ports_box,align="left",text ="Ethernet")
hdmi_supp = CheckBox(ports_box,align="left",text ="HDMI")
headphonejack_supp = CheckBox(ports_box,align="left",text ="Headphone jack")
sdcard_supp = CheckBox(ports_box,align="left",text ="sd card")
#price
price_box = Box(app,align="top",border=True,width = "fill")
Text(price_box,align="left",text = "Price : ",size = 20)
Text(price_box,align="left",text = "buy ",size = 15)
buy_price = TextBox(price_box,align="left",width = 9,command = regulate_buy)
Text(price_box,align="left",text = " sell ",size = 15)
sell_price = TextBox(price_box,align="left",width = 9,command = regulate_sell)
buy_price.text_size = 15
sell_price.text_size = 15
Text(price_box,align="left",text = "  Revenue: ")
money = Text(price_box,align="left")
used = CheckBox(price_box,align= "left",text = "used",command= en_condition)
condition = Combo(price_box,align="left",options=["perfect","good","normal","bad","open box","new"],enabled=False,selected = "new")
#options
option_box = Box(app,align="top",border = True , width= "fill")
Text(option_box,align="left",text ="Quantinty ")
quantity = TextBox(option_box,align="left",width = 4,command = regulate_qt)
Text(option_box,align= "left",text = "Barcode ")
barcode = TextBox(option_box,align="left",width = 15)
Text(option_box,align= "left",text = "   ")
save = PushButton(option_box,align = "left",text = "Save",command = save)
save.bg = "cyan"
#save.tk.config(bd = 5)
search = PushButton(option_box,align = "left",text = "Search all devices",command=search)
search.bg = "lime"
search_barcod = PushButton(option_box,align = "left",text = "Search by barcode",command=search_barcode)
search_barcod.bg = "red"
reset_boxes =  PushButton(option_box,align = "left",text = "reset all",command=reset)
reset_boxes.bg = "yellow"
app.display()