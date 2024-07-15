from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk #python -m pip install pillow
from tkinter import ttk,messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import time
import os
import tempfile
import smtplib


class BillClass:

    def __init__(self,root):
        self.root=root
        self.root.geometry("1385x720+0+50")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='#0C3242')
        self.cart_list=[]
        self.chk_print=0
        self.var_descuento=StringVar()
        self.var_descuento.set('0')
         # Definimos el estilo para Treevi 
        style = ttk.Style()
        style.configure("mystyle.Treeview", 
                        background="#95A1A4",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="BLACK")
        
        style.map('mystyle.Treeview', background=[('selected', '#347083')])
      
        
        style.configure("mystyle.Treeview.Heading",
                background="darkblue",  # Color de fondo de las cabeceras
                foreground="black",  # Color del texto de las cabeceras
                font=("Bahnschrift",11,"bold"),bg="red",fg="red")  # Fuente de las cabeceras
    
        ## -------------------- title --------------------PRIMER CAMBIO
        self.logo_image = Image.open("images/logo1.png")
        self.logo_image = self.logo_image.resize((60,60), Image.LANCZOS)  # Ajusta el tamaño según sea necesario
        self.icon_title = ImageTk.PhotoImage(self.logo_image)
        title = Label(self.root, text="SISTEMA DE GESTION", image=self.icon_title, compound=LEFT, font=("Bahnschrift", 47, "bold"), bg="#1A3949", fg="#FFFEFC", anchor="w", padx=20)
        title.place(x=0, y=-2, relwidth=1, height=80)
        ## -------------------- logout button --------------------#aca tambien toquetie algo (mark)
        btn_logout=Button(self.root,text="LOGOUT",command=self.logout,font=("Lucida Console",15,"bold"),bg="#8C3027",fg="white").place(x=1270,y=10,height=50,width=100)
        ## clock
        self.lbl_clock=Label(self.root,text="Bienvenido\t\t Fecha: DD-MM-YYYY\t\t Time: HH-MM-SS",font=("times new roman",15,"bold"),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        ##---------------Product Frame--------------------------
        ProductFrame1= Frame(self.root,bd=4,relief=RIDGE)  # Cambia aquí el color de fondo
        ProductFrame1.config(bg="#38646E") 
        ProductFrame1.place(x=6,y=110,width=410,height=550) #COLOR FRAME 3 
        pTitle=Label(ProductFrame1,text=" INVENTARIO ",font=("Bahnschrift",20,"bold"),bg="#3D4655",fg="white").pack(side=TOP,fill=X) 
        lbl_note=Label(text="PRESIONA PARA AGREGAR AL CARRITO",font=("goudy old style",10,'bold'),anchor='w',bg="#395D5A",fg="white").place(x=10,y=215)  # Cambia aquí el color de fondo
        # #------------Product Search Frame-------------------------------
        #Definimos  self.var_search antes de usarlo (Agragado extra)
        self.var_search = StringVar()   #Realicé esto porque me slaia un error (Alexis)
        ProductFrame2= Frame(ProductFrame1,bd=0,relief=RIDGE,bg="#26454C")  # Cambia aquí el color de fondo
        ProductFrame2.place(x=2,y=42,width=398,height=90) #FRAME DE BUSCAR
        #lbl_search=Label(ProductFrame2,text="Buscar Producto | Por nombre  ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        lbl_search=Label(ProductFrame2,text="BUSCAR",font=("Bahnschrift",15),bg="#26454C",fg="white").place(x=2 ,y=15)  # Cambia aquí el color de fondo
        #Sucedió un error porque  self.var_search no estaba definido(se arregló)
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("Bahnschrift",15),bg="lightgray").place(x=100,y=15,width=230,height=22)
        btn_search=Button(ProductFrame2,text="🔎",command=self.search,font=("goudy old style",18,"bold"),bg="#106963",fg="white",cursor="hand2").place(x=338,y=10,width=48,height=30)
        btn_show_all=Button(ProductFrame2,text="MOSTRAR TODO",command=self.show,font=("Bahnschrift",11),bg="#083531",fg="white",cursor="hand2").place(x=265,y=56,width=130,height=28)
        #------------Product Details Frame-------------------------------
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE, bg="black")  # Cambia aquí el color de fondo POSICION DEL FRAME DE PRODUCTOS
        ProductFrame3.place(x=2,y=140,width=398,height=175)
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL) 
        self.product_Table = ttk.Treeview(ProductFrame3,
                                  columns=("pid", "name", "price", "qty", "status"),
                                  yscrollcommand=scrolly.set,
                                  xscrollcommand=scrollx.set,
                                  style="mystyle.Treeview")  # Aplica el estilo personalizado aquí
        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.product_Table.xview)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="NOMBRE")
        self.product_Table.heading("price",text="PRECIO(s/.)")
        self.product_Table.heading("qty",text="CANT.")
        self.product_Table.heading("status",text="ESTADO")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40, anchor='center')
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100, anchor='center')
        self.product_Table.column("qty",width=60, anchor='center')
        self.product_Table.column("status",width=80, anchor='center')
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)
        
        
        #===========DETALLES DEL CLIENTE FRAME===========
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_celu=StringVar()
        CustomerFrame= Frame(self.root,bd=4,relief=RIDGE,bg="#26454C")
        CustomerFrame.place(x=420,y=110,width=540,height=105)
        cTitle=Label(CustomerFrame,text="DETALLES DEL CLIENTE",font=("Bahnschrift",20,"bold"),bg="#3D4655",fg="white").pack(side=TOP,fill=X)
        lbl_name=Label(CustomerFrame,text="NOMBRE",font=("Bahnschrift",15),bg="#26454C",fg="white").place(x=5 ,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("Bahnschrift",13),bg="lightgray").place(x=100,y=35,width=180)
        lbl_contact=Label(CustomerFrame,text="DNI",font=("Bahnschrift",15),bg="#26454C",fg="white").place(x=290,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("Bahnschrift",13),bg="lightgray").place(x=340,y=35,width=180)
        lbl_contact=Label(CustomerFrame,text="CORREO",font=("Bahnschrift",14),bg="#26454C",fg="white").place(x=5,y=65)
        txt_p_qty=Entry(CustomerFrame,textvariable=self.var_email,font=("Bahnschrift",13),bg="lightgray",fg="black").place(x=100,y=65,width=180)
        lbl_contact=Label(CustomerFrame,text="CEL",font=("Bahnschrift",15),bg="#26454C",fg="white").place(x=290,y=65)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_celu,font=("Bahnschrift",13),bg="lightgray").place(x=340,y=65,width=180)
        # -----------Calculator frame-------------
        Cal_Cart_Frame = Frame(self.root, bd=0, relief=RIDGE)
        Cal_Cart_Frame.place(x=13, y=425, width=396, height=228)
        self.var_cal_input = StringVar()
        Cal_Frame = Frame(Cal_Cart_Frame, relief=RIDGE, bg="#252A2C")
        Cal_Frame.place(x=0, y=0, width=396, height=228)

        # Ajustar el Entry de la calculadora
        self.txt_cal_input = Entry(Cal_Frame, textvariable=self.var_cal_input, font=("Bahnschrift", 15, "bold"), bd=5, relief=GROOVE, state="readonly", justify=RIGHT)
        self.txt_cal_input.grid(row=0, columnspan=4, ipadx=70, ipady=5, pady=5)

        # Crear los botones de la calculadora
        btn_7 = Button(Cal_Frame, text='7', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(7))
        btn_8 = Button(Cal_Frame, text='8', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(8))
        btn_9 = Button(Cal_Frame, text='9', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(9))
        btn_sum = Button(Cal_Frame, text='+', font=("Bahnschrift", 15, "bold"),bg="#3E5357",fg="white", command=lambda: self.get_input('+'))
        btn_4 = Button(Cal_Frame, text='4', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(4))
        btn_5 = Button(Cal_Frame, text='5', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(5))
        btn_6 = Button(Cal_Frame, text='6', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(6))
        btn_sub = Button(Cal_Frame, text='-', font=("Bahnschrift", 15, "bold"),bg="#3E5357",fg="white", command=lambda: self.get_input('-'))
        btn_1 = Button(Cal_Frame, text='1', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(1))
        btn_2 = Button(Cal_Frame, text='2', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(2))
        btn_3 = Button(Cal_Frame, text='3', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(3))
        btn_mul = Button(Cal_Frame, text='x', font=("Bahnschrift", 15, "bold"),bg="#3E5357",fg="white", command=lambda: self.get_input('*'))
        btn_0 = Button(Cal_Frame, text='0', font=("Bahnschrift", 15, "bold"), command=lambda: self.get_input(0))
        btn_c = Button(Cal_Frame, text='BORRAR', font=("Bahnschrift", 8, "bold"),bg="#3E5357",fg="white", command=self.clear_cal)
        btn_eq = Button(Cal_Frame, text='=', font=("Bahnschrift", 15, "bold"),bg="#8F4962",fg="white",  command=self.perform_cal)
        btn_div = Button(Cal_Frame, text='/', font=("Bahnschrift", 15, "bold"),bg="#3E5357",fg="white", command=lambda: self.get_input('/'))

        # Distribuir los botones en la cuadrícula
        buttons = [
            [btn_7, btn_8, btn_9, btn_sum],
            [btn_4, btn_5, btn_6, btn_sub],
            [btn_1, btn_2, btn_3, btn_mul],
            [btn_0, btn_c, btn_eq, btn_div]
        ]

        for i, row in enumerate(buttons):
            for j, button in enumerate(row):
                button.grid(row=i+1, column=j, ipadx=10, ipady=10, padx=5, pady=5)

        # Definir los tamaños de las columnas y filas para que ocupen todo el espacio
        for i in range(4):
            Cal_Frame.columnconfigure(i, weight=1)
            Cal_Frame.rowconfigure(i+1, weight=1)
        #----------Cart Frame---------------
        Cart_Frame = Frame(self.root, bd=1, relief=RIDGE)
        Cart_Frame.place(x=420, y=217, width=540, height=305)  # UBICACION FRAME CARRITO
        self.cartTitle = Label(Cart_Frame, text="CARRITO        DE \t PRODUCTOS: [0]              ", font=("Bahnschrift", 15), bg="lightgray")
        self.cartTitle.pack(side=TOP, fill=X)
        btn_clear_all=Button(text='VACIAR CARRITO',command=self.clear_all,cursor='hand2',font=("Bahnschrift",10,"bold"),bg="orange",fg="black").place(x=850, y=218)
        scrolly = Scrollbar(Cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(Cart_Frame, orient=HORIZONTAL)
        self.CartTable=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set, style="mystyle.Treeview")
        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.CartTable.xview)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid",text="PID")
        self.CartTable.heading("name",text="PRODUCTO")
        self.CartTable.heading("price",text="PRECIO (s/.)")
        self.CartTable.heading("qty",text="CANT.")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid", width=14, anchor='center')
        self.CartTable.column("name", width=240, anchor='center')
        self.CartTable.column("price", width=90, anchor='center')
        self.CartTable.column("qty", width=40, anchor='center')
        self.CartTable.pack(fill=BOTH,expand=2)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        #--------ADD Cart Widgets Frame---------------------
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        
        #==========frame limpiar agregar carrito=============
        lbl_note=Label(text="     NOTA  :    RECUERDA QUE ERES REEMPLAZABLE                                      ",font=("goudy old style",11,'bold'),anchor='w',bg="#657A6C",fg="white").place(x=420,y=525)  # Cambia aquí el color de fondo
        Add_CartWidgetsFrame= Frame(self.root,bd=4,relief=RIDGE,bg="#0C3242")#color de fondo 
        Add_CartWidgetsFrame.place(x=420,y=550,width=540,height=110)
        lbl_p_name=Label(Add_CartWidgetsFrame,text="PRODUCTO",font=("Bahnschrift",15),bg="#0C3242",fg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartWidgetsFrame,textvariable=self.var_pname,font=("Bahnschrift",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)
        lbl_p_price=Label(Add_CartWidgetsFrame,text="PRECIO",font=("Bahnschrift",15),bg="#0C3242",fg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartWidgetsFrame,textvariable=self.var_price,font=("Bahnschrift",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=130,height=22)
        lbl_p_qty=Label(Add_CartWidgetsFrame,text="CANTIDAD",font=("Bahnschrift",15),bg="#0C3242",fg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartWidgetsFrame,textvariable=self.var_qty,font=("Bahnschrift",15),bg="lightyellow", justify="center",fg="black").place(x=375,y=35,width=130,height=22)
        self.lbl_inStock=Label(Add_CartWidgetsFrame,text="EN STOCK",font=("Bahnschrift",15),bg="#0C3242",fg="white")
        self.lbl_inStock.place(x=5,y=70)
        btn_clear_cart=Button(Add_CartWidgetsFrame,text="     🗑️",command=self.clear_cart,font=("Bahnschrift",15),bg="orange",cursor="hand2").place(x=130,y=5,width=50,height=28)  
        btn_add_cart=Button(Add_CartWidgetsFrame,text="AGREGAR  ",command=self.add_update_cart,font=("Bahnschrift",15,"bold"),bg="orange",cursor="hand2").place(x=230,y=67,width=140,height=30)  
        btn_delete_car=Button(Add_CartWidgetsFrame,text="QUITAR ",command=self.delete_car,font=("Bahnschrift",15,"bold"),bg="orange",cursor="hand2").place(x=370,y=67,width=140,height=30)  
        lbl_name=Label(Add_CartWidgetsFrame,text="S/.",font=("Bahnschrift",15),bg="#EBEDF0",fg="black").place(x=328,y=36,height=20)
        #---------------Billing area--------------------------------------
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=967,y=110,width=410,height=400)  #UBICACION FRAME BOLETA
        BTitle=Label(billFrame,text="BOLETA",font=("Bahnschrift",20,"bold"),bg="#3D4655",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set, bg="#B1C1D1")  # Cambia aquí el color de fondo
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        btn_clear_bill = Button(billFrame, text='LIMPIAR \n BOLETA', command=self.limpiarboleta, cursor='hand2', font=("Bahnschrift", 12, "bold"), bg="#FF5733", fg="white")
        btn_clear_bill.place(x=285, y=43, width=100, height=50)          
        #-----------------------Billing buttons-------------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='#26454C')
        billMenuFrame.place(x=967,y=520,width=410,height=140)
        self.lbl_amnt=Label(billMenuFrame,text='MONTO \n TOTAL\n [ 0 ]',font=("goudy old style",13,"bold"),bg="#4C5F79",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)
        self.lbl_net_pay=Label(billMenuFrame,text='PAGO CON\n DESCUENTO\n[ 0 ]',font=("goudy old style",13,"bold"),bg="#3A4758",fg="white")
        self.lbl_net_pay.place(x=124,y=5,width=120,height=70)
    
        btn_print=Button(billMenuFrame,text='IMPRIMIR',command=self.print_bill,cursor='hand2',font=("Bahnschrift",15,"bold"),bg="#9CAEAC",fg="BLACK")
        btn_print.place(x=2,y=80,width=120,height=50)
        btn_email_bill = Button( billMenuFrame,text='ENVIAR BOLETA \n POR CORREO', command=self.send_bill_email, cursor='hand2', font=("Bahnschrift", 11, "bold"),bg="orange",fg="black")
        btn_email_bill.place(x=124,y=80,width=120,height=50)
        btn_generate=Button(billMenuFrame,text='GENERAR BOLETA \n GUARDAR',command=self.generate_bill,cursor='hand2',font=("Bahnschrift",13,"bold"),bg="orange",fg="black")
        btn_generate.place(x=246,y=80,width=156,height=50)
        btn_generate=Button(billMenuFrame,text='APLICAR \n DESCUENTO',command=self.apply_discount,cursor='hand2',font=("Bahnschrift",13),bg="#3E543E",fg="WHITE")
        btn_generate.place(x=246,y=5,width=156,height=40)
        # txt_p_price=Entry(billMenuFrame,textvariable=self.var_descuento ,font=("Bahnschrift",15),bg="lightyellow",state='readonly').place(x=30,y=35,width=128,height=22)
        #Descuento
        txt_p_qty=Entry(billMenuFrame,textvariable=self.var_descuento,font=("Bahnschrift",13),bg="lightgray",fg="black", justify="center").place(x=246,y=47,width=155,height=28)  
        lbl_name=Label(billMenuFrame,text="%",font=("Bahnschrift",16),bg="lightgray",fg="black").place(x=360,y=50,height=20)
        
        #----------------Footer-----------------------------------
        footer=Label(self.root,text="SGI-Sistema  de Gestión de Inventario | Desarrollado por Grupo 5 - Base 22\nComputación Científica-UNMSM",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.show()
        # self.bill_top()
        self.update_date_time()
#----------------------------FUNCIONES-----------------------------
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)       
    def clear_cal(self):
        self.var_cal_input.set('')       
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))     
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT pid,name,price,qty,status FROM product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)  
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            else:
                cur.execute("SELECT pid,name,price,qty,status FROM product WHERE name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No se encontro registro!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"En Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        #pid,name,price,qty,stock
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"En Stock [{str(row[4])}]")
        self.var_stock.set(row[4])     
    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Por favor selecciona algo de la Lista", parent=self.root)
        elif self.var_qty.get() == '':
            messagebox.showerror('Error', "cantidad es requerida", parent=self.root) 
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Error', "Invalid Quantity", parent=self.root)         
        else:   
            price_cal = self.var_price.get()
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
            
            # ---------------- Check if product is already in the cart -----------------------------    
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    messagebox.showerror('Error', "Product is already in the cart", parent=self.root)
                    return

            # If the product is not in the cart, add it
            self.cart_list.append(cart_data)
            # Add the new item to the CartTable
            self.CartTable.insert("", 'end', values=(self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()))

            self.bill_updates()  # Update billing information
    def delete_car(self):

        if self.var_pid.get() == '':
            messagebox.showerror('Error', "Please select product from the list", parent=self.root)
        else:
        # price_cal = self.var_price.get()
        # cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]
        
        # ---------------- Update_cart -----------------------------    
            present = 'no'
            index_ = 0
        for i, row in enumerate(self.cart_list):
            if self.var_pid.get() == row[0]:
                present = 'yes'
                index_ = i
                break

        if present == 'yes':
            op = messagebox.askyesno('Confirm', "Do you want to remove the selected product from the Cart List?", parent=self.root)    
            if op == True:
                self.cart_list.pop(index_)  # Remove item from the cart list
                # Also remove the item from the CartTable
                selected_item = self.CartTable.selection()[0]  # Get selected item
                self.CartTable.delete(selected_item)  # Delete the selected item from the table
        else:
            messagebox.showerror('Error', "Product not in the cart", parent=self.root)

        self.bill_updates()  # Update billing information
    def bill_updates(self):
        
        self.bill_amnt = 0
        self.net_pay = 0  
        discount_value = self.var_descuento.get()
        try:
            self.discount = float(discount_value) if discount_value else 0.0
        except ValueError:
            self.discount = 0  
        for row in self.cart_list:
            self.bill_amnt += (float(row[2]) * int(row[3]))
        self.discount = (self.bill_amnt * self.discount) / 100
        self.net_pay = self.bill_amnt - self.discount
        self.lbl_amnt.config(text=f'MONTO TOTAL\n{str(self.bill_amnt)}     .S/',font='Bahnschrift')
        self.lbl_net_pay.config(text=f'PAGO CON \nDESCUENTO\n{str(self.net_pay)}     .S/',font='Bahnschrift')       
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)  
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':        
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)  
        else:
            #=======Bill Top==========
            self.bill_top()  
            #=======Bil Middle========
            self.bill_middle()
            #=======Bill Bottom========
            self.bill_bottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been generated/Save in Backend",parent=self.root)
            self.chk_print=1  
    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
    \t       Voleta
  No. Celular 98725**** , Lima 
{str("="*47)}
Nombre de cliente: {self.var_cname.get()}
No Cel.: {self.var_contact.get()}
No. factura: {str(self.invoice)}\t\tFecha: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
Nombre del prod.\t\tCant.\tPrecio
{str("="*47)} 
'''
        self.txt_bill_area.delete('1.0', END)
        self.txt_bill_area.insert('1.0', bill_top_temp)
    def bill_bottom(self):
        discount_percentage = self.var_descuento.get() if self.var_descuento.get() else "0"
        bill_bottom_temp = f''' 
        
        
{str("="*47)} 
Total de la factura\tS/.{self.bill_amnt}
Descuento {discount_percentage} % \t\tS/.{self.discount}
Pago Neto\t\tS/.{self.net_pay}        
{str("="*47)}\n
'''     
        self.txt_bill_area.insert(END, bill_bottom_temp)
        self.txt_bill_area.config(state=DISABLED) 
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                # pid,name,price,qty,stock
                
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'       
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+row[3]+"\tS/."+price)
                #------------update qty in product table--------------------
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                    
                ))
                con.commit()
            con.close()
            self.show()    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)       
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"EN STOCK",font=('Bahnschrift'))
        self.var_stock.set('')  
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('') 
        self.var_contact.set('')  
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"CARRITO        DE \t PRODUCTOS: [0]              ")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0  #Agregé intrucción  (Alexis)             
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Bienvenido al Sistema de Gestion de Inventario\t\t Fecha: {str(date_)}\t\t Hora: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)  
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('Print',"Please generate bill, to print the receipt",parent=self.root)        
    #Algunos botones extras  (mark)
    def logout(self):
        self.root.destroy()
        os.system("python login.py")        
    def send_bill_email(self):
        qty_value = self.var_email.get()
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror("Error", "Los detalles del cliente son necesarios", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror("Error", "Por favor, agregue productos al carrito", parent=self.root)
        else:
            # Obtener el contenido de la boleta
            bill_content = self.txt_bill_area.get('1.0', END)
            recipient_email = qty_value  
            # Configurar el correo electrónico
            sender_email = "markquispegonzales@outlook.es"
            sender_password = "gjjzjhcnisqvetka"
            subject = "Boleta de Compra"
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(bill_content, 'plain'))

            try:
                # Configurar el servidor SMTP
                server = smtplib.SMTP('smtp.office365.com', 587)  
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, recipient_email, text)
                server.quit()
                messagebox.showinfo("Éxito", "La boleta ha sido enviada por correo", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo enviar el correo\n{str(e)}", parent=self.root)
    def apply_discount(self):
            messagebox.showinfo("Éxito", "DESCUENTO APLICADO IMPRIMA LA BOLETA", parent=self.root)
            self.bill_updates()
    def limpiarboleta(self):
        # Habilitar el área de texto para permitir la eliminación
        self.txt_bill_area.config(state=NORMAL)
        # Limpiar el área de texto
        self.txt_bill_area.delete('1.0', END)
        # Deshabilitar el área de texto después de limpiarla si es necesario
    
        
        # Resetear variables de facturación
        self.cart_list.clear()  # Limpiar la lista del carrito
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        
        # Limpiar los campos de entrada del cliente
        self.var_cname.set('')
        self.var_contact.set('')
        self.var_email.set('')
        self.var_celu.set('')
        
        
        # Limpiar el contenido del carrito
        self.show_cart()
        
        # Habilitar el botón de generar boleta si está deshabilitado
        self.btn_generate.config(state=NORMAL)
        
        # Reiniciar el área de texto de la boleta para permitir nuevas entradas
        self.txt_bill_area.config(state=NORMAL)

        # Reiniciar el estado de cualquier otra variable o widget relacionado con la generación de boletas
        self.chk_print = 0
        self.var_descuento.set('0')
        self.bill_no = ''  # Si tienes una variable para el número de boleta, reiníciala aquí

        self.update()
             
if __name__=="__main__":
     root=Tk()
     obj=BillClass(root)    
     root.mainloop()
