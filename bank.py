from tkinter import *
from PIL import Image,ImageTk

class BankManagementSys :
    

    def __init__(self,root) :
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry ("1000x800")

        #methodes 
        def show():
            usernm = username.get()
            passwd = password.get()
            print (usernm , passwd)


        # head picture
        imghead = Image.open(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\images\head.jpg")
        imghead = imghead.resize((1000,120),Image.ANTIALIAS)
        self.photoimghead = ImageTk.PhotoImage(imghead)

        lblimghead = Label(self.root,image=self.photoimghead,bd=4,relief=RIDGE)
        lblimghead.place(x=0,y=0,width=1000,height=120)

        #logo
        imglogo = Image.open(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\images\logo.png")
        imglogo = imglogo.resize((120,120),Image.ANTIALIAS)
        self.photoimglogo = ImageTk.PhotoImage(imglogo)

        lblimglogo = Label(self.root,image=self.photoimglogo,bd=4,relief=RIDGE)
        lblimglogo.place(x=0,y=0,width=120,height=120)

        #title
        lbltitle = Label(self.root , text="Bank Management System",font=("times new roman",35,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbltitle.place(x=0,y=120,width=1000,height=60) 

        #main frame
        mainframe = Frame(self.root , bd=4 , relief=RIDGE)
        mainframe.place (x=200 , y= 180 , width=600 , height=800)
        
        #log in
        lblmain = Label(mainframe , text="Log in",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblmain.place(x=200,y=20,width=200)

        lbluser = Label(mainframe , text="N° Account",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lbluser.place(x=200,y=100,width=200)

        username = Entry(mainframe,font=("arial",20,"bold"),width=60)
        username.place(x=200 , y=150 , width=200, height=50)

        lblpswd = Label(mainframe , text="Password",font=("times new roman",20,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE)
        lblpswd.place(x=200,y=250,width=200)

        password = Entry(mainframe,font=("arial",20,"bold"),width=60,show="*")
        password.place(x=200 , y=300 , width=200, height=50)

        login = Button(mainframe ,text="Login" , command=show,font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        login.place (x= 300 , y= 380 , width=150 , height=50)
        
        signin = Button(mainframe ,text="Sign In" ,font=("times new roman",18,"bold"),bg="black",fg="gold",bd=4,relief=RIDGE )
        signin.place (x= 100 , y= 380 , width=150 , height=50)

    
if __name__ == "__main__" :
    root=Tk()
    obj=BankManagementSys(root)
    root.mainloop()

