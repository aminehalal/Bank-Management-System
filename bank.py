from tkinter import *
from PIL import Image,ImageTk
from signup import SingUpPage
from blocks import ErrorLogin
import datetime
import sqlite3

class BankManagementSys :

    def __init__(self,root) :
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry ("1000x700+100+0")

        db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
        cr = db.cursor()


        def opendb():
            db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
            cr = db.cursor()
        #methodes 



        def loginnow():
            
            def opendb():
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                cr = db.cursor()
            
            def withdrawalnow():
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                balancen = balance.get()
                cr = db.cursor()
                cr.execute(f"update accounts set amount =amount - {balancen} where cin =='{cin}'")
                db.commit()
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                cr = db.cursor()
                cr.execute(f"insert into operations (cin,type,amount,datetime) values('{cin}','Withdrawal','{balancen}','{datetime.datetime.now()}')")
                db.commit()
                cr.execute(f"select amount from accounts where cin =='{cin}'")
                amount=cr.fetchone()

                amountnow = Label(mainframe , text="Your current balance is : " + str(amount[0]) + " DH" ,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
                amountnow.place(x=0,y=100,width=800,height=60)
                        
            def depositnow():
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                balancen = balance.get()
                cr = db.cursor()
                cr.execute(f"update accounts set amount =amount + {balancen} where cin == '{cin}' ")
                
                db.commit()
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                cr = db.cursor()
                cr.execute(f"insert into operations (cin,type,amount,datetime) values('{cin}','Deposit','{balancen}','{datetime.datetime.now()}')")
                
                db.commit()
                
                cr.execute(f"select amount from accounts where cin =='{cin}'")
                amount=cr.fetchone()

                amountnow = Label(mainframe , text="Your current balance is : " + str(amount[0]) + " DH" ,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
                amountnow.place(x=0,y=100,width=800,height=60)

            def logout():
                new = BankManagementSys(root)

            cin = username.get()
            passwrd = password.get()
            db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
            cr = db.cursor()
            exite = cr.execute(f"select * from accounts where cin == '{cin}' and password =='{passwrd}'")
            stillon = True
            if exite.fetchone() :
               # while stillon == True:
                    cr.execute(f"select amount from accounts where cin =='{cin}'")
                    amount=cr.fetchone()
                    cr.execute(f"select firstname from accounts where cin =='{cin}'")
                    firstoname = cr.fetchone()
                    cr.execute(f"select lastname from accounts where cin =='{cin}'")
                    lastoname = cr.fetchone()
                    fullname = firstoname[0] + " " + lastoname[0]
                    mainframe = Frame(self.root , bd=4 , relief=RIDGE)
                    mainframe.place (x=100 , y= 180 , width=800 , height=500)

                    welcome = Label(mainframe , text="Welcome " + fullname ,font=("times new roman",35,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
                    welcome.place(x=0,y=20,width=800,height=60)

                    amountnow = Label(mainframe , text="Your current balance is : " + str(amount[0]) + " DH" ,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
                    amountnow.place(x=0,y=100,width=800,height=60)

                    balance = Entry(mainframe,font=("arial",20,"bold"),width=60)
                    balance.place(x=300 , y=220 , width=200, height=50)

                    btnwd = Button(mainframe ,text="Withdrawal" , command=withdrawalnow,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
                    btnwd.place (x= 150 , y= 315 , width=250 , height=50)
                    
                    btndep = Button(mainframe ,text="Deposit" , command=depositnow,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
                    btndep.place (x= 450 , y= 315 , width=250 , height=50)

                    balancen = balance.get()

                    btndep = Button(mainframe ,text="Logout" , command=logout,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
                    btndep.place (x= 300 , y= 380 , width=250 , height=50)
                    #methodes
            else :
                self.errorlogindetail()
                print("user dont exite")
                db.close()


        # head picture
        imghead = Image.open(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\images\head.jpg")
        imghead = imghead.resize((880,120),Image.ANTIALIAS)
        self.photoimghead = ImageTk.PhotoImage(imghead)

        lblimghead = Label(self.root,image=self.photoimghead,bd=4,relief=RIDGE)
        lblimghead.place(x=120,y=0,width=880,height=120)

        #logo
        imglogo = Image.open(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\images\logo.png")
        imglogo = imglogo.resize((110,110),Image.ANTIALIAS)
        self.photoimglogo = ImageTk.PhotoImage(imglogo)

        lblimglogo = Label(self.root,image=self.photoimglogo,bd=4,relief=RIDGE)
        lblimglogo.place(x=5,y=5,width=110,height=110)

        #title
        lbltitle = Label(self.root , text="Bank Management System",font=("times new roman",35,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbltitle.place(x=0,y=120,width=1000,height=60) 

        #main frame
        mainframe = Frame(self.root , bd=4 , relief=RIDGE)
        mainframe.place (x=100 , y= 180 , width=800 , height=500)
        
        #mainbankoic

        imgmain = Image.open(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\images\mainbank.jpg")
        imgmain = imgmain.resize((800,500),Image.ANTIALIAS)
        self.photoimgmain = ImageTk.PhotoImage(imgmain)

        lblimgmain = Label(mainframe,image=self.photoimgmain,bd=4,relief=RIDGE)
        lblimgmain.place(x=0,y=0,width=800,height=500)

        #log in
        lblmain = Label(mainframe , text="Log in",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblmain.place(x=300,y=20,width=200)

        lbluser = Label(mainframe , text="N° Account",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbluser.place(x=300,y=100,width=200)

        username = Entry(mainframe,font=("arial",20,"bold"),width=60)
        username.place(x=300 , y=150 , width=200, height=50)

        lblpswd = Label(mainframe , text="Password",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblpswd.place(x=300,y=250,width=200)

        password = Entry(mainframe,font=("arial",20,"bold"),width=60,show="*")
        password.place(x=300 , y=300 , width=200, height=50)

        login = Button(mainframe ,text="Login" , command=loginnow,font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        login.place (x= 300 , y= 380 , width=200 , height=50)
        
        #signup = Button(mainframe , command=self.signupdetail,text="Sign Up" ,font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        #signup.place (x= 200 , y= 380 , width=150 , height=50)

    def signupdetail (self) :
        self.new_windows = Toplevel(self.root)
        self.app = SingUpPage(self.new_windows)
    def errorlogindetail (self) :
        self.new_windows = Toplevel(self.root)
        self.app = ErrorLogin(self.new_windows)

if __name__ == "__main__" :
    root=Tk()
    obj=BankManagementSys(root)
    root.mainloop()

