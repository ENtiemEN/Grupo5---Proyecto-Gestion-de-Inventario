from tkinter import *
from PIL import Image,ImageTk #python -m pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class SalesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1050x525+275+140")
        self.root.title("Inventory Management System | Developed By Group 5")
        self.root.config(bg='white')
        self.root.focus_force()

        ## All variables --------------------
        ## ============== title ==================
        title=Label(self.root,text="Ver facturas del cliente",font=("goudy old style",18),bg="#000000",fg="#F72798").pack(side=TOP,fill=X)

        lbl_invoice=Label(self.root,text="Factura N°",font=("times new roman",15),bg="white").place(x=50)

if __name__=="__main__":
        root=Tk()
        obj=SalesClass(root)
        root.mainloop()