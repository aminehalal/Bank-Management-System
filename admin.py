from tkinter import *
from PIL import Image,ImageTk
from signup import SingUpPage
from blocks import ErrorLogin
from bank import BankManagementSys
import datetime
import sqlite3

class BankManagementAdmin :

    def __init__(self,root) :
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry ("1000x700+100+0")


        #block user page
        def returntab() :
            new = BankManagementAdmin(root)

        def blockuser() :

            def block():
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                cr = db.cursor()
                blockinguser = blockusername.get()

                mainframeb = Frame(self.root , bd=4 , relief=RIDGE)
                mainframeb.place (x=100 , y= 180 , width=800 , height=500)

                cr.execute(f"select * from accounts where cin =='{blockinguser}'")

                if cr.fetchone() :
                    cr.execute(f"delete from accounts where cin =='{blockinguser}'")

                    db.commit()

                    blocking = Label(mainframeb , text=blockinguser + " is deleted from database" ,font=("times new roman",27,"bold"),fg="red",bd=4,relief=RIDGE)
                    blocking.place(x=100,y=60,width=600,height=50)
                else :
                    blocking = Label(mainframeb , text=blockinguser + " is not exist" ,font=("times new roman",27,"bold"),fg="red",bd=4,relief=RIDGE)
                    blocking.place(x=100,y=60,width=600,height=50)

                btnreturn = Button(mainframeb ,text="Back" ,command=returntab , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
                btnreturn.place (x= 300 , y= 200 , width=250 , height=50)

            mainframeb = Frame(self.root , bd=4 , relief=RIDGE)
            mainframeb.place (x=100 , y= 180 , width=800 , height=500)

            blockusername = Entry(mainframeb , font=("arial" , 14 , "bold") , width=200)
            blockusername.place ( x= 300 , y = 150 , height = 50 , width=250)

            btnblock = Button(mainframeb ,text="Block" , command=block,font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
            btnblock.place (x= 300 , y= 230 , width=250 , height=50)

            btnreturn = Button(mainframeb ,text="Back" ,command=returntab , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
            btnreturn.place (x= 300 , y= 320 , width=250 , height=50)

        #checkuserpage
        def checkuser() :

            #typing
            def check ():
                db = sqlite3.connect(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\bank.db")
                cr = db.cursor()
                checkinguser = checkusername.get()

                mainframec = Frame(self.root , bd=4 , relief=RIDGE)
                mainframec.place (x=100 , y= 180 , width=800 , height=500)

                cr.execute(f"select * from accounts where cin =='{checkinguser}'")

                if cr.fetchone() :
                    cr.execute(f"select type , datetime from operations where cin =='{checkinguser}' order by datetime limit 5")
                    detail = cr.fetchall()

                    db.close()

                    checking = Label(mainframec , text="Operations Carried out by "+ checkinguser+ "\n\n"+ detail[0][0] +" in " + detail [0][1]+"\n"+ detail[1][0] +" in " + detail [1][1] + "\n" + detail[2][0] +" in " + detail [2][1]+"\n" + detail[3][0] +" in " + detail [3][1]+"\n" + detail[4][0] +" in " + detail [4][1] ,font=("times new roman",27,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
                    checking.place(x=50,y=40,width=700,height=300)

                else :
                    blocking = Label(mainframec , text=checkinguser + " is not exist" ,font=("times new roman",27,"bold"),fg="red",bd=4,relief=RIDGE)
                    blocking.place(x=100,y=180,width=600,height=50)

                btnreturn = Button(mainframec ,text="Back" ,command=returntab , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
                btnreturn.place (x= 300 , y= 380 , width=250 , height=50)

            mainframeb = Frame(self.root , bd=4 , relief=RIDGE)
            mainframeb.place (x=100 , y= 180 , width=800 , height=500)

            checkusername = Entry(mainframeb , font=("arial" , 14 , "bold") , width=200)
            checkusername.place ( x= 300 , y = 150 , height = 50 , width=250)

            btncheck = Button(mainframeb ,text="Check" ,command=check , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
            btncheck.place (x= 300 , y= 230 , width=250 , height=50)

            btnreturn = Button(mainframeb ,text="Back" ,command=returntab , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
            btnreturn.place (x= 300 , y= 320 , width=250 , height=50)


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

        mainframe = Frame(self.root , bd=4 , relief=RIDGE)
        mainframe.place (x=100 , y= 180 , width=800 , height=500)

           
        btnadduser = Button(mainframe ,text="Add User" , command=self.signupdetail, font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btnadduser.place (x= 300 , y= 80 , width=250 , height=50)

        btnblockuser = Button(mainframe ,text="Block User" , command=blockuser, font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btnblockuser.place (x= 300 , y= 180 , width=250 , height=50)

        btncheckuser = Button(mainframe ,text="Check User" ,command=checkuser, font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btncheckuser.place (x= 300 , y= 280 , width=250 , height=50)

        btnusermode = Button(mainframe ,text="User Mode" ,command=self.usermode , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btnusermode.place (x= 300 , y= 380 , width=250 , height=50)

        #other pages
    def signupdetail (self) :
        self.new_windows = Toplevel(self.root)
        self.app = SingUpPage(self.new_windows)

    def usermode (self) :
        self.new_windows = Toplevel(self.root)
        self.app = BankManagementSys(self.new_windows)

    
if __name__ == "__main__" :
    root=Tk()
    obj=BankManagementAdmin(root)
    root.mainloop()