from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow
from employee import EmployeeClass
from supplier import SupplierClass
from category import CategoryClass
from product import ProductClass
from sales import SalesClass
import sqlite3
from tkinter import messagebox
import os
import time

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x720+0+50")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='#0C3242')


        ## -------------------- title ------------------------------------------------PRIMER CAMBIO
        self.logo_image = Image.open("images/logo1.png")
        self.logo_image = self.logo_image.resize((60,60), Image.LANCZOS)  # Ajusta el tamaño según sea necesario
        self.icon_title = ImageTk.PhotoImage(self.logo_image)
        title = Label(self.root, text="SISTEMA DE GESTION", image=self.icon_title, compound=LEFT, font=("Bahnschrift", 47, "bold"), bg="#1A3949", fg="#FFFEFC", anchor="w", padx=20)
        title.place(x=0, y=-2, relwidth=1, height=80)
        ## -------------------- logout button ----------------------------------##aca hize otro cambio(mark)
        btn_logout=Button(self.root,text="LOGOUT",command=self.logout,font=("Lucida Console",15,"bold"),bg="#CD5C5C",fg="white").place(x=1100,y=10,height=50,width=100)

        ## clock
        self.lbl_clock=Label(self.root,text="Bienvenido\t\t Fecha: DD-MM-YYYY\t\t Time: HH-MM-SS",font=("times new roman",15,"bold"),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        ## -------------------- left menu ------------------------------------------------
        self.MenuLogo=Image.open("images/menu_im.png")
                ####Image.LANCZOS for high-quality downsampling
        self.MenuLogo=self.MenuLogo.resize((240,200),Image.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
## -------------------- color marco del menu --------------------------------------------------------------
        LeftMenu=Frame(self.root,bd=15,relief=RIDGE,bg="#0C3242") 
        LeftMenu.place(x=0,y=105,width=260,height=570)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=BOTTOM,fill=X)


        self.icon_side=PhotoImage(file="images/side.png")

        lbl_menu=Label(LeftMenu,text="Menu",font=("impact",30),bg="#0C3242",fg="white").pack(side=TOP,fill=X)

        btn_employee=Button(LeftMenu,text="EMPLOYEE",command=self.employee,image=self.icon_side,compound=LEFT,padx=10,anchor="w",font=("Lucida Console",20,"bold"),bg="#005871",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_supplier=Button(LeftMenu,text="SUPPLIER",command=self.supplier,image=self.icon_side,compound=LEFT,padx=10,anchor="w",font=("Lucida Console",20,"bold"),bg="#005871",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_category=Button(LeftMenu,text="CATEGORY",command=self.category,image=self.icon_side,compound=LEFT,padx=10,anchor="w",font=("Lucida Console",20,"bold"),bg="#005871",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_product=Button(LeftMenu,text="PRODUCT",command=self.product,image=self.icon_side,compound=LEFT,padx=10,anchor="w",font=("Lucida Console",20,"bold"),bg="#005871",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_sales=Button(LeftMenu,text="SALES",command=self.sales,image=self.icon_side,compound=LEFT,padx=10,anchor="w",font=("Lucida Console",20,"bold"),bg="#005871",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        btn_exit=Button(LeftMenu,text="EXIT",image=self.icon_side,compound=LEFT,padx=10,anchor="w",font=("Lucida Console",20,"bold"),bg="#005871",fg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)

        ## -------------------- content --------------------------------------------------------------------------------------------------------
        self.lbl_employee=Label(self.root,text="TOTAL EMPLOYED\n[ 0 ]",bd=3,relief=RIDGE,bg="#547071",fg="white",font=("Bahnschrift",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

        self.lbl_supplier=Label(self.root,text="TOTAL SUPPLIER\n[ 0 ]",bd=3,relief=RIDGE,bg="#688391",fg="white",font=("Bahnschrift",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=300)

        self.lbl_category=Label(self.root,text="TOTAL CATEGORY\n[ 0 ]",bd=3,relief=RIDGE,bg="#547071",fg="white",font=("Bahnschrift",20,"bold"))
        self.lbl_category.place(x=1000,y=120,height=150,width=300)

        self.lbl_product=Label(self.root,text="TOTAL PRODUCT\n[ 0 ]",bd=3,relief=RIDGE,bg="#688391",fg="white",font=("Bahnschrift",20,"bold"))
        self.lbl_product.place(x=450,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="TOTAL SALES\n[ 0 ]",bd=3,relief=RIDGE,bg="#B06161",fg="white",font=("Bahnschrift",20,"bold"))
        self.lbl_sales.place(x=800,y=300,height=150,width=300)
        

        ## -------------------- footer --------------------
        lbl_footer=Label(self.root,text="Sistema de Gestion | Desarollado por Grupo 5\nEn caso de Problemas Tecnicos contactar con +51 941 652 599",font=("times new roman",11,"bold"),bg="#4d636d",fg="white")
        lbl_footer.pack(side=BOTTOM,fill=X)

        self.update_content() 
#       -       -       -       -       -       -       -       -

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=EmployeeClass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SupplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=CategoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ProductClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SalesClass(self.new_win)
    
    #Agragado (Alexis)
    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"TOTAL PRODUCT\n[ {str(len(product))} ]")
            
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"TOTAL SUPPLIER\n[ {str(len(supplier))} ]")
            
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"TOTAL CATEGORY\n[ {str(len(category))} ]")
            
            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f"TOTAL EMPLOYED\n[ {str(len(employee))} ]")
            
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'TOTAL SALES\n [{str(bill)}]') #aca hize uncambio (mark)
            
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Bienvenido al Sistema de Gestion de Inventario\t\t Fecha: {str(date_)}\t\t Hora: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)
            
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    ##otro gran aporte de mark , pvta que eficiente este pata , demosle un premio 
    def logout(self):
        self.root.destroy()
        os.system("python login.py")   
         
    
if __name__=="__main__":
        root=Tk()
        obj=IMS(root)
        root.mainloop()
        