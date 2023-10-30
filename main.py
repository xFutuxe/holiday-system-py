import os, os.path, time, sched
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import datetime


# Connecting to the database
connection = sqlite3.connect('system.db')
cursor = connection.cursor()

# Getting current time
now = datetime.now()
current_time = now.strftime("%H:%M %p") # Formats time

            
def homePage(x):
    Maincanvas.destroy()
    usrEntry.destroy()
    passwrdEntry.destroy()
    loginBtn.destroy()  


    # Making variables accessable outside function
    global homepage
    global logoutBtn
    global calendarBtn
    global customerBtn


    # Make homepage here
    homepage = tk.Canvas(root, width=480, height=450, bg='gray')
    homepage.create_text(160,50, text=f"Welcome, {x}", fill="black", font=('Helvetica 20'))
    homepage.place(relx=0.5, rely=0.53, anchor=tk.CENTER)


    logoutBtn = tk.Button(root, text="Logout", height=1, width=6, command=logout)
    logoutBtn.place(relx=0.95, rely=0.15, anchor=tk.E)

    calendarImage = tk.PhotoImage(file = "imgs/icons8-calendar-48.png")
    calendarBtn = tk.Button(root, image=calendarImage, command=calendar)
    calendarBtn.image = calendarImage
    calendarBtn.place(relx=0.2, rely=0.3, anchor=tk.W)

    customerImage = tk.PhotoImage(file = "imgs/icons8-user-48.png")
    customerBtn = tk.Button(root, image=customerImage, command=customerManage)
    customerBtn.image = customerImage
    customerBtn.place(relx=0.35, rely=0.3, anchor=tk.W)



    # Does user have a admin or 
    adminStatement = f"SELECT username='{x}' from staff WHERE role='admin';"
    cursor.execute(adminStatement)
    result = cursor.fetchall()
    print(result)
    if result == (1,):
        Topcanvas.itemconfig(notLoggedIn, text="Admin Enabled")
        Topcanvas.place(relx=0.5,anchor=tk.N)
    elif result == (0,):
        Topcanvas.place(relx=0.5,anchor=tk.N)
        Topcanvas.delete(notLoggedIn)
        
def calendar():
     pass

def customerManage():
     pass

    


if __name__ == "__main__":


    # initalises tkinter
    root = tk.Tk()
    root.geometry('500x500')
    root.configure(bg='gray')
    root.resizable(False, False)
    root.title('Infinite Journey Retreats')

    def loginPage():
        global Maincanvas
        global usrEntry
        global passwrdEntry
        global loginBtn
        global Topcanvas
        global notLoggedIn

         
        # Top box showing name and current system time
        Topcanvas = tk.Canvas(root, width=500, height=25, bg='dimgray')
        Topcanvas.create_text(95,12, text="Infinite Journey Retreats | ", fill="black", font=('Helvetica 12'))
        notLoggedIn = Topcanvas.create_text(230,12, text="Not Logged in", fill="black", font=('Helvetica 12'))
        Topcanvas.create_text(460,13, text=current_time, fill="black", font=('Helvetica 12'))
        Topcanvas.place(relx=0.5, anchor=tk.N)

        Maincanvas = tk.Canvas(root, width=480, height=450, bg='gray')
        Maincanvas.create_text(230,100, text="Staff Login", fill="black", font=('Helvetica 20'))
        Maincanvas.place(relx=0.5, rely=0.53, anchor=tk.CENTER)

        titleImg = PhotoImage(file="imgs/user-avatar-lock.png")
        Maincanvas.create_image(315, 100, anchor=tk.CENTER, image=titleImg)

        usrEntry = tk.Entry(root, width=30)
        usrEntry.place(rely=0.4, relx=0.5, anchor=tk.CENTER)
        passwrdEntry = tk.Entry(root, width=30, show="*")
        passwrdEntry.place(rely=0.5, relx=0.5, anchor=tk.CENTER)

        loginBtn = tk.Button(root, text="Login", command=login)
        loginBtn.place(rely=0.6, relx=0.5, anchor=tk.CENTER)


    def login():
        usernameInput = usrEntry.get()
        passwordInput = passwrdEntry.get()
        print(usernameInput, passwordInput)
        statement = f"SELECT username from staff WHERE username='{usernameInput}' AND Password = '{passwordInput}';"
        cursor.execute(statement)
        if not cursor.fetchone():
            msg=messagebox.showerror( "Error!", "Login Failed: Incorrect Credentials")
        else:
            homePage(usernameInput)
            msg=messagebox.showinfo( f"Welcome, {usernameInput}", "Login Successful!")

    def logout():
        homepage.destroy()
        logoutBtn.destroy()
        calendarBtn.destroy()
        customerBtn.destroy()
        loginPage()

        
    loginPage()
    root.mainloop()
    

         






