import tkinter
from tkinter import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import mysql.connector
from datetime import date, time, datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import re
import xlsxwriter
import os
import subprocess

global new
new = 0
global check
check = 0
global update
update = []
global d
global select

class Autocomplete(Entry):

    def __init__(self, lista, *args, **kwargs):
        self.lb2 = Listbox()
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var2 = self["textvariable"]
        if self.var2 == '':
            self.var2 = self["textvariable"] = StringVar()

        self.var2.trace('w', self.changed2)
        self.bind("<Right>", self.selection2)
        self.bind("<Return>", self.selection2)
        self.bind("<Up>", self.up2)
        self.bind("<Down>", self.down2)

        self.lb2_up = False

    def changed2(self, name2, index2, mode2):
        if self.var2.get() == '':
            self.lb2.destroy()
            Inventory.checkin(obj)
            self.lb2_up = False
        else:
            words = self.comparison2()
            if words:
                if not self.lb2_up:
                    global add
                    if new == 1:
                        self.lb2 = Listbox(addnewform1, relief=SOLID)
                    else:
                        self.lb2 = Listbox(addnewform, relief=SOLID)
                    self.lb2.bind("<Button-1>", self.selection2)
                    self.lb2.bind("<Right>", self.selection2)
                    self.lb2.bind("<Return>", self.selection2)
                    if select == 6:
                        self.lb2.place(x=287, y=156, width=201)
                    else:
                        self.lb2.place(x=275, y=106, width=201)
                    self.lb2_up = True
                self.lb2.delete(0, END)
                for w in words:
                    self.lb2.insert(END, w)
            else:
                if self.lb2_up:
                    self.lb2.destroy()
                    self.lb2_up = False

    def selection2(self, event2):

        if self.lb2_up:
            self.var2.set(self.lb2.get(ACTIVE))
            self.lb2.destroy()
            self.lb2_up = False
            self.icursor(END)
            d.execute("select Address,Bill_no,Amount,GST,Total_Items from stock where Item_name=%s", [val])
            for i in d:
                for j in range(len(i)):
                    total = i[j]
                    update.append(total)
            Inventory.Updation(obj)

    def up2(self, event):
        if self.lb2_up:
            if self.lb2.curselection() == ():
                index = '0'
            else:
                index = self.lb2.curselection()[0]
            if index != '0':
                self.lb2.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb2.selection_set(first=index)
                self.lb2.activate(index)

    def down2(self, event2):
        if self.lb2_up:
            if self.lb2.curselection() == ():
                index = '-1'
            else:
                index = self.lb2.curselection()[0]
            if index != END:
                self.lb2.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb2.selection_set(first=index)
                self.lb2.activate(index)

    def comparison2(self):
        global check
        check = 1
        if self.var2.get() == "":
            pass
        elif self.var2.get() != "":
            global pattern
            pattern = re.compile(self.var2.get().lower() + '.*')
            global val
            val = str(self.var2.get().lower())
            return [w for w in self.lista if re.match(pattern, w)]


class AutocompleteEntry(Entry):

    def __init__(self, lista, *args, **kwargs):
        self.lb = Listbox()
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    global add
                    self.lb = Listbox(relief=SOLID)
                    self.lb.bind("<Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.bind("<Return>", self.selection)
                    self.lb.place(x=9, y=100, width=116)
                    self.lb_up = True
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '-1'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        global check
        check = 1
        if self.var.get() == "":
            pass
        elif self.var.get() != "":
            pattern = re.compile('.*' + self.var.get().lower() + '.*')
            global val
            val = str(self.var.get().lower())

            return [w for w in self.lista if re.match(pattern, w)]


class Inventory(AutocompleteEntry, Autocomplete):

    def __init__(self, main):
        # ================================== Start MYSQL =====================================
        # try:subprocess.Popen(r'C:\xampp\mysql_start.bat')
        # except:
        #     try:subprocess.Popen(r'D:\xampp\mysql_start.bat')
        #     except:
        #         try:subprocess.Popen(r'E:\xampp\mysql_start.bat')
        #         except:
        #             try:subprocess.Popen(r'F:\xampp\mysql_start.bat')
        #             except:
        #                 try:subprocess.Popen(r'G:\xampp\mysql_start.bat')
        #                 except:
        #                     try:subprocess.Popen(r'H:\xampp\mysql_start.bat')
        #                     except:
        #                         try:subprocess.Popen(r'I:\xampp\mysql_start.bat')
        #                         except:pass
        try:subprocess.Popen(r'\xampp\mysql_start.bat')
        except:pass
        try:subprocess.Popen(r'D:\xampp\mysql_start.bat')
        except:pass
        try:subprocess.Popen(r'E:\xampp\mysql_start.bat')
        except:pass
        try:subprocess.Popen(r'F:\xampp\mysql_start.bat')
        except:pass
        try:subprocess.Popen(r'G:\xampp\mysql_start.bat')
        except:pass
        try:subprocess.Popen(r'H:\xampp\mysql_start.bat')
        except:pass
        try:subprocess.Popen(r'I:\xampp\mysql_start.bat')
        except:pass
        try:os.system("TASKKILL /F /IM cmd.exe")
        except:pass
        # ==================================database connection===============================
        # os.startfile(r'E:\xampp\mysql_start.bat')
        # self.c = DbConnection().g
        # os.system("taskkill -f /pid " + "cmd.exe")
        # self.d = self.c.cursor()
        # 864 1536
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        # ======================================Main(root)====================================
        self.style = ttk.Style()
        self.select = 0
        self.main = main
        # self.main.geometry("1366x770")
        self.main.geometry(str(self.screen_width) +"x"+ str(self.screen_height))
        self.main.state("zoomed")
        self.main.title("Inventory Management System")
        root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='project_icon.jpg'))
        # =======================================variables====================================
        global select
        select = self.select
        global check
        check = 0


    # ============================================== Main screens (Layouts)==================================================

    def first_screen(self):
        self.screen1 = Frame(self.main, bg='white')
        self.screen1.pack()
        label = Label(self.screen1, text='INVENTORY  MANAGENMENT', bg="cyan", width='300', height=3,font=('Copperplate Gothic Bold', 25, 'bold'))
        label.pack()
        space_label = Label(self.screen1, text="", bg='white')
        if self.screen_width > 1600:
            space_label.pack(pady=20)
        else:
            space_label.pack(pady=5)
        # space_label = Label(self.screen1, text="", bg='white')
        # space_label.pack(pady=10)
        img = Image.open("gne.png")
        photo = ImageTk.PhotoImage(img)
        imga = Label(self.screen1, image=photo, bd=0)
        imga.image = photo
        imga.pack()
        button = Button(self.screen1, text='LOGIN', activeforeground='white', bd=3, activebackground='black', bg='cyan',height='1', width='12', font=("Copperplate Gothic bold", 16, "bold"), command=self.Login_screen,relief=SOLID)
        button.pack(pady=15)
        space_label = Label(self.screen1, text="", bg='white')
        space_label.pack(pady=800)

    # def Databaseconnection(self):
    #
    #     self.Login_screen()

    def Login_screen(self):
        self.screen1.destroy()
        self.screen2 = Frame(self.main, bg='white')
        self.screen2.pack(side=TOP)
        global lbl_result
        menubar = Menu(self.main)
        self.filemenu = Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.Exit)
        menubar.add_cascade(label="File", menu=self.filemenu)
        self.main.config(menu=menubar)
        self.username = StringVar()
        self.password = StringVar()
        login = Label(self.screen2, text="LOGIN", bg="cyan", height='2', width='770',font=('Copperplate Gothic Bold', 25, 'bold'))
        login.pack()
        space_label = Label(self.screen2, text="", bg='white')
        space_label.pack(pady=20)
        name_label = Label(self.screen2, text="USERNAME", bg='white', height="2", width='60',font=('Copperplate Gothic Bold', 20))
        name_label.pack()
        self.username_entry = Entry(self.screen2, textvariable=self.username, font=('arial', 20), relief=SOLID, bd=2)
        self.username_entry.focus()
        self.username_entry.pack()
        password_label = Label(self.screen2, text="PASSWORD", bg='white', height='2', width='60',font=('Copperplate Gothic Bold', 20))
        password_label.pack()
        self.password_entry = Entry(self.screen2, textvariable=self.password, show='*', font=('arial', 20),relief=SOLID, bd=2)
        self.password_entry.pack()
        button = Button(self.screen2, text="Enter", font=("Copperplate Gothic Bold", 15, "bold"), bd=3, width='12',height='1', command=self.LogIn, relief=SOLID, activebackground='black',activeforeground='white')
        button.pack(pady=60)
        lbl_result = Label(self.screen2, text="", font=('Copperplate Gothic Bold', 18, 'bold'), bg='white')
        lbl_result.pack()
        space_labell = Label(self.screen2, text="", bg='white', height=30)
        space_labell.pack(pady=20)
        # ======================================Database connection=============================
        self.c = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="gndpcstock")
        self.d = self.c.cursor()
        global d
        d = self.c.cursor()
        # ======================================================================================


    def third_screen(self):
        #======================================variables=========================================
        self.ITEM_NAME = StringVar()
        self.BILL_NO = IntVar()
        self.ADDRESS = StringVar()
        self.TOTAL_AMOUNT = IntVar()
        self.GST = IntVar()
        self.TOTAL_ITEMS = IntVar()
        self.ISSUE = IntVar()
        self.BALANCE = IntVar()
        self.SEARCH = StringVar()
        self.DEPT_NAME = StringVar()
        self.ITEM_NAME = StringVar()
        self.balan = StringVar()
        self.ISS = IntVar()
        self.ITEM_PIECES = IntVar()
        self.NAME = StringVar()
        self.PHONE_NO = IntVar()
        self.dropdown = StringVar(root)
        #========================================================================================

        global add
        add = '0'
        self.screen2.destroy()
        global tree
        self.stock1 = Frame(self.main,bg="cyan")
        self.stock1.pack()
        self.select = 1
        global select
        select = self.select
        self.d.execute("SELECT Item_name from stock where Deleted_date=''")
        global lista
        lista = []
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        TopViewForm = Frame(self.stock1, width=600, bd=1, relief=SOLID,bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.stock1, width=600,bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.stock1, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="STOCK", font=('Copperplate Gothic Bold', 20), width=600,bg="cyan")
        lbl_text.pack(fill=X,pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"),bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        global search
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12,"bold"),relief=GROOVE, activebackground='black',activeforeground='white',bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12,"bold"),relief=GROOVE, activebackground='black',activeforeground='white',bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        # btn_add = Button(LeftViewForm, text="Add", command=self.ShowAddNew, font=("Copperplate Gothic Light", 12))
        # btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete, font=("Copperplate Gothic Light", 12,"bold"),relief=GROOVE, activebackground='black',activeforeground='white',bg='white')
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_print = Button(LeftViewForm, text="Print", font=("Copperplate Gothic Light", 12,"bold"),relief=GROOVE, activebackground='black',activeforeground='white',bg='white', command=self.choice)
        btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar",background="cyan",troughcolor="black",highlightcolor="green",highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar",background="cyan",troughcolor="black",highlightcolor="green",highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13,"bold"),background="black",foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S.No", "Date", "Item Name", "Total Items", "Issue", "Balance", "Address", "Bill No.", "Amount", "GST","GST Amount", "Without GST"), selectmode="extended", height=100,yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S.No', text="S.No", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Item Name', text="Item Name", anchor=W)
        tree.heading('Total Items', text="Total Items", anchor=W)
        tree.heading('Issue', text="Issue", anchor=W)
        tree.heading('Balance', text="Balance", anchor=W)
        tree.heading('Address', text="Firm Name", anchor=W)
        tree.heading('Bill No.', text="Bill No.", anchor=W)
        tree.heading('Amount', text="Amount", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('GST Amount', text="GST Amount", anchor=W)
        tree.heading('Without GST', text="Without GST", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=80)
        tree.column('#2', stretch=NO, minwidth=0, width=100)
        tree.column('#3', stretch=NO, minwidth=0, width=220)
        tree.column('#4', stretch=NO, minwidth=0, width=170)
        tree.column('#5', stretch=NO, minwidth=0, width=140)
        tree.column('#6', stretch=NO, minwidth=0, width=150)
        tree.column('#7', stretch=NO, minwidth=0, width=320)
        tree.column('#8', stretch=NO, minwidth=0, width=170)
        tree.column('#9', stretch=NO, minwidth=0, width=180)
        tree.column('#10', stretch=NO, minwidth=0, width=120)
        tree.column('#11', stretch=NO, minwidth=0, width=170)
        tree.column('#12', stretch=NO, minwidth=0, width=180)
        tree.pack()
        # ================================= Menubar ===========================================
        menubar = Menu(self.main)
        self.filemenu = Menu(menubar, tearoff=0)
        self.filemenu2 = Menu(menubar, tearoff=0)
        self.filemenu3 = Menu(menubar, tearoff=0)
        # self.filemenu4 = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=self.filemenu)
        menubar.add_cascade(label="Inventory", menu=self.filemenu2)
        menubar.add_cascade(label="Deleted", menu=self.filemenu3)
        self.filemenu.add_command(label="About", command=self.About)
        self.filemenu.add_command(label="Logout", command=self.LogOut)
        self.filemenu.add_command(label="Exit", command=self.Exit)
        self.filemenu2.add_command(label="Stock", command=self.Stock)
        self.filemenu2.add_command(label="Asset", command=self.Asset)
        self.filemenu2.add_command(label="Stationary", command=self.Stationary)
        self.filemenu2.add_command(label="Conty", command=self.County)
        self.filemenu2.add_command(label="Issue", command=self.Issue)
        self.filemenu3.add_command(label="Deleted Items", command=self.Deleted_Items)
        self.filemenu3.add_command(label="Deleted Bills", command=self.Deleted_Bills)
        self.filemenu3.add_command(label="Deleted Issued", command=self.Deleted_Issued)
        # self.filemenu4.add_command(label="Analytics", command=self.bar_graph)
        # menubar.add_cascade(label="More", menu=self.filemenu4)
        self.main.config(menu=menubar)
        self.DisplayData()


    # =============================================== LogIn , logOut & Exit =================================================

    def LogIn(self):
        if self.username_entry.get == "" or self.password_entry.get() == "":
            lbl_result.config(text="Please complete the required field!", fg="red")
        else:
            if self.username_entry.get() == 'ADMIN' and self.password_entry.get() == '12345678':
                self.screen2.destroy()
                self.third_screen()
                self.username.set("")
                self.password.set("")

            else:
                lbl_result.config(text="Invalid username or password", fg="red")
                self.username.set("")
                self.password.set("")


    def LogOut(self):
        global admin_id
        result = tkMessageBox.askquestion('Inventory Management System', 'Are you sure you want to Logout?',
                                          icon="warning")
        if result == 'yes':
            admin_id = ""
            root.deiconify()
            if self.select == 1:
                self.stock1.destroy()
            if self.select == 2:
                self.asset.destroy()
            if self.select == 3:
                self.stationary.destroy()
            if self.select == 4:
                self.stock.destroy()
            if self.select == 5:
                self.conty.destroy()
            if self.select == 6:
                self.issue.destroy()
            if self.select == 7:
                self.DeletedData.destroy()
            if self.select == 8:
                self.Deleted_bills.destroy()
            if self.select == 9:
                self.Deleted_issued.destroy()
            if self.select == 10:
                self.canvas.destroy()
                self.about.destroy()
            self.Login_screen()


    def Exit(self):
        result = tkMessageBox.askquestion('Inventory Management System', 'Are you sure you want to exit?',icon="warning")
        if result == 'yes':
            root.destroy()
            exit()

    # ==================================================== Screens (layouts) ==========================================================

    def Stock(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 4
        global select
        select = self.select
        global lista
        lista = []
        self.d.execute("SELECT Item_name from stock where Deleted_date=''")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        global tree
        self.stock = Frame(self.main)
        self.stock.pack()
        TopViewForm = Frame(self.stock, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.stock, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.stock, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="STOCK", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        global search
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        # btn_add = Button(LeftViewForm, text="Add", command=self.ShowAddNew, font=("Copperplate Gothic Light", 12))
        # btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_print = Button(LeftViewForm, text="Print", font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white', command=self.choice)
        btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S.No", "Date", "Item Name", "Total Items", "Issue", "Balance", "Address", "Bill No.", "Amount", "GST","GST Amount", "Without GST"), selectmode="extended", height=100, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S.No', text="S.No", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Item Name', text="Item Name", anchor=W)
        tree.heading('Total Items', text="Total Items", anchor=W)
        tree.heading('Issue', text="Issue", anchor=W)
        tree.heading('Balance', text="Balance", anchor=W)
        tree.heading('Address', text="Firm Name", anchor=W)
        tree.heading('Bill No.', text="Bill No.", anchor=W)
        tree.heading('Amount', text="Amount", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('GST Amount', text="GST Amount", anchor=W)
        tree.heading('Without GST', text="Without GST", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=80)
        tree.column('#2', stretch=NO, minwidth=0, width=100)
        tree.column('#3', stretch=NO, minwidth=0, width=210)
        tree.column('#4', stretch=NO, minwidth=0, width=170)
        tree.column('#5', stretch=NO, minwidth=0, width=130)
        tree.column('#6', stretch=NO, minwidth=0, width=140)
        tree.column('#7', stretch=NO, minwidth=0, width=320)
        tree.column('#8', stretch=NO, minwidth=0, width=170)
        tree.column('#9', stretch=NO, minwidth=0, width=180)
        tree.column('#10', stretch=NO, minwidth=0, width=100)
        tree.column('#11', stretch=NO, minwidth=0, width=170)
        tree.column('#12', stretch=NO, minwidth=0, width=180)
        tree.pack()
        self.DisplayData()

    def Stationary(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 3
        global select
        select = self.select
        global lista
        lista = []
        self.d.execute("SELECT Item_name from stock where Deleted_date ='' and department='stationary'")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)

        global tree
        self.stationary = Frame(self.main)
        self.stationary.pack()
        TopViewForm = Frame(self.stationary, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.stationary, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.stationary, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="STATIONARY", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        global search
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_add = Button(LeftViewForm, text="Add", command=self.ShowAddNew, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_print = Button(LeftViewForm, text="Print", font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white', command=self.choice)
        btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S.No", "Date", "Item Name", "Total Items", "Issue", "Balance", "Address", "Bill No.", "Amount", "GST","GST Amount", "Without GST"), selectmode="extended", height=100, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S.No', text="S.No", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Item Name', text="Item Name", anchor=W)
        tree.heading('Total Items', text="Total Items", anchor=W)
        tree.heading('Issue', text="Issue", anchor=W)
        tree.heading('Balance', text="Balance", anchor=W)
        tree.heading('Address', text="Firm Name", anchor=W)
        tree.heading('Bill No.', text="Bill No.", anchor=W)
        tree.heading('Amount', text="Amount", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('GST Amount', text="GST Amount", anchor=W)
        tree.heading('Without GST', text="Without GST", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=80)
        tree.column('#2', stretch=NO, minwidth=0, width=100)
        tree.column('#3', stretch=NO, minwidth=0, width=210)
        tree.column('#4', stretch=NO, minwidth=0, width=170)
        tree.column('#5', stretch=NO, minwidth=0, width=130)
        tree.column('#6', stretch=NO, minwidth=0, width=140)
        tree.column('#7', stretch=NO, minwidth=0, width=320)
        tree.column('#8', stretch=NO, minwidth=0, width=170)
        tree.column('#9', stretch=NO, minwidth=0, width=180)
        tree.column('#10', stretch=NO, minwidth=0, width=100)
        tree.column('#11', stretch=NO, minwidth=0, width=170)
        tree.column('#12', stretch=NO, minwidth=0, width=180)
        tree.pack()
        self.DisplayData()

    def Asset(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 2
        global select
        select = self.select

        global lista
        lista = []
        self.d.execute("SELECT Item_name from stock where Deleted_date ='' and department='asset'")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        global tree
        self.asset = Frame(self.main)
        self.asset.pack()
        TopViewForm = Frame(self.asset, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.asset, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.asset, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="ASSET", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        global search
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_add = Button(LeftViewForm, text="Add", command=self.ShowAddNew, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_print = Button(LeftViewForm, text="Print", font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white', command=self.choice)
        btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S.No", "Date", "Item Name", "Total Items", "Issue", "Balance", "Address", "Bill No.", "Amount", "GST","GST Amount", "Without GST"), selectmode="extended", height=100, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S.No', text="S.No", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Item Name', text="Item Name", anchor=W)
        tree.heading('Total Items', text="Total Items", anchor=W)
        tree.heading('Issue', text="Issue", anchor=W)
        tree.heading('Balance', text="Balance", anchor=W)
        tree.heading('Address', text="Firm Name", anchor=W)
        tree.heading('Bill No.', text="Bill No.", anchor=W)
        tree.heading('Amount', text="Amount", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('GST Amount', text="GST Amount", anchor=W)
        tree.heading('Without GST', text="Without GST", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=80)
        tree.column('#2', stretch=NO, minwidth=0, width=100)
        tree.column('#3', stretch=NO, minwidth=0, width=210)
        tree.column('#4', stretch=NO, minwidth=0, width=170)
        tree.column('#5', stretch=NO, minwidth=0, width=130)
        tree.column('#6', stretch=NO, minwidth=0, width=140)
        tree.column('#7', stretch=NO, minwidth=0, width=320)
        tree.column('#8', stretch=NO, minwidth=0, width=170)
        tree.column('#9', stretch=NO, minwidth=0, width=180)
        tree.column('#10', stretch=NO, minwidth=0, width=100)
        tree.column('#11', stretch=NO, minwidth=0, width=170)
        tree.column('#12', stretch=NO, minwidth=0, width=180)
        tree.pack()
        self.DisplayData()

    def County(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 5
        global select
        select = self.select

        global lista
        lista = []
        self.d.execute("SELECT Item_name from conty where Deleted_date ='' ")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        global tree
        self.conty = Frame(self.main)
        self.conty.pack()
        TopViewForm = Frame(self.conty, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.conty, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.conty, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="CONTY", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        global search
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_add = Button(LeftViewForm, text="Add Bill", command=self.county_pay, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_print = Button(LeftViewForm, text="Print", font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white', command=self.choice)
        btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S_No", "Date", "Item name", "Quantity", "Shop address", "Bill no.", "Cost Without GST", "GST", "Total Cost"),selectmode="extended", height=100, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S_No', text="S.No", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Item name', text="Item Name", anchor=W)
        tree.heading('Quantity', text="Quantity", anchor=W)
        tree.heading('Shop address', text="Firm Name", anchor=W)
        tree.heading('Bill no.', text="Bill No.", anchor=W)
        tree.heading('Cost Without GST', text="Cost Without GST", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('Total Cost', text="Total Cost", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=100)
        tree.column('#2', stretch=NO, minwidth=0, width=160)
        tree.column('#3', stretch=NO, minwidth=0, width=280)
        tree.column('#4', stretch=NO, minwidth=0, width=180)
        tree.column('#5', stretch=NO, minwidth=0, width=390)
        tree.column('#6', stretch=NO, minwidth=0, width=170)
        tree.column('#7', stretch=NO, minwidth=0, width=290)
        tree.column('#8', stretch=NO, minwidth=0, width=170)
        tree.column('#9', stretch=NO, minwidth=0, width=190)
        tree.pack()
        self.DisplayData()

    def Issue(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 6
        global select
        select = self.select
        # ============================For search on main screen=========================
        global lista
        lista = []
        self.d.execute("SELECT Dept_Name,Item_Name from issue where Deleted_date ='' ")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        # ===========================For search add Item screen==========================
        global lista2
        lista2 = []
        self.d.execute("SELECT Item_name from stock where Deleted_date ='' ")
        for i in self.d:
            for j in range(len(i)):
                total2 = i[j]
                lista2.append(total2)
        # ==============================================main screen==========================
        global tree
        self.issue = Frame(self.main)
        self.issue.pack()
        TopViewForm = Frame(self.issue, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.issue, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.issue, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="ISSUE", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        global search
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_add = Button(LeftViewForm, text="Issue", command=self.ShowAddNew, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_delete = Button(LeftViewForm, text="Delete", command=self.Delete, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_print = Button(LeftViewForm, text="Print", font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white', command=self.choice)
        btn_print.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S_NO", "Date", "Time", "Dept_Name", "Item_Name", "Item_pieces", "Name", "Phone_No"), selectmode="extended",height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S_NO', text="S_NO", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Time', text="Time", anchor=W)
        tree.heading('Dept_Name', text="Dept_Name", anchor=W)
        tree.heading('Item_Name', text="Item_Name", anchor=W)
        tree.heading('Item_pieces', text="Item_pieces", anchor=W)
        tree.heading('Name', text="Name", anchor=W)
        tree.heading('Phone_No', text="Phone_No", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=100)
        tree.column('#2', stretch=NO, minwidth=0, width=170)
        tree.column('#3', stretch=NO, minwidth=0, width=190)
        tree.column('#4', stretch=NO, minwidth=0, width=380)
        tree.column('#5', stretch=NO, minwidth=0, width=300)
        tree.column('#6', stretch=NO, minwidth=0, width=200)
        tree.column('#7', stretch=NO, minwidth=0, width=270)
        tree.column('#8', stretch=NO, minwidth=0, width=260)
        tree.pack()
        self.DisplayData()

    def Deleted_Items(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 7
        global select
        select = self.select

        global lista
        lista = []
        self.d.execute("SELECT Item_name from stock where Deleted_date !=''")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)

        global tree
        self.DeletedData = Frame(self.main)
        self.DeletedData.pack()
        TopViewForm = Frame(self.DeletedData, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.DeletedData, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.DeletedData, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="DELETED  ITEMS", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_restore = Button(LeftViewForm, text="Restore", command=self.Restore, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_restore.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S.No", "Deleted_date", "Item Name", "Total Items", "Issue", "Balance", "Address", "Bill No.", "Amount", "GST","GST Amount", "Without GST"), selectmode="extended", height=100, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S.No', text="S.No", anchor=W)
        tree.heading('Deleted_date', text="Deleted_date", anchor=W)
        tree.heading('Item Name', text="Item Name", anchor=W)
        tree.heading('Address', text="Address", anchor=W)
        tree.heading('Bill No.', text="Bill No.", anchor=W)
        tree.heading('Amount', text="Amount", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('GST Amount', text="GST Amount", anchor=W)
        tree.heading('Without GST', text="Without GST", anchor=W)
        tree.heading('Total Items', text="Total Items", anchor=W)
        tree.heading('Issue', text="Issue", anchor=W)
        tree.heading('Balance', text="Balance", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=90)
        tree.column('#2', stretch=NO, minwidth=0, width=110)
        tree.column('#3', stretch=NO, minwidth=0, width=200)
        tree.column('#4', stretch=NO, minwidth=0, width=160)
        tree.column('#5', stretch=NO, minwidth=0, width=120)
        tree.column('#6', stretch=NO, minwidth=0, width=130)
        tree.column('#7', stretch=NO, minwidth=0, width=310)
        tree.column('#8', stretch=NO, minwidth=0, width=160)
        tree.column('#9', stretch=NO, minwidth=0, width=160)
        tree.column('#10', stretch=NO, minwidth=0, width=90)
        tree.column('#11', stretch=NO, minwidth=0, width=170)
        tree.column('#12', stretch=NO, minwidth=0, width=170)
        tree.pack()
        self.DisplayData()

    def Deleted_Bills(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()

        self.select = 8
        global select
        select = self.select

        global lista
        lista = []
        self.d.execute("SELECT Item_name from conty")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        global tree
        self.Deleted_bills = Frame(self.main)
        self.Deleted_bills.pack()
        TopViewForm = Frame(self.Deleted_bills, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.Deleted_bills, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.Deleted_bills, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="DELETED  BILLS", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_restore = Button(LeftViewForm, text="Restore", command=self.Restore, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_restore.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S_No", "Date", "Item name", "Quantity", "Shop address", "Bill no.", "Cost Without GST", "GST", "Total Cost"),selectmode="extended", height=100, yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S_No', text="S.No", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Item name', text="Item Name", anchor=W)
        tree.heading('Quantity', text="Quantity", anchor=W)
        tree.heading('Shop address', text="Shop Address", anchor=W)
        tree.heading('Bill no.', text="Bill No.", anchor=W)
        tree.heading('Cost Without GST', text="Cost Without GST", anchor=W)
        tree.heading('GST', text="GST", anchor=W)
        tree.heading('Total Cost', text="Total Cost", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=90)
        tree.column('#2', stretch=NO, minwidth=0, width=170)
        tree.column('#3', stretch=NO, minwidth=0, width=270)
        tree.column('#4', stretch=NO, minwidth=0, width=170)
        tree.column('#5', stretch=NO, minwidth=0, width=390)
        tree.column('#6', stretch=NO, minwidth=0, width=170)
        tree.column('#7', stretch=NO, minwidth=0, width=250)
        tree.column('#8', stretch=NO, minwidth=0, width=130)
        tree.column('#9', stretch=NO, minwidth=0, width=170)
        tree.pack()
        self.DisplayData()

    def Deleted_Issued(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()

        self.select = 9
        global select
        select = self.select

        global lista
        lista = []
        self.d.execute("SELECT Dept_Name,Item_Name from issue")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                lista.append(total)
        global tree
        self.Deleted_issued = Frame(self.main)
        self.Deleted_issued.pack()
        TopViewForm = Frame(self.Deleted_issued, width=600, bd=1, relief=SOLID, bg="cyan")
        TopViewForm.pack(side=TOP, fill=X)
        LeftViewForm = Frame(self.Deleted_issued, width=600, bg="ghost white")
        LeftViewForm.pack(side=LEFT, fill=Y)
        MidViewForm = Frame(self.Deleted_issued, width=600)
        MidViewForm.pack(side=RIGHT)
        lbl_text = Label(TopViewForm, text="DELETED ISSUED ITEMS", font=('Copperplate Gothic Bold', 20), width=600, bg="cyan")
        lbl_text.pack(fill=X, pady=4)
        lbl_txtsearch = Label(LeftViewForm, text="Search", font=('Copperplate Gothic Light', 15, "bold"), bg="ghost white")
        lbl_txtsearch.pack(side=TOP, anchor=W)
        search = AutocompleteEntry(lista, LeftViewForm, font=('arial', 15), width=10, relief=SOLID)
        search.pack(side=TOP, padx=10, fill=X)
        btn_search = Button(LeftViewForm, text="Search", command=self.Search, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_reset = Button(LeftViewForm, text="Refresh", command=self.Reset, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        btn_restore = Button(LeftViewForm, text="Restore", command=self.Restore, font=("Copperplate Gothic Light", 12, "bold"), relief=GROOVE, activebackground='black', activeforeground='white', bg='white')
        btn_restore.pack(side=TOP, padx=10, pady=10, fill=X)
        self.style.configure("Vertical.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        self.style.configure("Horizontal.TScrollbar", background="cyan", troughcolor="black", highlightcolor="green", highlightbackground="red")
        scrollbarx = ttk.Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = ttk.Scrollbar(MidViewForm, orient=VERTICAL)
        self.style.configure("mystyle.Treeview", font=('arial', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Copperplate Gothic Light', 13, "bold"), background="black", foreground="cyan")
        tree = ttk.Treeview(MidViewForm, style="mystyle.Treeview", columns=("S_NO", "Date", "Time", "Dept_Name", "Item_Name", "Item_pieces", "Name", "Phone_No"), selectmode="extended",height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        tree.heading('S_NO', text="S_NO", anchor=W)
        tree.heading('Date', text="Date", anchor=W)
        tree.heading('Time', text="Time", anchor=W)
        tree.heading('Dept_Name', text="Dept_Name", anchor=W)
        tree.heading('Item_Name', text="Item_Name", anchor=W)
        tree.heading('Item_pieces', text="Item_pieces", anchor=W)
        tree.heading('Name', text="Name", anchor=W)
        tree.heading('Phone_No', text="Phone_No", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=100)
        tree.column('#2', stretch=NO, minwidth=0, width=160)
        tree.column('#3', stretch=NO, minwidth=0, width=190)
        tree.column('#4', stretch=NO, minwidth=0, width=390)
        tree.column('#5', stretch=NO, minwidth=0, width=300)
        tree.column('#6', stretch=NO, minwidth=0, width=210)
        tree.column('#7', stretch=NO, minwidth=0, width=260)
        tree.column('#8', stretch=NO, minwidth=0, width=260)
        tree.pack()
        self.DisplayData()

    # ========================================================== Adding new Item =================================================================

    def ShowAddNew(self):
        global addnewform
        global titl
        if self.select == 6:
            titl = "Inventory Management System/Issue"
            addnewform = Toplevel()
            addnewform.title(titl)
            width = 550
            height = 450
        else:
            titl = "Inventory Management System/Add new"
            addnewform = Toplevel()
            addnewform.title(titl)
            width = 550
            height = 490
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
        addnewform.resizable(0, 0)
        self.AddNewForm()

    def AddNewForm(self):
        new = 0
        if self.select == 6:
            global TopAddNew
            global MidAddNew
            TopAddNew = Frame(addnewform, width=600, height=600, bd=1, relief=SOLID)
            TopAddNew.pack(side=TOP, pady=10)
            lbl_text = Label(TopAddNew, text="Issue", font=('arial', 22), width=600)
            lbl_text.pack(fill=X)
            MidAddNew = Frame(addnewform, width=600)
            MidAddNew.pack(side=TOP, pady=5)
            # ======================== label ===================
            lbl_dept_name = Label(MidAddNew, text="Department Name:", font=('arial', 18), bd=10)
            lbl_dept_name.grid(row=0, sticky=W)
            lbl_item_name = Label(MidAddNew, text="Item Name:", font=('arial', 18), bd=10)
            lbl_item_name.grid(row=1, sticky=W)
            lbl_item_pieces = Label(MidAddNew, text="Item Pieces.:", font=('arial', 18), bd=10)
            lbl_item_pieces.grid(row=2, sticky=W)
            lbl_name = Label(MidAddNew, text="Name:", font=('arial', 18), bd=10)
            lbl_name.grid(row=3, sticky=W)
            lbl_phone_no = Label(MidAddNew, text="Phone No:", font=('arial', 18), bd=10)
            lbl_phone_no.grid(row=4, sticky=W)
            # ======================= input ====================
            choices = {'Computer Applications', 'Computer Hardware and Networking', 'Plumbing and Sanitary','Electrition/Motor winding/Wiremaan', 'Refrigeration/Air conditioning','Carpentary and Aluminium fabrication', 'Welding and Steel Fabrication', 'Motor mechanic','Electrition', 'Fence Desighning', 'Auto Electrition', 'Machienist','Food Processing/Cooking Course'}
            self.dropdown.set('   - - - - - - -SELECT- - - - - - -   ')
            popupMenu = OptionMenu(MidAddNew, self.dropdown,*choices)  # ( Exception , combo box - self.combo = ttk.Combobox(self.register, font=("Times New Roman", 18), width=18)
            # self.combo['values'] = ('Computer Applications', 'Computer Hardware and Networking', 'Plumbing and Sanitary', 'Electrition/Motor winding/Wiremaan', 'Refrigeration/Air conditioning', 'Carpentary and Aluminium fabrication', 'Welding and Steel Fabrication', 'Motor mechanic', 'Electrition', 'Fence Desighning', 'Auto Electrition', 'Machienist', 'Food Processing/Cooking Course')
            # self.combo.current(1)  # set the selected item
            # self.combo.grid(column=2, row=6) )
            popupMenu.grid(row=0, column=1)
            item_name = Autocomplete(lista2, MidAddNew, font=('arial', 18), width=15, relief=SOLID)
            item_name.focus()
            item_name.grid(row=1, column=1)
            item_pieces = Entry(MidAddNew, textvariable=self.ITEM_PIECES, font=('arial', 18), width=15, relief=SOLID)
            item_pieces.grid(row=2, column=1)
            name = Entry(MidAddNew, textvariable=self.NAME, font=('arial', 18), width=15, relief=SOLID)
            name.grid(row=3, column=1)
            phone_no = Entry(MidAddNew, textvariable=self.PHONE_NO, font=('arial', 18), width=15, relief=SOLID)
            phone_no.grid(row=4, column=1)
            btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", relief=SOLID,command=self.AddNew)
            btn_add.grid(row=5, columnspan=2, pady=20)
            global lbl_result3
            lbl_result3 = Label(MidAddNew, text="", font=('Copperplate Gothic Bold', 18, 'bold'))
            lbl_result3.grid(row=6, column=0, columnspan=3)

        else:
            TopAddNew = Frame(addnewform, width=600, height=600, bd=1, relief=SOLID)
            TopAddNew.pack(side=TOP, pady=10)
            lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 22), width=600)
            lbl_text.pack(fill=X)
            MidAddNew = Frame(addnewform, width=600)
            MidAddNew.pack(side=TOP, pady=5)
            lbl_itemname = Label(MidAddNew, text="Item Name:", font=('arial', 18), bd=10)
            lbl_itemname.grid(row=0, sticky=W)
            lbl_address = Label(MidAddNew, text="Firm Name:", font=('arial', 18), bd=10)
            lbl_address.grid(row=1, sticky=W)
            lbl_billno = Label(MidAddNew, text="Bill No.:", font=('arial', 18), bd=10)
            lbl_billno.grid(row=2, sticky=W)
            lbl_total_amount = Label(MidAddNew, text="Total Amount:", font=('arial', 18), bd=10)
            lbl_total_amount.grid(row=3, sticky=W)
            lbl_gst = Label(MidAddNew, text="GST (In %):", font=('arial', 18), bd=10)
            lbl_gst.grid(row=4, sticky=W)
            lbl_totalitems = Label(MidAddNew, text="Total Items:", font=('arial', 18), bd=10)
            lbl_totalitems.grid(row=5, sticky=W)
            item_name = Autocomplete(lista, MidAddNew, font=('arial', 18), width=15, relief=SOLID)
            item_name.focus()
            item_name.grid(row=0, column=1)
            address = Entry(MidAddNew, textvariable=self.ADDRESS, font=('arial', 18), width=15, relief=SOLID)
            address.grid(row=1, column=1)
            bill_no = Entry(MidAddNew, textvariable=self.BILL_NO, font=('arial', 18), width=15, relief=SOLID)
            bill_no.grid(row=2, column=1)
            total_amount = Entry(MidAddNew, textvariable=self.TOTAL_AMOUNT, font=('arial', 18), width=15, relief=SOLID)
            total_amount.grid(row=3, column=1)
            gst = Entry(MidAddNew, textvariable=self.GST, font=('arial', 18), width=15, relief=SOLID)
            gst.grid(row=4, column=1)
            total_items = Entry(MidAddNew, textvariable=self.TOTAL_ITEMS, font=('arial', 18), width=15, relief=SOLID)
            total_items.grid(row=5, column=1)
            btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=self.AddNew,relief=SOLID)
            btn_add.grid(row=8, columnspan=2, pady=20)
            global lbl_result2
            lbl_result2 = Label(MidAddNew, text="", font=('Copperplate Gothic Bold', 18, 'bold'))
            lbl_result2.grid(row=9, column=0, columnspan=3)


    def checkin(self):
        if self.ITEM_NAME.get() == "" or self.ITEM_NAME.get() == 0:
            self.ITEM_NAME.set("")
            self.BILL_NO.set(0)
            self.ADDRESS.set("")
            self.GST.set(0)
            self.TOTAL_ITEMS.set(0)
            self.ISSUE.set("")
            self.BALANCE.set(0)
            self.DEPT_NAME.set("")
            self.ITEM_NAME.set("")
            self.ITEM_PIECES.set(0)
            self.NAME.set("")
            self.PHONE_NO.set(0)
            self.TOTAL_AMOUNT.set(0)
            TopAddNew.destroy()
            MidAddNew.destroy()
            self.AddNewForm()
        else:
            pass


    def Assign_update(self):
        global addr, bil, amt, Gst, titem
        addr = update[0]
        bil = update[1]
        amt = update[2]
        Gst = update[3]
        titem = update[4]
        self.ADDRESS.set(addr)
        self.BILL_NO.set(bil)
        self.TOTAL_AMOUNT.set(amt)
        self.GST.set(Gst)
        self.TOTAL_ITEMS.set(titem)
        check = 1
        return bil

    def Updation(self):
        if check != 0:
            self.Assign_update()
        elif check == 0:
            new = 1
            self.Assign_update()
            addnewform.destroy()
            global addnewform1
            addnewform1 = Tk()
            addnewform1.title(titl)
            width = 550
            height = 480
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = (screen_width / 2) - (width / 2)
            y = (screen_height / 2) - (height / 2)
            addnewform1.geometry("%dx%d+%d+%d" % (width, height, x, y))
            addnewform1.resizable(0, 0)
            TopAddNew = Frame(addnewform1, width=600, height=600, bd=1, relief=SOLID)
            TopAddNew.pack(side=TOP, pady=10)
            lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 22), width=600)
            lbl_text.pack(fill=X)
            MidAddNew = Frame(addnewform1, width=600)
            MidAddNew.pack(side=TOP, pady=5)
            lbl_itemname = Label(MidAddNew, text="Item Name:", font=('arial', 18), bd=10)
            lbl_itemname.grid(row=0, sticky=W)
            lbl_address = Label(MidAddNew, text="Address:", font=('arial', 18), bd=10)
            lbl_address.grid(row=1, sticky=W)
            lbl_billno = Label(MidAddNew, text="Bill No.:", font=('arial', 18), bd=10)
            lbl_billno.grid(row=2, sticky=W)
            lbl_total_amount = Label(MidAddNew, text="Total Amount:", font=('arial', 18), bd=10)
            lbl_total_amount.grid(row=3, sticky=W)
            lbl_gst = Label(MidAddNew, text="GST:", font=('arial', 18), bd=10)
            lbl_gst.grid(row=4, sticky=W)
            lbl_totalitems = Label(MidAddNew, text="Total Items:", font=('arial', 18), bd=10)
            lbl_totalitems.grid(row=5, sticky=W)
            item_name = Autocomplete(lista, MidAddNew, font=('arial', 18), width=15, relief=SOLID)
            item_name.insert(END, val)
            item_name.grid(row=0, column=1)
            address = Entry(MidAddNew, textvariable=self.ADDRESS, font=('arial', 18), width=15, relief=SOLID)
            address.insert(END, addr)
            address.grid(row=1, column=1)
            bill_no = Entry(MidAddNew, textvariable=self.BILL_NO, font=('arial', 18), width=15, relief=SOLID)
            bill_no.insert(END, bil)
            bill_no.grid(row=2, column=1)
            total_amount = Entry(MidAddNew, textvariable=self.TOTAL_AMOUNT, font=('arial', 18), width=15, relief=SOLID)
            total_amount.insert(END, amt)
            total_amount.grid(row=3, column=1)
            gst = Entry(MidAddNew, textvariable=self.GST, font=('arial', 18), width=15, relief=SOLID)
            gst.insert(END, Gst)
            gst.grid(row=4, column=1)
            total_items = Entry(MidAddNew, textvariable=self.TOTAL_ITEMS, font=('arial', 18), width=15, relief=SOLID)
            total_items.insert(END, titem)
            total_items.grid(row=5, column=1)
            btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=30, bg="#009ACD", command=self.AddNew,relief=SOLID)
            btn_add.grid(row=8, columnspan=2, pady=20)

    def addmore_paybill(self):
        global m
        global Cdate
        self.d.execute("SELECT MAX(S_No) from stock where Deleted_date='' ")
        for i in self.d:
            for j in range(len(i)):
                sno = i[j]
        sno += 1
        b = self.TOTAL_ITEMS.get()
        tot = self.TOTAL_AMOUNT.get()
        gst = float(self.GST.get())
        without_gst = float(tot - ((gst * tot) / (100 + gst)))
        gst_amt = float(without_gst * (gst / 100))
        Cdate = date.today().__format__('%d-%m-%Y')
        global val
        if self.ADDRESS.get() == " " or self.BILL_NO.get() == " " or self.TOTAL_ITEMS.get() == " " or tot == 0 or gst == 0 or self.ITEM_NAME.get() == " " or self.BILL_NO.get() == 0:
              lbl_result4.config(text="Please complete all fields!!!", fg="red")
        else:
            if new == 1:
                addnewform1.destroy()
            elif new == 0:
                addnewform.destroy()
            self.m = 'conty'
            self.d.execute("INSERT into conty(Date,Item_name,Address,Bill_no,Quantity,Without_gst,GST,Total_amount)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(str(Cdate), str(self.ITEM_NAME.get()), str(self.ADDRESS.get()), int(self.BILL_NO.get()),int(self.TOTAL_ITEMS.get()), without_gst, int(self.GST.get()), float(self.TOTAL_AMOUNT.get())))
            self.c.commit()
            self.ITEM_NAME.set("")
            addnewform.destroy()
            self.county_pay()

    def AddNew(self):
        global m
        global Cdate
        self.d.execute("SELECT MAX(S_No) from stock where Deleted_date='' ")
        for i in self.d:
            for j in range(len(i)):
                sno = i[j]
        sno += 1
        if new == 1:
            addnewform1.destroy()
            # elif new == 0:
            #     addnewform.destroy()
            b = self.TOTAL_ITEMS.get()
            tot = self.TOTAL_AMOUNT.get()
            gst = float(self.GST.get())
            without_gst = float(tot - ((gst * tot) / (100 + gst)))
            gst_amt = float(without_gst * (gst / 100))
            Cdate = date.today().__format__('%d-%m-%Y')
            global val
            if self.select == 2:
                if self.ADDRESS.get() == " " or self.BILL_NO.get() == 0 or self.TOTAL_AMOUNT.get() == 0 or gst == 0 or self.TOTAL_ITEMS.get() == 0:
                    lbl_result2.config(text="Please complete all fields!!!", fg="red")
                else:
                    self.m = 'asset'
                    self.d.execute("INSERT INTO stock (S_No,Date,Item_name,Address,Bill_no,Amount,GST,Total_Items,Department,Balance,GST_Amt,Without_GST) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(sno), str(Cdate), str(val), str(self.ADDRESS.get()), int(self.BILL_NO.get()),float(self.TOTAL_AMOUNT.get()), float(self.GST.get()), int(self.TOTAL_ITEMS.get()), str(self.m), int(self.TOTAL_ITEMS.get()),gst_amt, without_gst))
                    self.c.commit()
            elif self.select == 3:
                if self.ADDRESS.get() == " " or self.BILL_NO.get() == 0 or self.TOTAL_AMOUNT.get() == 0 or gst == 0 or self.TOTAL_ITEMS.get() == 0:
                    lbl_result2.config(text="Please complete all fields!!!", fg="red")
                else:
                    self.m = 'stationary'
                    self.d.execute("INSERT INTO stock (S_No,Date,Item_name,Address,Bill_no,Amount,GST,Total_Items,Department,Balance,GST_Amt,Without_GST) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(sno), str(Cdate), str(val), str(self.ADDRESS.get()), int(self.BILL_NO.get()),float(self.TOTAL_AMOUNT.get()), float(self.GST.get()), int(self.TOTAL_ITEMS.get()), str(self.m), b,gst_amt, without_gst))
                    self.c.commit()
            elif self.select == 5:
                if self.ITEM_NAME or self.ADDRESS or self.BILL_NO or self.TOTAL_ITEMS or self.GST or self.TOTAL_AMOUNT:
                    lbl_result4.config(text="Please complete all fields!!!", fg="red")
                else:
                    self.m = 'conty'
                    self.d.execute("INSERT into conty(Date,Item_name,Address,Bill_no,Quantity,Without_gst,GST,Total_amount)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(str(Cdate), str(self.ITEM_NAME.get()), str(self.ADDRESS.get()), int(self.BILL_NO.get()),int(self.TOTAL_ITEMS.get()), without_gst, int(self.GST.get()), float(self.TOTAL_AMOUNT.get())))
                    self.c.commit()
            elif self.select == 6:
                if self.ITEM_PIECES.get() == "" or self.NAME.get() == "" or self.PHONE_NO.get() == 0 or self.dropdown.get() == "   - - - - - - -SELECT- - - - - - -   ":
                    lbl_result3.config(text="Please complete all fields!!!", fg="red")
                else:
                    global totall
                    global issuee
                    self.d.execute("SELECT Issue from stock where Item_name=%s", [val])
                    for i in self.d:
                        for j in range(len(i)):
                            global issuee
                            issuee = i[j] + self.ITEM_PIECES.get()
                            self.ISS = issuee
                    self.d.execute("UPDATE stock set Issue=%s where Item_name=%s", [ str(self.ISS), str( val ) ])
                    self.d.execute("SELECT Total_Items from stock where Item_name=%s", [val])
                    for i in self.d:
                        for j in range(len(i)):
                            totall = i[j]
                    self.d.execute("SELECT Balance from stock where Item_name=%s", [val])
                    print("ISS=",self.ISS)
                    for i in self.d:
                        for j in range(len([i])):
                            self.balan = i[j]
                    print("balan=",self.balan)
                    if int(self.balan) < 1:
                        result = tkMessageBox.showwarning('Inventory Management System', 'Item not available !',icon="warning")
                        # showerror('Inventory Management System', 'Item not available !',icon="warning")
                    else:
                        self.balan = totall - issuee
                        self.d.execute("UPDATE stock set Balance=%s where Item_name=%s", [self.balan, val])
                        Ctime = datetime.now().strftime(format('%I:%M:%S %p'))
                        Cdate = date.today().__format__('%d-%m-%Y')
                        self.d.execute("INSERT INTO issue (Date,Time,Dept_Name,Item_Name,Item_pieces,Name,Phone_No) VALUES(%s,%s,%s,%s,%s,%s,%s)",(str(Cdate), str(Ctime), str(self.dropdown.get()), str(val),int(self.ITEM_PIECES.get()), str(self.NAME.get()), int(self.PHONE_NO.get())))
                        self.c.commit()
                # ==================== Reset variables value ===================
                self.ITEM_NAME.set("")
                self.BILL_NO.set(0)
                self.ADDRESS.set("")
                self.GST.set(0)
                self.TOTAL_ITEMS.set(0)
                b=0
                tot=0
                gst = 0
                without_gst = 0
                gst_amt = 0
                self.ISSUE.set(0)
                self.BALANCE.set(0)
                self.DEPT_NAME.set("")
                self.ITEM_PIECES.set(0)
                self.NAME.set("")
                self.PHONE_NO.set(0)
                self.TOTAL_AMOUNT.set(0)
                # addnewform.destroy()

        # ================================ For Adding New Bill =====================================

    def county_pay(self):
        global addnewform
        addnewform = Toplevel()
        addnewform.title("Simple Inventory System/Pay bill")
        width = 550
        height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
        addnewform.resizable(0, 0)
        TopAddNew = Frame(addnewform, width=600, height=600, bd=1, relief=SOLID)
        TopAddNew.pack(side=TOP, pady=10)
        lbl_text = Label(TopAddNew, text="Add Bill", font=('arial', 22), width=600)
        lbl_text.pack(fill=X)
        MidAddNew = Frame(addnewform, width=600)
        MidAddNew.pack(side=TOP, pady=5)
        lbl_itemname = Label(MidAddNew, text="Item Name:", font=('arial', 18), bd=10)
        lbl_itemname.grid(row=5, sticky=W)
        lbl_address = Label(MidAddNew, text="Shop address:", font=('arial', 18), bd=10)
        lbl_address.grid(row=1, sticky=W)
        lbl_billno = Label(MidAddNew, text="Bill No.:", font=('arial', 18), bd=10)
        lbl_billno.grid(row=2, sticky=W)
        lbl_total_amount = Label(MidAddNew, text="Quantity", font=('arial', 18), bd=10)
        lbl_total_amount.grid(row=3, sticky=W)
        lbl_gst = Label(MidAddNew, text="GST:", font=('arial', 18), bd=10)
        lbl_gst.grid(row=4, sticky=W)
        lbl_totalitems = Label(MidAddNew, text="Total Amount:", font=('arial', 18), bd=10)
        lbl_totalitems.grid(row=0, sticky=W)
        item_name = Entry(MidAddNew, textvariable=self.ITEM_NAME, font=('arial', 18), width=15, relief=SOLID)
        item_name.focus()
        item_name.grid(row=5, column=1)
        address = Entry(MidAddNew, textvariable=self.ADDRESS, font=('arial', 18), width=15, relief=SOLID)
        address.grid(row=1, column=1)
        bill_no = Entry(MidAddNew, textvariable=self.BILL_NO, font=('arial', 18), width=15, relief=SOLID)
        bill_no.grid(row=2, column=1)
        total_amount = Entry(MidAddNew, textvariable=self.TOTAL_ITEMS, font=('arial', 18), width=15, relief=SOLID)
        total_amount.grid(row=3, column=1)
        gst = Entry(MidAddNew, textvariable=self.GST, font=('arial', 18), width=15, relief=SOLID)
        gst.grid(row=4, column=1)
        total_items = Entry(MidAddNew, textvariable=self.TOTAL_AMOUNT, font=('arial', 18), width=15, relief=SOLID)
        total_items.grid(row=0, column=1)
        btn_add = Button(MidAddNew, text="Save", font=('arial', 18), width=16, bg="#009ACD", relief=SOLID,command=self.AddNew)
        btn_add.grid(row=8, column=0, pady=20, padx=8)
        btn_add2 = Button(MidAddNew, text="Add more", font=('arial', 18), width=16, bg="#009ACD", relief=SOLID,command=self.addmore_paybill)
        btn_add2.grid(row=8, column=1, pady=20, padx=8)
        global lbl_result4
        lbl_result4 = Label(MidAddNew, text="", font=('Copperplate Gothic Bold', 18, 'bold'))
        lbl_result4.grid(row=9, column=0, columnspan=3)

    # =================================== For Searching,Reset,Delete,Restore data=====================================

    def Search(self):
        if check == 1:
            tree.delete(*tree.get_children())
            if self.select == 1:
                self.d.execute("SELECT * FROM stock WHERE Item_name LIKE '%" + val + "%'")
            elif self.select == 2:
                k = 'asset'
                self.d.execute("select * from stock where Item_name=%s and department=%s", [val, k])
            elif self.select == 3:
                k = 'stationary'
                self.d.execute("select * from stock where Item_name=%s and department=%s", [val, k])
            elif self.select == 4:
                self.d.execute("SELECT * FROM stock WHERE Item_name LIKE '%" + val + "%'")
            elif self.select == 5:
                self.d.execute("SELECT * FROM conty WHERE Item_name LIKE '%" + val + "%'")
            elif self.select == 6:
                self.d.execute("SELECT * FROM issue WHERE Item_name LIKE '" + val + "%'")
            elif self.select == 7:
                self.d.execute("SELECT * FROM stock WHERE Item_name LIKE '" + val + "%' and Deleted_date!=''")
            for data in self.d:
                tree.insert('', 'end', values=(data))

    def Reset(self):
        tree.delete(*tree.get_children())
        search.setvar("")
        self.DisplayData()

    def Delete(self):
        if not tree.selection():
            print("ERROR")
        else:
            result = tkMessageBox.askquestion('Inventory Management System','Are you sure you want to delete this record?', icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                x = selecteditem[0]
                tup = [x]
                global s_no
                for i in tup:
                    s_no = i
                Cdate = date.today().__format__('%d-%m-%Y')
                # val=[Cdate,x,]
                if self.select == 5:
                    self.d.execute("UPDATE conty set Deleted_date=%s where S_no=%s", [Cdate, s_no])
                    self.c.commit()
                elif self.select == 6:
                    self.d.execute("UPDATE issue set Deleted_date=%s where S_no=%s", [Cdate, s_no])
                    self.c.commit()
                else:
                    self.d.execute("UPDATE stock set Deleted_date=%s where S_no=%s", [Cdate, s_no])
                    self.c.commit()

    def Restore(self):
        if not tree.selection():
            print("ERROR")
        else:
            result = tkMessageBox.askquestion('Inventory Management System', 'Do you want to restore this record?',icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                x = selecteditem[0]
                tup = [x]
                global s_no
                for i in tup:
                    s_no = i
                if self.select == 8:
                    self.d.execute("UPDATE conty set Deleted_date=' ' where S_no=%s", [s_no])
                    self.c.commit()
                elif self.select == 9:
                    self.d.execute("UPDATE issue set Deleted_date=' ' where S_no=%s", [s_no])
                    self.c.commit()
                else:
                    self.d.execute("UPDATE stock set Deleted_date=' ' where S_no=%s", [s_no])
                    self.c.commit()
            tree.delete(*tree.get_children())
            self.DisplayData()

    def About(self):
        if self.select == 1:
            self.stock1.destroy()
        elif self.select == 2:
            self.asset.destroy()
        elif self.select == 3:
            self.stationary.destroy()
        elif self.select == 4:
            self.stock.destroy()
        elif self.select == 5:
            self.conty.destroy()
        elif self.select == 6:
            self.issue.destroy()
        elif self.select == 7:
            self.DeletedData.destroy()
        elif self.select == 8:
            self.Deleted_bills.destroy()
        elif self.select == 9:
            self.Deleted_issued.destroy()
        elif self.select == 10:
            self.canvas.destroy()
            self.about.destroy()
        self.select = 10
        txt = """⦿ DEVELOPED BY :-

   ♦ Amanjot Singh
   ♦ Arshdeep Singh
   ♦ Jaspreet Singh


⦿ TRAINING :-

   We all had taken Training in Python from STC (Skill Training Center) under the Guidance of Gurpreet Singh (Python Trainer).


⦿ FEATURE's OF OUR PROJECT :-

   ♦ Open Source Software
   ♦ User Friendly
   ♦ Good Performance
   ♦ Eazy Operation
   ♦ All GST Calculations (In backend)
   ♦ Print Facility (Creates PDF or XL sheet)
   ♦ Easy Searching
   ♦ Autocomplete Suggestions
   ♦ Data security (Username & Password Required)
   ♦ Xampp Software (Provided)


⦿ FUTURE UPDATE WILL CONSIST :-

   ♦ Alert for Stock Running Out
   ♦ Change Username & Password Settings
   ♦ Analytics (Using Graphs)


⦿ MENTORS :-

   ♦ Dr.H.S.Jawanda (H.O.D)
   ♦ Gurpreet Singh (Python Trainer)

⦿ PROJECT FOCUS :-

   ♦ It mainly Removes the Burden of Files and difficult calculations.

                                                                          """
        self.about = Frame(self.main, bg='white')
        self.about.pack()
        self.canvas = Canvas(self.main, bg="white")
        scroll_y = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview, relief=SOLID)
        self.frame = Frame(self.canvas, bg="white")

        if self.screen_width >= 1400:
            label = Label(self.about, text='ABOUT', bg="cyan", width='300', height=1,
                          font=('Lucida Calligraphy', 25, 'bold'), bd=2)
            label.pack()
            Label(self.frame, text=txt, justify=LEFT, font=('Lucida Calligraphy', 15), bg="white").pack()
        elif self.screen_width <= 900:
            label = Label(self.about, text='ABOUT', bg="cyan", width='300', height=1,
                          font=('Lucida Calligraphy', 20, 'bold'), bd=2)
            label.pack()
            Label(self.frame, text=txt, justify=LEFT, font=('Lucida Calligraphy', 10), bg="white").pack()
        elif self.screen_width > 900 and self.screen_width < 1400:
            label = Label(self.about, text='ABOUT', bg="cyan", width='300', height=1,
                          font=('Lucida Calligraphy', 23, 'bold'), bd=2)
            label.pack()
            Label(self.frame, text=txt, justify=LEFT, font=('Lucida Calligraphy', 12), bg="white").pack()
        else:
            label = Label(self.about, text='ABOUT', bg="cyan", width='300', height=1,
                          font=('Lucida Calligraphy', 23, 'bold'), bd=2)
            label.pack()
            Label(self.frame, text=txt, justify=LEFT, font=('Lucida Calligraphy', 8), bg="white").pack()
        self.canvas.create_window(0, 0, anchor='nw', window=self.frame)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'), yscrollcommand=scroll_y.set)
        self.canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

    def choice(self):
        global Print_form
        Print_form = Toplevel(bg="white")
        if self.select == 1:
            Print_form.title("Simple Inventory System\Stock\Print")
        elif self.select == 2:
            Print_form.title("Simple Inventory System\Asset\Print")
        elif self.select == 3:
            Print_form.title("Simple Inventory System\Stationary\Print")
        elif self.select == 4:
            Print_form.title("Simple Inventory System\Stock\Print")
        elif self.select == 5:
            Print_form.title("Simple Inventory System\Conty\Print")
        elif self.select == 6:
            Print_form.title("Simple Inventory System\Issue\Print")
        width = 450
        height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        Print_form.geometry("%dx%d+%d+%d" % (width, height, x, y))
        Print_form.resizable(0, 0)
        TopAddNew = Frame(Print_form, bg="white", width=600, height=600, bd=1, relief=SOLID)
        TopAddNew.pack(side=TOP, pady=10)
        lbl_text = Label(TopAddNew, bg="white", text="Select Your Choice", font=('arial', 22), width=600)
        lbl_text.pack(fill=X)
        MidAddNew = Frame(Print_form, bg="white", width=600)
        MidAddNew.pack(side=TOP, pady=5)
        space_label = Label(MidAddNew, text="", bg="white")
        space_label.grid(row=1, column=1, pady=10)
        lb_choice = Label(MidAddNew, text="Options :", font=("Times New Roman", 25), bg="white")
        lb_choice.grid(row=2, column=1, pady=30)
        choices = {'      Generate XL Sheet     ', '        Generate PDF        '}
        self.dropdown.set('  - - - - -SELECT- - - - -  ')
        popmenu = OptionMenu(MidAddNew, self.dropdown, *choices)
        popmenu.grid(row=2, column=2)
        space_label.grid(row=3, column=1, pady=40)
        btn_add = Button(MidAddNew, text="Print", font=('arial', 18), width=20, activebackground='black',
                         activeforeground='white', relief=SOLID, command=self.print)
        btn_add.grid(row=4, column=1, columnspan=2)

    # ========================================== Display Data (Sql queries) =======================================

    def DisplayData(self):
        global k, nul
        nul = ''
        if self.select == 1:
            self.d.execute("SELECT * from stock where Deleted_date=''")
        elif self.select == 2:
            k = 'asset'
            self.d.execute("SELECT * from stock where Department=%s and Deleted_date=' '", [k])
        elif self.select == 3:
            k = 'stationary'
            self.d.execute("SELECT * from stock where Department=%s and Deleted_date=' '", [k])
        elif self.select == 4:
            self.d.execute("SELECT * from stock where Deleted_date = ' '")
        elif self.select == 5:
            self.d.execute("SELECT * from conty where Deleted_date = ' '")
        elif self.select == 6:
            self.d.execute("SELECT * from issue")
        elif self.select == 7:
            self.d.execute("select * from stock where Deleted_date != ' '")
        elif self.select == 8:
            self.d.execute("select * from conty where Deleted_date != ' '")
        elif self.select == 9:
            self.d.execute("select * from issue where Deleted_date != ' '")
        fetch = self.d.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))

    # ================================================= Bar Graph ==============================================

    def bar_graph(self):
        global glabels, gvalues
        glabels = []
        gvalues = []
        self.d.execute("SELECT Item_Name from issue where Deleted_date=''")
        for i in self.d:
            for j in range(len(i)):
                total = i[j]
                glabels.append(total)
        self.d.execute("SELECT Item_pieces from issue where Deleted_date=''")
        for i in self.d:
            for j in range(len(i)):
                totals = i[j]
                gvalues.append(totals)
        self.index = np.arange(len(glabels))
        plt.bar(self.index, gvalues)
        plt.xlabel('Items', fontsize=9)
        plt.ylabel('Most Issued', fontsize=9)
        plt.xticks(self.index, glabels, fontsize=7, rotation=0)
        plt.title('Isssued Items')
        plt.show()


    # ====================================================== Print ======================================================
    def print(self, spacing=1):
        printed_data_XL = []
        row = 0
        column = 0

        if str(self.dropdown.get()) == "      Generate XL Sheet     ":
            if self.select == 1:
                self.d.execute("SELECT * from stock where Deleted_date=''")
                headings = ["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount",
                            "GST", "GST Amount", "Without Gst", "field"]
                wb = xlsxwriter.Workbook("Stock Report.xlsx")
                ws = wb.add_worksheet()
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_XL.append(condata)
                for i in headings:
                    ws.write(row, column, i)
                    column += 1
                row = 1
                column = 0
                for Lsno, Ldate, Litem, Ltotal, Lissue, Lbalance, Laddress, LbillNo, LAmount, Lgst, LgstAmt, LwithoutGst, depart, deleteDate in printed_data_XL:
                    ws.write(row, column, Lsno)
                    ws.write(row, column + 1, Ldate)
                    ws.write(row, column + 2, Litem)
                    ws.write(row, column + 3, Ltotal)
                    ws.write(row, column + 4, Lissue)
                    ws.write(row, column + 5, Lbalance)
                    ws.write(row, column + 6, Laddress)
                    ws.write(row, column + 7, LbillNo)
                    ws.write(row, column + 8, LAmount)
                    ws.write(row, column + 9, Lgst)
                    ws.write(row, column + 10, LgstAmt)
                    ws.write(row, column + 11, LwithoutGst)
                    ws.write(row, column + 12, depart)
                    row += 1
                wb.close()
                os.startfile(".\Stock Report.xlsx", "open")

            if self.select == 2:
                self.d.execute("SELECT * from stock where Deleted_date='' and Department='asset'")
                headings = ["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount",
                            "GST", "GST Amount", "Without Gst", "Field"]
                wb = xlsxwriter.Workbook("Asset Report.xlsx")
                ws = wb.add_worksheet()
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_XL.append(condata)
                for i in headings:
                    ws.write(row, column, i)
                    column += 1
                row = 1
                column = 0
                for Lsno, Ldate, Litem, Ltotal, Lissue, Lbalance, Laddress, LbillNo, LAmount, Lgst, LgstAmt, LwithoutGst, depart, deleteDate in printed_data_XL:
                    ws.write(row, column, Lsno)
                    ws.write(row, column + 1, Ldate)
                    ws.write(row, column + 2, Litem)
                    ws.write(row, column + 3, Ltotal)
                    ws.write(row, column + 4, Lissue)
                    ws.write(row, column + 5, Lbalance)
                    ws.write(row, column + 6, Laddress)
                    ws.write(row, column + 7, LbillNo)
                    ws.write(row, column + 8, LAmount)
                    ws.write(row, column + 9, Lgst)
                    ws.write(row, column + 10, LgstAmt)
                    ws.write(row, column + 11, LwithoutGst)
                    ws.write(row, column + 12, depart)
                    row += 1
                wb.close()
                os.startfile(".\Asset Report.xlsx", "open")

            if self.select == 3:
                self.d.execute("SELECT * from stock where Deleted_date='' and Department='stationary'")
                headings = ["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount","GST", "GST Amount", "Without Gst", "Field"]
                wb = xlsxwriter.Workbook("Stationary Report.xlsx")
                ws = wb.add_worksheet()
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_XL.append(condata)
                for i in headings:
                    ws.write(row, column, i)
                    column += 1
                row = 1
                column = 0
                for Lsno, Ldate, Litem, Ltotal, Lissue, Lbalance, Laddress, LbillNo, LAmount, Lgst, LgstAmt, LwithoutGst, depart, deleteDate in printed_data_XL:
                    ws.write(row, column, Lsno)
                    ws.write(row, column + 1, Ldate)
                    ws.write(row, column + 2, Litem)
                    ws.write(row, column + 3, Ltotal)
                    ws.write(row, column + 4, Lissue)
                    ws.write(row, column + 5, Lbalance)
                    ws.write(row, column + 6, Laddress)
                    ws.write(row, column + 7, LbillNo)
                    ws.write(row, column + 8, LAmount)
                    ws.write(row, column + 9, Lgst)
                    ws.write(row, column + 10, LgstAmt)
                    ws.write(row, column + 11, LwithoutGst)
                    ws.write(row, column + 12, depart)
                    row += 1
                wb.close()
                os.startfile(".\Stationary Report.xlsx", "open")

            if self.select == 4:
                self.d.execute("SELECT * from stock where Deleted_date=''")
                headings = ["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount",
                            "GST", "GST Amount", "Without Gst", "Field"]
                wb = xlsxwriter.Workbook("Stock Report.xlsx")
                ws = wb.add_worksheet()
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_XL.append(condata)
                for i in headings:
                    ws.write(row, column, i)
                    column += 1
                row = 1
                column = 0
                for Lsno, Ldate, Litem, Ltotal, Lissue, Lbalance, Laddress, LbillNo, LAmount, Lgst, LgstAmt, LwithoutGst, depart, deleteDate in printed_data_XL:
                    ws.write(row, column, Lsno)
                    ws.write(row, column + 1, Ldate)
                    ws.write(row, column + 2, Litem)
                    ws.write(row, column + 3, Ltotal)
                    ws.write(row, column + 4, Lissue)
                    ws.write(row, column + 5, Lbalance)
                    ws.write(row, column + 6, Laddress)
                    ws.write(row, column + 7, LbillNo)
                    ws.write(row, column + 8, LAmount)
                    ws.write(row, column + 9, Lgst)
                    ws.write(row, column + 10, LgstAmt)
                    ws.write(row, column + 11, LwithoutGst)
                    ws.write(row, column + 12, depart)
                    row += 1
                wb.close()
                os.startfile(".\Stock Report.xlsx", "open")

            if self.select == 5:
                self.d.execute("SELECT * from conty where Deleted_date=''")
                headings = ["S No.", "Date", "Item Name", "Quantity", "Address", "Bill No.", "Without GST", "GST",
                            "Total Amount"]
                wb = xlsxwriter.Workbook("County Bills Report.xlsx")
                ws = wb.add_worksheet()
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_XL.append(condata)
                for i in headings:
                    ws.write(row, column, i)
                    column += 1
                row = 1
                column = 0
                for S_no, Date, Item_name, Quantity, Address, Bill_no, Without_gst, GST, Total_amount, Deleted_date in printed_data_XL:
                    ws.write(row, column, S_no)
                    ws.write(row, column + 1, Date)
                    ws.write(row, column + 2, Item_name)
                    ws.write(row, column + 3, Quantity)
                    ws.write(row, column + 4, Address)
                    ws.write(row, column + 5, Bill_no)
                    ws.write(row, column + 6, Without_gst)
                    ws.write(row, column + 7, GST)
                    ws.write(row, column + 8, Total_amount)
                    row += 1
                wb.close()
                os.startfile(".\County Bills Report.xlsx", "open")

            if self.select == 6:
                self.d.execute("SELECT * from issue where Deleted_date=''")
                headings = ["S No.", "Date", "Time", "Dept. Name", "Item Name", "Item Pieces", "Name", "Phone No."]
                wb = xlsxwriter.Workbook("Issued Report.xlsx")
                ws = wb.add_worksheet()
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_XL.append(condata)
                for i in headings:
                    ws.write(row, column, i)
                    column += 1
                row = 1
                column = 0
                for S_No, Date, Time, Dept_Name, Item_Name, Item_pieces, Name, Phone_No in printed_data_XL:
                    ws.write(row, column, S_No)
                    ws.write(row, column + 1, Date)
                    ws.write(row, column + 2, Time)
                    ws.write(row, column + 3, Dept_Name)
                    ws.write(row, column + 4, Item_Name)
                    ws.write(row, column + 5, Item_pieces)
                    ws.write(row, column + 6, Name)
                    ws.write(row, column + 7, Phone_No)
                    row += 1
                wb.close()
                os.startfile(".\Issued Report.xlsx", "open")



        elif str(self.dropdown.get()) == "        Generate PDF        ":
            pdf = FPDF()
            pdf.add_page(HORIZONTAL)

            if self.select == 1:
                printed_data_PDF = [["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount", "GST","GST Amount", "Without Gst"]]
                self.d.execute("SELECT S_No,Date,Item_name,Total_Items,Issue,Balance,Address,Bill_no,Amount,GST,GST_Amt,Without_GST from stock where Deleted_date=''")
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_PDF.append(condata)
                pdf.set_font("Arial", style="B", size=15)
                pdf.cell(w=110)
                pdf.cell(60, 10, "..!! Stock Report !!..", border=1, ln=0, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=10)
                col_width = pdf.w / 12.9
                row_height = pdf.font_size + 1
                for row in printed_data_PDF:
                    for item in row:
                        pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
                    pdf.ln(row_height * spacing)
                pdf.set_y(-31)
                pdf.set_font("Arial", style="I", size=8)
                pageNum = "Page no. %s" % pdf.page_no()
                pdf.cell(0, 10, pageNum, align="C")
                pdf.output('Stock Report.pdf')
                os.startfile(".\Stock Report.pdf", "open")

            if self.select == 2:
                printed_data_PDF = [["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount", "GST","GST Amount", "Without Gst"]]
                self.d.execute("SELECT S_No,Date,Item_name,Total_Items,Issue,Balance,Address,Bill_no,Amount,GST,GST_Amt,Without_GST from stock where Deleted_date='' and Department='asset'")
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_PDF.append(condata)
                pdf.set_font("Arial", style="B", size=15)
                pdf.cell(w=110)
                pdf.cell(60, 10, "..!! Asset Report !!..", border=1, ln=0, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=10)
                col_width = pdf.w / 12.9
                row_height = pdf.font_size + 1
                for row in printed_data_PDF:
                    for item in row:
                        pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
                    pdf.ln(row_height * spacing)
                pdf.set_y(-31)
                pdf.set_font("Arial", style="I", size=8)
                pageNum = "Page no. %s" % pdf.page_no()
                pdf.cell(0, 10, pageNum, align="C")
                pdf.output('Asset Report.pdf')
                os.startfile(".\Asset Report.pdf", "open")

            if self.select == 3:
                printed_data_PDF = [["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount", "GST","GST Amount", "Without Gst"]]
                self.d.execute("SELECT S_No,Date,Item_name,Total_Items,Issue,Balance,Address,Bill_no,Amount,GST,GST_Amt,Without_GST from stock where Deleted_date='' and Department='stationary'")
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_PDF.append(condata)
                pdf.set_font("Arial", style="B", size=15)
                pdf.cell(w=100)
                pdf.cell(70, 10, "..!! Stationary Report !!..", border=1, ln=0, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=10)
                col_width = pdf.w / 12.9
                row_height = pdf.font_size + 1
                for row in printed_data_PDF:
                    for item in row:
                        pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
                    pdf.ln(row_height * spacing)
                pdf.set_y(-31)
                pdf.set_font("Arial", style="I", size=8)
                pageNum = "Page no. %s" % pdf.page_no()
                pdf.cell(0, 10, pageNum, align="C")
                pdf.output('Stationary Report.pdf')
                os.startfile(".\Stationary Report.pdf", "open")

            if self.select == 4:
                printed_data_PDF = [["S No.", "Date", "Item", "Total Items", "Issued", "Remainig", "Address", "BillNo", "Amount", "GST","GST Amount", "Without Gst"]]
                self.d.execute("SELECT S_No,Date,Item_name,Total_Items,Issue,Balance,Address,Bill_no,Amount,GST,GST_Amt,Without_GST from stock where Deleted_date=''")
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_PDF.append(condata)
                pdf.set_font("Arial", style="B", size=15)
                pdf.cell(w=110)
                pdf.cell(60, 10, "..!! Stock Report !!..", border=1, ln=0, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=10)
                col_width = pdf.w / 12.9
                row_height = pdf.font_size + 1
                for row in printed_data_PDF:
                    for item in row:
                        pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
                    pdf.ln(row_height * spacing)
                pdf.set_y(-31)
                pdf.set_font("Arial", style="I", size=8)
                pageNum = "Page no. %s" % pdf.page_no()
                pdf.cell(0, 10, pageNum, align="C")
                pdf.output('Stock Report.pdf')
                os.startfile(".\Stock Report.pdf", "open")

            if self.select == 5:
                printed_data_PDF = [["S No.", "Date", "Item", "Quantity", "Address", "Bill No.", "Without GST", "GST", "Total Amount"]]
                self.d.execute("SELECT S_no,Date,Item_name,Quantity,Address,Bill_no,Without_gst,GST,Total_amount from conty where Deleted_date=''")
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_PDF.append(condata)
                pdf.set_font("Arial", style="B", size=15)
                pdf.cell(w=110)
                pdf.cell(60, 10, "..!! Bills Report !!..", border=1, ln=0, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=10)
                col_width = pdf.w / 9.9
                row_height = pdf.font_size + 1
                for row in printed_data_PDF:
                    for item in row:
                        pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
                    pdf.ln(row_height * spacing)
                pdf.set_y(-31)
                pdf.set_font("Arial", style="I", size=8)
                pageNum = "Page no. %s" % pdf.page_no()
                pdf.cell(0, 10, pageNum, align="C")
                pdf.output('Bills Report.pdf')
                os.startfile(".\Bills Report.pdf", "open")

            if self.select == 6:
                printed_data_PDF = [["S No.", "Date", "Time", "Department Name", "Item Name", "Item Pieces", "Name", "Phone No."]]
                self.d.execute("SELECT S_No,Date,Time,Dept_Name,Item_Name,Item_pieces,Name,Phone_No from issue where Deleted_date=''")
                fetch = self.d.fetchall()
                for data in fetch:
                    condata = list(data)
                    printed_data_PDF.append(condata)
                pdf.set_font("Arial", style="B", size=15)
                pdf.cell(w=100)
                pdf.cell(60, 10, "..!! Issue Report !!..", border=1, ln=0, align="C")
                pdf.ln(20)
                pdf.set_font("Arial", size=10)
                col_width = pdf.w / 8.9
                row_height = pdf.font_size + 1
                for row in printed_data_PDF:
                    for item in row:
                        pdf.cell(col_width, row_height * spacing, txt=str(item), border=1)
                    pdf.ln(row_height * spacing)
                pdf.set_y(-31)
                pdf.set_font("Arial", style="I", size=8)
                pageNum = "Page no. %s" % pdf.page_no()
                pdf.cell(0, 10, pageNum, align="C")
                pdf.output('Issue Report.pdf')
                os.startfile(".\Issue Report.pdf", "open")

    def __del__(self):
        try:os.remove(".\Stock Report.pdf")
        except:pass
        try:os.remove(".\Asset Report.pdf")
        except:pass
        try:os.remove(".\Stationary Report.pdf")
        except:pass
        try:os.remove(".\Bills Report.pdf")
        except:pass
        try:os.remove(".\Issue Report.pdf")
        except:pass
        try:os.remove(".\Stock Report.xlsx")
        except:pass
        try:os.remove(".\Asset Report.xlsx")
        except:pass
        try:os.remove(".\Stationary Report.xlsx")
        except:pass
        try:os.remove(".\Bills Report.xlsx")
        except:pass
        try:os.remove(".\Issue Report.xlsx")
        except:pass

# ========================== Main Window ==================
root = Tk()
obj = Inventory(root)
obj.first_screen()
style = ttk.Style()
style.theme_use('alt')
del obj
root.mainloop()
