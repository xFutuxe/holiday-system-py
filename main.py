## RUNNING THIS PROGRAM REQUIRES PYTHON 3.6+ 

import os, os.path, calendar, sys, subprocess
import sqlite3
import tkinter as tk
import subprocess
from tkinter import *
from tkinter import messagebox
from datetime import *

globalDateFormat = "%d/%m/%y"

today = datetime.today()
formatted_date = today.strftime('%d/%m/%y')
print(formatted_date)

# Connecting to the database
connection = sqlite3.connect('system.db')
cursor = connection.cursor()

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
    calendarBtn = tk.Button(root, image=calendarImage, command=calendarMenu)
    calendarBtn.image = calendarImage
    calendarBtn.place(relx=0.2, rely=0.3, anchor=tk.W)

    customerImage = tk.PhotoImage(file = "imgs/icons8-user-48.png")
    customerBtn = tk.Button(root, image=customerImage, command=customerManage)
    customerBtn.image = customerImage
    customerBtn.place(relx=0.35, rely=0.3, anchor=tk.W)




    # Does user have a admin or 
    adminStatement = f"SELECT username='{x}' from tblStaff WHERE role='admin';"
    cursor.execute(adminStatement)
    result = cursor.fetchone()
    print(result)
    if result == (1,):
        Topcanvas.itemconfig(notLoggedIn, text="Admin Enabled")
        Topcanvas.place(relx=0.5,anchor=tk.N)
        # Event Manager button (gets hidden if user is not admin)
        eventImage = tk.PhotoImage(file = "imgs/icons8-calendar-settings-32.png")
        eventBtn = tk.Button(root, image=eventImage, command=eventManager)
        eventBtn.image = eventImage
        eventBtn.place(relx=0.5, rely=0.3, anchor=tk.W)
        
    elif result == (0,):
        Topcanvas.place(relx=0.5,anchor=tk.N)
        Topcanvas.delete(notLoggedIn)
        
def calendarMenu():
    calendarMenu = Toplevel(root)
    calendarMenu.title("Infinite Journey Retreats | Calendar")
    calendarMenu.geometry("350x350")
    calendarMenu.resizable(False, False)
    calendarMenu.configure(bg='gray')

    currentDay = Label(calendarMenu, text=formatted_date, bg="gray", font=('Helvetica 20'))
    currentDay.place(relx=0.5, rely=0.15, anchor=tk.N)

    eventGrab = f"SELECT event from tblCalendar WHERE date='{formatted_date}' AND assigned='{usernameInput}';" 
    cursor.execute(eventGrab) 
    result = cursor.fetchone()
    print(result[0])

def customerManage():

    customerMenu = Toplevel(root)
    customerMenu.title("Infinite Journey Retreats | Customer Management")
    customerMenu.geometry("350x350")
    customerMenu.resizable(False, False)
    customerMenu.configure(bg='gray')

def eventManager():

    eventManager = Toplevel(root)
    eventManager.title("Infinite Journey Retreats | Event Manager")
    eventManager.geometry("350x350")
    eventManager.resizable(False, False)
    eventManager.configure(bg='gray')

    menuTitle = Label(eventManager, text="Event Manager", bg="gray", font=('Helvetica 20'))
    menuTitle.place(relx=0.3, anchor=tk.N)

    # Form for managers to fill in to make events system wide | Event Name
    eventNameLbl = Label(eventManager, text="Event Name:", bg="gray")
    eventNameLbl.pack(side=LEFT,anchor=tk.NW, pady=(50,0))
    eventName = tk.Entry(eventManager, width=30)
    eventName.place(relx=0.22, rely=0.15, anchor=tk.NW)

    # Date of event
    dateLbl = Label(eventManager, text="Event Date:", bg="gray")
    dateLbl.place(rely=0.22, anchor=tk.NW)
    eventDate = tk.Entry(eventManager, width=30)
    eventDate.place(relx=0.22, rely=0.22, anchor=tk.NW)

    # Assigning user to an event
    assignLbl = Label(eventManager, text="Assigned User:", bg="gray")
    assignLbl.place(rely=0.29, anchor=tk.NW)
    userAssign = tk.Entry(eventManager, width=30)
    userAssign.place(relx=0.22, rely=0.29, anchor=tk.NW)

    checkboxValue = tk.BooleanVar()
    globalText = Label(eventManager, text="Global:", bg="gray")
    globalText.place(rely=0.35, anchor=tk.NW)
    globalButton = Checkbutton(eventManager, bg='gray', activebackground='gray', variable=checkboxValue)
    globalButton.place(relx=0.12, rely=0.35, anchor=tk.NW)


    def showAllEvents():
        events = []
        showAllScreen = Toplevel(eventManager)
        showAllScreen.title("Infinite Journey Retreats | Event Manager")
        showAllScreen.geometry("350x350")
        showAllScreen.resizable(False, False)
        showAllScreen.configure(bg='gray')
      
        listbox = tk.Listbox(
            showAllScreen,
            listvariable=events,
            height=20,
            selectmode=tk.BROWSE,
        )

        listbox.place(relx=0.03, rely=0.03, anchor=tk.NW)

        cursor.execute("SELECT eventID, event from tblCalendar")
        allEvents = cursor.fetchall()
        for row in allEvents:
            events.append(str(row[1]))
            listbox.insert(END, row[1])
        
        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            print('You selected item %d: "%s"' % (index, value))
            # fetch other information from db
            eventNumber = index + 1
            cursor.execute(f"SELECT event, date, assigned, global, eventCreatedBy, eventTimeCreated, eventDateCreated FROM tblCalendar WHERE eventID='{eventNumber}'")
            eventResults = cursor.fetchall()
            print(eventResults[0])

            # Form for managers to fill in to make events system wide | Event Name
            eventNameLbl = Label(showAllScreen, text="Event Name:", bg="gray")
            eventNameLbl.place(rely=0.05, relx=0.43, anchor=tk.NW)
            eventName = tk.Entry(showAllScreen, width=30)
            eventName.place(relx=0.43, rely=0.10, anchor=tk.NW)
            eventName.insert(END, eventResults[0][0])

            # Date of event
            dateLbl = Label(showAllScreen, text="Event Date:", bg="gray")
            dateLbl.place(rely=0.16, relx=0.43, anchor=tk.NW)
            eventDate = tk.Entry(showAllScreen, width=30)
            eventDate.place(relx=0.43, rely=0.22, anchor=tk.NW)
            eventDate.insert(END, eventResults[0][1])

            # Assigning user to an event
            assignLbl = Label(showAllScreen, text="Assigned User:", bg="gray")
            assignLbl.place(rely=0.28, relx=0.43, anchor=tk.NW)
            userAssign = tk.Entry(showAllScreen, width=30)
            userAssign.place(relx=0.43, rely=0.34, anchor=tk.NW)
            userAssign.insert(END, eventResults[0][2])

            checkboxValue = tk.BooleanVar()
            globalText = Label(showAllScreen, text="Global:", bg="gray")
            globalText.place(rely=0.40, relx=0.43, anchor=tk.NW)
            globalButton = Checkbutton(showAllScreen, bg='gray', activebackground='gray', variable=checkboxValue)
            if eventResults[0][3] == '1':
                globalButton.select()
            else:
                pass
            globalButton.place(relx=0.55, rely=0.35, anchor=tk.NW)




        listbox.bind('<<ListboxSelect>>', onselect)    

    def sendData():
        cursor.execute('''INSERT INTO tblCalendar(date, event, assigned, global, eventCreatedBy, eventTimeCreated, eventDateCreated) VALUES (?, ?, ?, ?, ?, ?, ?);''', (eventDate.get(), eventName.get(), userAssign.get(), checkboxValue.get(), usernameInput, current_time, formatted_date)) # Tells the database to insert these values
        connection.commit()
        eventDate.delete(0,END)
        eventName.delete(0,END)
        userAssign.delete(0,END)
        msg=messagebox.showinfo( "Success!", f"The event, {eventName.get()} was successfully added to the database and was assigned to {userAssign.get()}") # Shows error to user letting them know
        print(f"Given information was sent to the database on {formatted_date} at {current_time}")
    # Checks all inputted data is present and formatted correctly
    def checkEventData():
        dateValue = eventDate.get()
        userValue = userAssign.get()
        eventValue = eventName.get()
        dateBool = True
        if not len(dateValue) == 0:
            try:
                # Checks if the dateValue variable is formatted to correct format e.g 10/01/24
                dateBool = bool(datetime.strptime(dateValue, globalDateFormat))
            except:
                # dateBool will be false if it is not.
                dateBool = False
            if dateBool == True:
                print("Present and Fomatted")
            else:
                print("Present but not formatted")
                msg=messagebox.showerror( "Error!", "Date needs to be formatted as example: 10/01/24 (D/M/Y)!") # Shows error to user letting them know
                return     
        else:
            print("Not Present")
            msg=messagebox.showerror( "Error!", "The event date field needs to be filled!")
            return

        if not len(eventValue) == 0:
            print("Event Name Present")
        else:
            msg=messagebox.showerror( "Error!", "The event name field needs to be filled!")
            print("Event Name not present")
            return

        if not len(userValue) == 0:
            print("User Assigned Present")
        else:
            if checkboxValue.get() == True:
                print("user is not assigned but global option is checked")
            else:
                print("User Assigned Not Present")
                msg=messagebox.showerror( "Error!", "The assigned user field needs to be filled or Global option should be checked!")
                return
        
        sendData() # After all variables have passed checks sendData function will be called


    # Sends the data to the database if all data passes checkEventData 
    submitBtn = tk.Button(eventManager, text="Create", command=checkEventData)
    submitBtn.place(rely=0.6, relx=0.5, anchor=tk.CENTER)

    # Sends the data to the database if all data passes checkEventData 
    showAllBtn = tk.Button(eventManager, text="Show all", command=showAllEvents)
    showAllBtn.place(rely=0.6, relx=0.7, anchor=tk.CENTER)

if __name__ == "__main__":


    # initalises tkinter
    root = tk.Tk()
    root.geometry('500x500')
    root.configure(bg='gray')
    root.resizable(False, False)
    root.title('Infinite Journey Retreats')

    def menuBar():
        global Topcanvas
        global notLoggedIn
        global clock

        # Getting current time and updating it
        def update_time():
            global current_time

            time = datetime.now()
            current_time = time.strftime("%H:%M:%S %p") # Formats time
            clock.config(text=current_time)
            clock.after(1000, update_time)

        # Top box showing name and current system time
        Topcanvas = tk.Canvas(root, width=500, height=25, bg='dimgray')
        Topcanvas.create_text(95,12, text="Infinite Journey Retreats | ", fill="black", font=('Helvetica 12'))
        notLoggedIn = Topcanvas.create_text(235,12, text="Not Logged in", fill="black", font=('Helvetica 12'))
        clock = Label(Topcanvas, bg="dimgray", font=('Helvetica 10'))
        clock.place(relx=0.9, rely=0.45, anchor=tk.CENTER)
        ## clock = Topcanvas.create_text(460,13, fill="black", font=('Helvetica 12'))
        Topcanvas.place(relx=0.5, anchor=tk.N)
        update_time()


    def loginPage():
        global Maincanvas
        global usrEntry
        global passwrdEntry
        global loginBtn

        Maincanvas = tk.Canvas(root, width=480, height=450, bg='gray')
        Maincanvas.create_text(230,100, text="Staff Login", fill="black", font=('Helvetica 20'))
        Maincanvas.place(relx=0.5, rely=0.53, anchor=tk.CENTER)

        titleImg = PhotoImage(file="imgs/user-avatar-lock.png")
        Maincanvas.create_image(460, 50, anchor=tk.CENTER, image=titleImg)

        Maincanvas.create_text(190,143, text="Username", fill="black", font=('Helvetica 13'))
        Maincanvas.create_text(189,190, text="Password", fill="black", font=('Helvetica 13'))
        usrEntry = tk.Entry(root, width=30)
        usrEntry.place(rely=0.4, relx=0.5, anchor=tk.CENTER)
        passwrdEntry = tk.Entry(root, width=30, show="*")
        passwrdEntry.place(rely=0.5, relx=0.5, anchor=tk.CENTER)

        loginBtn = tk.Button(root, text="Login", command=login)
        loginBtn.place(rely=0.6, relx=0.5, anchor=tk.CENTER)


    def login():
        global usernameInput

        usernameInput = usrEntry.get()
        passwordInput = passwrdEntry.get()
        print(usernameInput, passwordInput)
        statement = f"SELECT username from tblStaff WHERE username='{usernameInput}' AND Password = '{passwordInput}';"
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
        Topcanvas.itemconfig(notLoggedIn, text="Not logged in")
        loginPage()
   
    eventManager()
    menuBar()
    loginPage()
    root.mainloop()

    

         







