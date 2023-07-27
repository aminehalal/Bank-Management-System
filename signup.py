from tkinter import *
from tkcalendar import Calendar, DateEntry
import sqlite3
from random import randint
import os

current_path = os.path.dirname(os.path.abspath(__file__))

class SingUpPage :
    def __init__(self,root): 
        self.root = root
        self.root.title("Sign Up")
        self.root.geometry ("610x600+350+10")

        db = sqlite3.connect(os.path.join(current_path , 'bank.db'))
        cr = db.cursor()
        db.commit()

        def opendb():
            db = sqlite3.connect(os.path.join(current_path , 'bank.db'))
            cr = db.cursor()
            cr.execute("create table if not exists accounts (cin text primary key,firstname text , lastname text ,birthday date ,email text , adress text, password text , amount integer)")
            cr.execute("create table if not exists operations (id integer primary key autoincrement, cin text , type text , amount integer ,datetime text,foreign key (cin) references accounts(cin))")
            db.commit()    
        def closedb():
            db.close()
        #methodes
        def signup ():
            opendb()
            if var.get() == 1 :
                firstname = firstnamea.get()
                lastname = lastnamea.get()
                cin = cina.get()
                birthday = birthdaya.get_date()
                email = emaila.get()
                adress = adressa.get()
                exite = cr.execute(f"select * from accounts where cin == '{cin}' ")
                if not exite.fetchone():
                    passw = randint(1,9999)
                    password = str(passw).zfill(4)
                    print("im here")
                    cr.execute(f"insert into accounts (cin,firstname , lastname ,birthday,email, adress, password, amount) values ('{cin}','{firstname}','{lastname}','{birthday}','{email}','{adress}','{password}',0)")
                    db.commit()
                    db.close()
            
                    framnew = Frame(self.root , bd=4 , relief=RIDGE)
                    framnew.place (x=50 , y= 5 , width=517 , height=80 )

                    labelnew = Label(framnew, text="Your N° is " +cin +" and your password is " + password, font=("times new roman",17,"bold") ,fg="red" , bd=4 , relief=RIDGE)
                    labelnew.place(x = 0 , y = 0 , width=517,height=80)

                else :
                    print("this user already in")
                    db.close()
                    framnew = Frame(self.root , bd=4 , relief=RIDGE)
                    framnew.place (x=50 , y= 10 , width=517 , height=80 )

                    labelnew = Label(framnew, text="This account is already existe", font=("times new roman",20,"bold") ,fg="red" , bd=4 , relief=RIDGE)
                    labelnew.place(x = 0 , y = 0 , width=517,height=80)
               

                firstnamea.delete(0, END)
                lastnamea.delete(0, END)
                cina.delete(0, END)
                emaila.delete(0,END)
                adressa.delete(0, END)
                rdbtn["value"] = 0
            else :
                print("Error !")
            

        #mainframe
        mainframesign = Frame(self.root , bd=4 , relief=RIDGE)
        mainframesign.place (x=50 , y= 60 , width=517 , height=530)

        #labels
        lblname = Label(mainframesign , text="First Name",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblname.place(x=25,y=20,width=200)

        firstnamea = Entry(mainframesign,font=("arial",14,"bold"),width=50)
        firstnamea.place(x=25 , y=65 , width=200, height=40)

        lblsname = Label(mainframesign , text="Last Name",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblsname.place(x=285,y=20,width=200)

        lastnamea = Entry(mainframesign,font=("arial",14,"bold"),width=50)
        lastnamea.place(x=285 , y=65 , width=200, height=40)

        lblcin = Label(mainframesign , text="CIN",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblcin.place(x=25,y=115,width=200)

        cina = Entry(mainframesign,font=("arial",14,"bold"),width=50)
        cina.place(x=25 , y=160 , width=200, height=40)

        lblbirthday = Label(mainframesign , text="Birthday",font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblbirthday.place(x=285,y=115,width=200)

        birthdaya = DateEntry(mainframesign,font=("arial",15,"bold"),width=50)
        birthdaya.place(x=285 , y=160 , width=200, height=40)

        lblemail = Label(mainframesign, text="Email" , font=("times new roman",18,"bold") , bg="black",fg="gold" , bd=4 , relief=RIDGE)
        lblemail.place(x = 150 , y = 210 , width=200)

        emaila = Entry(mainframesign , font=("arial" , 14 , "bold") , width=200)
        emaila.place ( x= 50 , y = 255 , height = 40 , width=400)

        lbladress = Label(mainframesign, text="Adress" , font=("times new roman",18,"bold") , bg="black",fg="gold" , bd=4 , relief=RIDGE)
        lbladress.place(x = 150 , y = 305 , width=200)

        adressa = Entry(mainframesign , font=("arial" , 14 , "bold") , width=200)
        adressa.place ( x= 50 , y = 350 , height = 40 , width=400)

        var = IntVar() 

        rdbtn = Radiobutton (mainframesign ,variable= var , value=1, text="I agree to the user terms" , font=("times new roman",18,"bold") ,fg="black" , relief=RIDGE)
        rdbtn.place (x = 50 ,  y = 410 , height = 40 , width=400)

        btnsignup = Button(mainframesign, command=signup,text="Sign Up" , font=("times new roman",18,"bold") , bg="black",fg="gold" , bd=4 , relief=RIDGE)
        btnsignup.place(x = 150 , y = 460 , width=200)



if __name__ == "__main__" :
    root=Tk()
    obj=SingUpPage(root)
    root.mainloop()

