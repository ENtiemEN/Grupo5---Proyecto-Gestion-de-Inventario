import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from tkinter import *
from tkinter import ttk
from PIL import ImageTk #python -m pip install pillow
from PIL import Image, ImageTk
from tkinter import messagebox
#from customtkinter import*

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System | Developed By Mark | BusyMonkeys")
        self.root.geometry("1080x800+210+50")
        

        # Eliminar los marcos de la ventana
        self.root.overrideredirect(True)

        # Create a style for the focus
        style = ttk.Style()
        style.configure("TEntry", fieldbackground="#ECECEC", padding=10)
        style.map("TEntry", fieldbackground=[('focus', 'lightblue')])

        # === Fondo principal ==========
        self.bg_image = ImageTk.PhotoImage(file="images/background.png")
        self.lbl_bg_image = Label(self.root, image=self.bg_image)
        self.lbl_bg_image.place(x=0, y=0, relwidth=1, relheight=1)



        #===Login_Frame====
        self.employee_id = StringVar()
        self.password = StringVar()
        # Load shadow image
        # self.shadow_image = ImageTk.PhotoImage(file="images/side.png")
        # shadow_label = Label(self.root, image=self.shadow_image)
        # shadow_label.place(x=248, y=88)

        login_frame = Frame(self.root, bd=0, relief=RIDGE,bg="#2A2F2E")
        login_frame.place(x=350, y=190, width=350, height=460)
        title = Label(login_frame, text="LOGIN SYSTEM", font=("Bahnschrift", 30, "bold"), bg="#2A2F2E", fg="white").place(x=0, y=30, relwidth=1)
        hr = Label(login_frame, bg="lightgray").place(x=30, y=84, width=280, height=2)
        lbl_user = Label(login_frame, text="USUARIO ID", font=("Calibri", 15), bg="#2A2F2E", fg="white").place(x=50, y=110)
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("Calibri", 15, "bold"), bg="#ECECEC").place(x=50, y=140,width=250)
        btn_show = Button(login_frame, text="👤", font=("Arial Rounded MT Bold", 18), bg="#ECECEC",bd=0, fg="#565B5E").place(x=272, y=141, width=28, height=26)

        lbl_pass = Label(login_frame, text="CONTRASEÑAS ", font=("Calibri", 15), bg="#2A2F2E", fg="white").place(x=50, y=210)
        txt_pass = Entry(login_frame, textvariable=self.password, show="•", font=("Calibri", 15, "bold"), bg="#ECECEC")
        self.txt_pass = txt_pass  # Store reference to access later
        txt_pass.place(x=50, y=240, width=250)  
        #===Login_BUTTON====
        btn_show = Button(login_frame, command=self.show_hide, text="👁", font=("Arial Rounded MT Bold", 18), bg="#ECECEC", activebackground="#565B5E",bd=0, fg="#565B5E", activeforeground="white", cursor="hand2").place(x=272, y=241, width=28, height=26)
        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Bahnschrift", 15), bg="#40494E", activebackground="black",bd=0, fg="white", activeforeground="white", cursor="hand2").place(x=50, y=300, width=250, height=35)
        
        hr = Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text=" O ", bg="#2A2F2E", fg="white", font=("Times New Roman", 15, "bold")).place(x=160, y=355)
        btn_forget = Button(login_frame, text="  OLVIDE LA CONTRASENA  ", command=self.forget_window, font=("Bahnschrift", 13), bg="#40494E", activebackground="black",bd=0, fg="white", activeforeground="white", cursor="hand2").place(x=50, y=390, width=250, height=35)
        btn_close = Button(self.root, text="X", command=self.close_program, font=("Bahnschrift", 17, "bold"), bg="#793232", activebackground="black",bd=0, fg="white", activeforeground="white", cursor="hand2")
        btn_close.place(x=1030, y=1, width=35, height=60)
        #===Frame2============
        register_frame = Frame(self.root,bg="#2A2F2E")
        register_frame.place(x=350, y=668, width=350, height=50)
        lbl_reg = Label(register_frame, text="Login System | By BusyMonkeys", font=("Calibri", 13), bg="#2A2F2E", fg="white").place(x=60, y=12)
    
    
    def show_hide(self):
        if self.txt_pass.cget('show') == '':
            self.txt_pass.config(show='•')
        else:
            self.txt_pass.config(show='')

    def send_otp(self, email, otp):
        sender_email = "markquispegonzales@outlook.es"
        sender_password = "gjjzjhcnisqvetka"
        subject = "Password Reset OTP"
        body = f"Your OTP for password reset is: {otp}"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, email, text)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def generate_otp(self):
        return ''.join(random.choices(string.digits, k=6))

    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror('Error', "Employee ID must be required", parent=self.root)
            else:
                cur.execute("select email from employee where eid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror('Error', "Invalid Employee ID, Try again", parent=self.root)
                else:
                    # Generate OTP
                    self.var_otp_code = self.generate_otp()
                    # Send OTP
                    self.send_otp(email[0], self.var_otp_code)
                    # Create the reset password window
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()

                    self.forget_win = Toplevel(self.root)
                    self.forget_win.title('RESET PASSWORD')
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()

                    title = Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold'), bg='black', fg="white").pack(side=TOP, fill=X)
                    lbl_reset = Label(self.forget_win, text="Enter OTP Sent on Registered Email", font=("times new roman", 15)).place(x=20, y=60)
                    Txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15), bg="White").place(x=20, y=100, width=250, height=30)

                    self.btn_reset = Button(self.forget_win, text="SUBMIT", command=self.validate_otp, font=("times new roman", 15), bg="lightblue")
                    self.btn_reset.place(x=280, y=100, width=100, height=30)

                    lbl_new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 15)).place(x=20, y=160)
                    Txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("times new roman", 15), bg="White").place(x=20, y=190, width=250, height=30)

                    lbl_c_pass = Label(self.forget_win, text="Confirmar Contrasena", font=("times new roman", 15)).place(x=20, y=225)
                    Txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("times new roman", 15), bg="white").place(x=20, y=255, width=250, height=30)

                    self.btn_update = Button(self.forget_win, text="UPDATE", state=DISABLED, command=self.update_password, font=("times new roman", 15), bg="lightblue")
                    self.btn_update.place(x=150, y=300, width=100, height=30)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def validate_otp(self):
        if self.var_otp.get() == self.var_otp_code:
            self.btn_update.config(state=NORMAL)
            messagebox.showinfo("Info", "OTP Verified! You can now reset your password.", parent=self.forget_win)
        else:
            messagebox.showerror("Error", "Invalid OTP! Please try again.", parent=self.forget_win)

    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "Passwords do not match!", parent=self.forget_win)
        else:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            try:
                cur.execute("UPDATE employee SET pass=? WHERE eid=?", (self.var_new_pass.get(), self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.forget_win)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All Fields are required", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "INVALID USERNAME/PASSWORD", parent=self.root)
                else:
                    print(user)
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def close_program(self):
        self.root.destroy()
root = Tk()
obj = Login_System(root)
root.mainloop()
