from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class EmployeeClass:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1050x525+275+190")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='#547071')## COLORRRRRRRRRRR1 --------------------
        self.root.focus_force()
     # Eliminar los marcos de la ventana
        self.root.overrideredirect(True)
        ## All variables --------------------

        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()

        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()

        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()

        self.var_salary=StringVar()

        ## -------------------- Search Frame --------------------
        SearchFrame = LabelFrame(self.root,text="BUSCAR EMPLEADO",font=("goudy old style",12,"bold"),fg="white",bd=3,relief=RIDGE,bg="#316078")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        ## -------------------- Options --------------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("SELECT","Email","Name","Contact"),state='readonly',justify=CENTER,font=("Bahnschrift",14))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("Constantia",15),bg="#C8DFE2").place(x=200,y=10)

        btn_search=Button(SearchFrame,text="Buscar",command=self.search,font=("impact",15),bg="#072531",fg="#C2D9FF",cursor="hand2").place(x=410,y=9,width=150,height=30)

        ## -------------------- Title --------------------
        title=Label(self.root,text="DETALLES DEL EMPLEADO",font=("SEGOE UI",15),bg="#203B47",fg="white").place(x=50,y=100,width=1000)

        ## -------------------- Content --------------------
        ## row 1 *****************************
        lbl_empid=Label(self.root,text="EMP ID                                            ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="GENDER                                                    ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=350,y=150)
        lbl_contact=Label(self.root,text="CONTACT                                        ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=750,y=150)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15),bg="#C8DFE2").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("SELECT","MALE","FEMALE","OTHER"),state='readonly',justify=CENTER,font=("goudy old style",14))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="#C8DFE2").place(x=850,y=150,width=180)

        ## row 2 *****************************
        lbl_name=Label(self.root,text="NAME                                             ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="D.O.B                                                         ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=350,y=190)
        lbl_doj=Label(self.root,text="D.O.J                                                ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="#C8DFE2").place(x=150,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="#C8DFE2").place(x=500,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="#C8DFE2").place(x=850,y=190,width=180)

        ##row 3 *****************************
        lbl_email=Label(self.root,text="EMAIL                                             ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="PASSWORD                                             ",font=("Segoe UI",15),bg="#688391",fg="white").place(x=350,y=230)
        lbl_utype=Label(self.root,text="USER TYPE                                        ",font=("Segoe UI",13),bg="#688391",fg="white").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="#C8DFE2").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="#C8DFE2").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Admin","Employee"),state='readonly',justify=CENTER,font=("goudy old style",14))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)

        ##row 4 *****************************
        lbl_address=Label(self.root,text="ADDRESS",font=("goudy old style",15),bg="#688391",fg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="SALARY                                  ",font=("goudy old style",15),bg="#688391",fg="white").place(x=500,y=270)

        self.txt_address=Text(self.root,font=("goudy old style",15),bg="#C8DFE2")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("goudy old style",15),bg="#C8DFE2").place(x=600,y=270,width=180)

        ## -------------------- buttons --------------------
        btn_add=Button(self.root,text="GUARDAR",command=self.add,font=("IMPACT",15),bg="#072531",fg="White",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_update=Button(self.root,text="ACTUALIZAR",command=self.update,font=("IMPACT",15),bg="#4F6A77",fg="White",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_delete=Button(self.root,text="ELIMINAR",command=self.delete,font=("IMPACT",15),bg="#872341",fg="White",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_clear=Button(self.root,text="LIMPIAR",command=self.clear,font=("IMPACT",15),bg="#688391",fg="White",cursor="hand2").place(x=860,y=305,width=110,height=28)

        ## -------------------- Employee Details --------------------
        emp_frame=Frame(self.root,bd=6,relief=RIDGE, bg="black")
        emp_frame.place(x=0,y=350,relwidth=1,height=150)
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
        
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set, style="mystyle.Treeview") ## --EL STYLE PARA COLORSITO---

        scrollx.pack(side=BOTTOM,fill=X)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Gender")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("doj",text="D.O.J")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="User Type")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("salary",text="Salary")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=110)
        self.EmployeeTable.column("salary",width=100)
        self.EmployeeTable.pack(fill=BOTH,expand=1)

        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#       -       -       -       -       -       -       -       -
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Se necesita Employee ID",parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row != None:
                    messagebox.showerror("Error","Employee ID ya asignado, intente otro diferente",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                            self.var_emp_id.get(),
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0',END),
                            self.var_salary.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Empleado agregado satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        print(row)
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete('1.0',END),
        self.txt_address.insert(END,row[9]),
        self.var_salary.set(row[10])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Se necesita Employee ID",parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Employee ID invalido",parent=self.root)
                else:
                    cur.execute("UPDATE employee SET name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? WHERE eid=?",(
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_utype.get(),
                            self.txt_address.get('1.0',END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Empleado actualizado satisfactoriamente",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Se necesita Employee ID",parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Employee ID invalido",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","¿Realmente quieres eliminarlo?",parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM employee WHERE eid=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Empleado eliminado satisfactoriamente",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
    
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
                cur.execute("SELECT * FROM employee WHERE "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No se encontro registro!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

if __name__=="__main__":
        root=Tk()
        obj=EmployeeClass(root)
        root.mainloop()