from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class SupplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1080x525+265+190")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='#547071')
        self.root.focus_force()
        # Eliminar los marcos de la ventana
        self.root.overrideredirect(True)
        ## All variables --------------------

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()

        ## -------------------- Search Frame --------------------
        ## -------------------- Options --------------------
        lbl_search=Label(self.root,text=" INVOICE N° ",bg="#688391",font=("Segoe UI",15),fg="white")
        lbl_search.place(x=680,y=72)
        
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("Segoe UI",15),bg="#C8DFE2").place(x=800,y=75,width=140)
        btn_search=Button(self.root,text="BUSCAR",command=self.search,font=("impact",20),bg="#424A61",fg="WHITE",cursor="hand2").place(x=950,y=65,width=118,height=48)

        ## -------------------- Title --------------------
        title=Label(self.root,text="Detalles del proveedor",font=("impact",25),bg="#203B47",fg="WHITE").place(x=50,y=10,width=1000,height=40)

        ## -------------------- Content --------------------
        ## row 1 *****************************
        lbl_supplier_invoice=Label(self.root,text="  INVOICE N°  ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=80)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("Segoe UI",15),bg="#C8DFE2").place(x=180,y=80,width=180)

        ## row 2 *****************************
        lbl_name=Label(self.root,text="      NAME       ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("Segoe UI",15),bg="#C8DFE2").place(x=180,y=120,width=180)

        ##row 3 *****************************
        lbl_contact=Label(self.root,text="  CONTACTO  ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("Segoe UI",15),bg="#C8DFE2").place(x=180,y=160,width=180)

        ##row 4 *****************************
        lbl_desc=Label(self.root,text="DESCRIPCION ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("Segoe UI",15),bg="#C8DFE2")
        self.txt_desc.place(x=180,y=200,width=470,height=120)

        ## -------------------- buttons --------------------
        btn_add=Button(self.root,text="Guardar",command=self.add,font=("IMPACT",15),bg="#072531",fg="White",cursor="hand2").place(x=180,y=370,width=110,height=30)
        btn_update=Button(self.root,text="Actualizar",command=self.update,font=("IMPACT",15),bg="#4F6A77",fg="White",cursor="hand2").place(x=300,y=370,width=110,height=30)
        btn_delete=Button(self.root,text="Eliminar",command=self.delete,font=("IMPACT",15),bg="#872341",fg="White",cursor="hand2").place(x=420,y=370,width=110,height=30)
        btn_clear=Button(self.root,text="Limpiar",command=self.clear,font=("IMPACT",15),bg="#37525F",fg="White",cursor="hand2").place(x=540,y=370,width=110,height=30)

        ## -------------------- Supplier Details --------------------
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=680,y=120,width=380,height=350)

## -------------------- ESTE PEDAZO AGREGA COLOR DE FONDO  ---
        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        background="#C8DFE2", 
                        fieldbackground="#C8DFE2", 
                        foreground="black",
                        rowheight=25)
        style.map("mystyle.Treeview", 
                background=[('selected', '#6A8E7F')], 
                foreground=[('selected', 'white')])

        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set, style="mystyle.Treeview")

        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("invoice",text="Invoice N°")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")

        self.SupplierTable["show"]="headings"

        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        self.SupplierTable.pack(fill=BOTH,expand=1)

        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
        
#       -       -       -       -       -       -       -       -
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice Must be required",parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Este N° factura ya ha sido asignado, intente otra",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                            self.var_sup_invoice.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Proveedor agregado satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

#-
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
#-

#-
    def get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),
#-

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Se necesita un N° Factura",parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","N° factura invalido",parent=self.root)
                else:
                    cur.execute("UPDATE supplier SET name=?,contact=?,desc=? WHERE invoice=?",(
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get('1.0',END),
                            self.var_sup_invoice.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Proveedor actualizado satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Se necesita N° factura",parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","N° Factura invalido",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","¿Estas seguro de eliminarlo?",parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM supplier WHERE invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Proveedor eliminado satisfactoriamente",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END)
        
        self.var_searchtxt.set("")
    
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Se necesita N° Factura",parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row != None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No se encontro registro!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
        root=Tk()
        obj=SupplierClass(root)
        root.mainloop()