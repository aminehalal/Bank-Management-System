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

           
        btndep = Button(mainframe ,text="Add User" , command=self.signupdetail, font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btndep.place (x= 300 , y= 80 , width=250 , height=50)

        btndep = Button(mainframe ,text="Block User" , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btndep.place (x= 300 , y= 180 , width=250 , height=50)

        btndep = Button(mainframe ,text="Check User" , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btndep.place (x= 300 , y= 280 , width=250 , height=50)

        btndep = Button(mainframe ,text="User Mode" ,command=self.usermode , font=("times new roman",30,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        btndep.place (x= 300 , y= 380 , width=250 , height=50)

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