from tkinter import *
from PIL import Image, ImageTk

class ErrorLogin :
        
    def __init__(self,root) :
        self.root = root
        self.root.title("Login Error")
        self.root.geometry ("500x400+400+20")

        #error picture
        imghead = Image.open(r"C:\Users\lenevo\Desktop\Langage\Python Projects\Project\Gestion de banque\images\error.jpg")
        imghead = imghead.resize((400,260),Image.ANTIALIAS)
        self.photoimghead = ImageTk.PhotoImage(imghead)

        lblimghead = Label(self.root,image=self.photoimghead,relief=RIDGE)
        lblimghead.place(x=0,y=0,width=500,height=300)

        mainframelogeror = Frame(self.root , relief=RIDGE)
        mainframelogeror.place (x=50 , y= 300 , height=400,width=400)

        errortext = Label(mainframelogeror, text="Password is worng" , font=("times new roman",20,"bold") ,fg="red" , bd=4 , relief=RIDGE)
        errortext.place(x = 0 , y = 0 , width=400)


if __name__ == "__main__" :
    root=Tk()
    obj=ErrorLogin(root)
    root.mainloop()
