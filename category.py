from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class CategoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1080x525+265+190")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='#688391')
        self.root.focus_force()
        # Eliminar los marcos de la ventana
        self.root.overrideredirect(True)
        ## Variables --------------------

        self.var_cat_id=StringVar()
        self.var_name=StringVar()


        ## -------------------- Title --------------------
        lbl_title=Label(self.root,text="GESTIONAR CATEGORIA DE PRODUCTO",font=("impact",30),bg="#072531",fg="WHITE",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=2)

        lbl_name=Label(self.root,text="                          NOMBRE DE CATEGORIA                               ",font=("impact",25),bg="#203B47",fg="#C8DFE2").place(x=50,y=100)
        txt_name=Entry(self.root,text=self.var_name,font=("goudy old style",20),bg="#C8DFE2").place(x=50,y=170,width=300)

        btn_add=Button(self.root,text="AGREGAR",command=self.add,font=("IMPACT",18),bg="#37525F",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="ELIMINAR",command=self.delete,font=("IMPACT",15),bg="#872341",fg="White",cursor="hand2").place(x=520,y=170,width=150,height=30)

        ## -------------------- Category Details --------------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=340,height=140)

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
        

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set, style="mystyle.Treeview")

        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid",text="Cat ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"
        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        self.CategoryTable.pack(fill=BOTH,expand=1)

        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)

        ## -------------------- Images -------------------- 
        self.im1=Image.open("images/cat.jpg")
        self.im1=self.im1.resize((500,200),Image.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)

        self.lbl_im1=Label(self.root,image=self.im1,bd=6,relief=RAISED,bg="#0C3242")
        self.lbl_im1.place(x=50,y=250)

        self.im2=Image.open("images/category.jpg")
        self.im2=self.im2.resize((450,200),Image.LANCZOS)
        self.im2=ImageTk.PhotoImage(self.im2)

        self.lbl_im2=Label(self.root,image=self.im2,bd=6,relief=RAISED,bg="#0C3242")
        self.lbl_im2.place(x=580,y=250)

        self.show()

## ============================ Functions ============================ 

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Se necesita Nombre de Categoria",parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Categoria ya asignada, intente otra",parent=self.root)
                else:
                    cur.execute("Insert into category (name) values(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Categoria agregada satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0]),
        self.var_name.set(row[1]),

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Ingrese una categoria",parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","categoria invalida",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","¿Estas seguro de eliminarlo?",parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM category WHERE cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Categoria eliminada satisfactoriamente",parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
        root=Tk()
        obj=CategoryClass(root)
        root.mainloop()