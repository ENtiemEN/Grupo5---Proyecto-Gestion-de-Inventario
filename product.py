from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class ProductClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1080x525+265+190")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='#688391')
        self.root.focus_force()
        # Eliminar los marcos de la ventana
        self.root.overrideredirect(True)
        ## All variables --------------------
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()

        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        ## ================================

        product_Frame=Frame(self.root,bd=5,relief=RIDGE,bg="#4F6A77")
        product_Frame.place(x=10,y=10,width=456,height=480)

        title=Label(product_Frame,text="GESTIONAR DETALLES DEL PRODUCTO",font=("IMPACT",18),bg="#072531",fg="WHITE").pack(side=TOP,fill=X)
        

        ## ============= column 1 ============= 
        lbl_category=Label(product_Frame,text="CATEGORIA           ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="PROVEDOR            ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=30,y=110)
        lbl_name=Label(product_Frame,text="PRODUCTO           ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="PRECIO                  ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="CANTIDAD             ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="ESTADO                  ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=30,y=310)

        ## ============= column 2 ============= 
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",14))
        cmb_cat.place(x=200,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",14))
        cmb_sup.place(x=200,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="#C8DFE2").place(x=200,y=160,width=200)

        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="#C8DFE2").place(x=200,y=210,width=200)

        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="#C8DFE2").place(x=200,y=260,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",14))
        cmb_status.place(x=200,y=310,width=200)             #Modificación linea 61 ACTIVE INACTIVE lo cambia a minuscula, habia un error en billing(Alexis)
        cmb_status.current(0)

        ## =================== buttons ===================
        btn_add=Button(product_Frame,text="GUARDAR",command=self.add,font=("IMPACT",15),bg="#072531",fg="White",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="ACTUALIZAR",command=self.update,font=("IMPACT",15),bg="#4F6A77",fg="White",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="ELIMINAR",command=self.delete,font=("IMPACT",15),bg="#872341",fg="White",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="LIMPIAR",command=self.clear,font=("IMPACT",15),bg="#37525F",fg="White",cursor="hand2").place(x=340,y=400,width=100,height=40)

        ## -------------------- Search Frame --------------------
        SearchFrame = LabelFrame(self.root,text="BUSCAR PRODUCTO",font=("goudy old style",12,"bold"),fg="white",bd=4,relief=RIDGE,bg="#37525F")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        ## -------------------- Options --------------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("SELECT","CATEGORY","SUPPLIER","NAME"),state='readonly',justify=CENTER,font=("goudy old style",14))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="#C8DFE2").place(x=200,y=10)

        btn_search=Button(SearchFrame,text="BUSCAR",command=self.search,font=("impact",15),bg="#424A61",fg="WHITE",cursor="hand2").place(x=430,y=1,width=150,height=40)

        ## ========================== Product Details ==========================
        pro_frame=Frame(self.root,bd=3,relief=RIDGE)
        pro_frame.place(x=480,y=100,width=600,height=390)

        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        background="#C8DFE2", 
                        fieldbackground="#C8DFE2", 
                        foreground="black",
                        rowheight=25)
        style.map("mystyle.Treeview", 
                background=[('selected', '#6A8E7F')], 
                foreground=[('selected', 'white')])


        scrolly=Scrollbar(pro_frame,orient=VERTICAL)
        scrollx=Scrollbar(pro_frame,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(pro_frame,columns=("pid","category","supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set, style="mystyle.Treeview")

        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("pid",text="Prod ID")
        self.ProductTable.heading("category",text="Categoria")
        self.ProductTable.heading("supplier",text="Proveedor")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Precio")
        self.ProductTable.heading("qty",text="Cantidad")
        self.ProductTable.heading("status",text="Estado")

        self.ProductTable["show"]="headings"

        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("category",width=100)
        self.ProductTable.column("supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)

        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
        self.fetch_cat_sup()

## ===================== Functions =====================

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("SELECT")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("SELECT name FROM supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("SELECT")
                for i in sup:
                    self.sup_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","Se necesita completar todos los registros",parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name=? AND supplier=?",(self.var_name.get(),self.var_sup.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","El producto ya se encuentra, intente uno diferente",parent=self.root)
                else:
                    cur.execute("Insert into product (category,supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Producto agregado satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        print(row)
        self.var_pid.set(row[0])
        self.var_sup.set(row[1]),    #Modificación:Se  movieron dos filas(Alexis)
        self.var_cat.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Selecciona un producto de la lista",parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Producto ID ivalido",parent=self.root)
                else:
                    cur.execute("UPDATE product SET category=?,supplier=?,name=?,price=?,qty=?,status=? WHERE pid=?",(
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Producto actualizado satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Seleccione un producto de la lista",parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Producto ID invalido",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","¿Realmente quieres eliminarlo?",parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM product WHERE pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Producto eliminado satisfactoriamente",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set(""),
        self.var_searchby.set("Select"),
        self.var_searchtxt.set(""),

        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No se encontro registro!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)



if __name__=="__main__":
        root=Tk()
        obj=ProductClass(root)
        root.mainloop()