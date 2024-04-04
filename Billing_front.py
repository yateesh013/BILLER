import customtkinter as ct
from tkinter import ttk
import db_func as db
from tkinter import messagebox as ms


class App(ct.CTk):

    def __init__(self) -> None:
        super().__init__()
        self.geometry("750x600")
        self.title("MY BILLING SYSTEM")
        ct.set_appearance_mode("dark")
        ct.set_default_color_theme("blue")
        self.resizable("FALSE","FALSE")
        self.items=[]


    def num(self,n):
        if n=="<":
            l=len(self.e2.get())
            self.e2.delete(l-1)
        else:    
            self.e2.insert("end",n)
    

    def main_w(self):
        name=ct.CTkLabel(self,text="yateesh food court".upper())
        name.place(x=300,y=20)
        
        e1=ct.CTkEntry(self,corner_radius=50,placeholder_text="BILL.NO:")
        e1.place(x=20,y=20)
        itm=["egg","biriyani","bonda"]
        item=ct.CTkComboBox(self,values=itm,dropdown_hover_color="green",button_hover_color="green",corner_radius=50)
        item.place(x=20,y=60)
        item.set("   ")
        self.e2=ct.CTkEntry(self,placeholder_text="Quantity",corner_radius=50)
        self.e2.place(x=200,y=60)
        pay=["CASH","UPI"]
        pay_type=ct.CTkComboBox(self,values=pay,dropdown_hover_color="green",button_hover_color="green",corner_radius=50)
        pay_type.place(x=380,y=60)
        pay_type.set("   ")

        def cur_display():
            t1.delete(*t1.get_children())
            for i in self.items:
                t1.insert("","end",values=i)

        def clear():
            item.set("   ")
            pay_type.set("   ")
            self.e2.delete(0,"end")
        def add_item():
            b=e1.get()
            food=item.get()
            q=self.e2.get()
            t=pay_type.get()
            if b=="" or food=="   " or q=="":
                #display any message needed
                ms.showerror("ERROR IN BILLING","FILL ALL DETAILS CORRECTLY.")
                return
            elif len(db.search(b))!=0:
                ms.showerror("BILL ERROR ","BILL IS ALREADY PRESENT")
                return          
            pr=db.getdata(food)
            q=int(q)
            self.items.append([b,food,q,q*pr])
            cur_display()
            cur_total=0
            for i in self.items:
                cur_total+=int(i[3])
            total.configure(self,text=f"TOTAL     :    {cur_total}")    
            self.inf.configure(text=f"{food} added to the bill".upper())
            clear()

        def delete_item():
            l=t1.focus()    
            l=t1.item(l)
            data=l["values"]
            if len(data)==0:
                ms.showerror("SELECTION ERROR","FIRST SELECT ANY ITEM TO DELETE.")
                return
            try:
                for i in self.items:
                    if i[0]==str(data[0]) and i[1]==str(data[1]) and i[2]==data[2] and i[3]==(data[3]):
                        self.items.remove(i)
                        break
            except:
                return
            cur_total=0
            for i in self.items:
                cur_total+=int(i[3])
            total.configure(self,text=f"TOTAL     :    {cur_total}")
            cur_display()        
            self.inf.configure(text=f"deleted from the bill".upper())

        b1=ct.CTkButton(self,command=add_item,text="ADD ITEM",corner_radius=50,hover_color="green")
        b1.place(x=100,y=120)
        b2=ct.CTkButton(self,command=delete_item,text="DELETE ITEM",corner_radius=50,hover_color="green")
        b2.place(x=300,y=120)

        se=ct.CTkEntry(self,placeholder_text="Search:",corner_radius=50)
        se.place(x=550,y=120)
        def search():
            id=se.get()
            self.items=db.search(id)
            if len(self.items)==0:
                ms.showerror("BILL ERROR","BILL IS NOT FOUND IN DATABASE.")
                return
            cur_display()
            cur_total=0
            for i in self.items:
                cur_total+=int(i[3])
            total.configure(self,text=f"TOTAL     :    {cur_total}")    
            def close():
                self.items.clear()
                cur_display()
                cls.destroy()
                total.configure(self,text=f"TOTAL     :         ")
                se.delete(0,"end")
                self.inf.configure(text=f"bill is closed".upper())

            cls=ct.CTkButton(self,command=close,text="CLOSE",hover_color="green",width=100,corner_radius=50)
            cls.place(x=620,y=160)
            self.inf.configure(text=f"bill.no : {id} is opened".upper())

        se1=ct.CTkButton(self,text="Q",command=search,width=20,corner_radius=50)
        se1.place(x=690,y=120)
        
        f1=ct.CTkFrame(self,height=300,width=430)
        f1.place(x=300,y=200)
        col=["B","I","Q","P"]
        t1=ttk.Treeview(f1,columns=col,show="headings")
        t1.pack()
        t1.heading(column="B",text="BILL.NO:")
        t1.column(column="B",stretch="False",width=75)
        t1.heading(column="I",text="ITEM")
        t1.column(column="I",stretch="False",width=180)
        t1.heading(column="Q",text="QUANTITY")
        t1.column(column="Q",stretch="False",width=75)
        t1.heading(column="P",text="PRICE")
        t1.column(column="P",stretch="False",width=100)
        
        total=ct.CTkLabel(self,text=f"TOTAL     :       ")
        total.place(x=600,y=430)


        def save():
            if len(self.items)==0:
                ms.showerror("BILL ERROR","NO ITEM IS ADDED")
                return
            try:
                check=db.search(self.items[0][0])
            except:
                ms.showerror("BILL ERROR","BILL ALREADY FOUND IN DATABSE.")
                return    
            if len(check)!=0:
                if len(check)!=len(self.items):
                    db.delete(check)
                    p=pay_type.get()
                    for i in self.items:
                        i.append(p)
                    db.save(self.items)
                    self.items.clear()
                    cur_display()
                    total.configure(self,text=f"TOTAL     :     ")
                    self.inf.configure(text=f"bill is updated".upper())

                    return
                ms.showinfo("BILL ERROR","BILL IS ALREADY SAVED IN DATABASE.")    
                return
            p=pay_type.get()
            for i in self.items:
                i.append(p)
            db.save(self.items)
            self.items.clear()
            cur_display()
            total.configure(self,text=f"TOTAL     :     ")
            self.inf.configure(text=f"bill is saved to database.".upper())


        def delete():
            try:
                db.delete(self.items)
            except:
                ms.showerror("BILL ERROR","NO BILL IS ADDED TO DELETE")
                return
            self.items.clear()
            cur_display() 
            total.configure(self,text=f"TOTAL     :      ") 
            self.inf.configure(text=f"bill is deleted from database".upper())
  
        b3=ct.CTkButton(self,command=save,text="SAVE",hover_color="green",corner_radius=50)
        b3.place(x=350,y=480)
        b4=ct.CTkButton(self,command=delete,text="DELETE",hover_color="green",corner_radius=50)
        b4.place(x=550,y=480)
        b5=ct.CTkButton(self,state="disabled",text="PRINT",hover_color="green",corner_radius=50)
        b5.place(x=450,y=530)
        nd=ct.CTkButton(self,command=lambda:self.num("<"),text="<-|",width=75,corner_radius=50,hover_color="green")
        nd.place(x=200,y=410)
        n0=ct.CTkButton(self,command=lambda:self.num("0"),text="0",width=75,corner_radius=50,hover_color="green")
        n0.place(x=110,y=410)
        n1=ct.CTkButton(self,command=lambda:self.num("1"),text="1",width=75,corner_radius=50,hover_color="green")
        n1.place(x=20,y=340)
        n2=ct.CTkButton(self,command=lambda:self.num("2"),text="2",width=75,corner_radius=50,hover_color="green")
        n2.place(x=110,y=340)
        n3=ct.CTkButton(self,command=lambda:self.num("3"),text="3",width=75,corner_radius=50,hover_color="green")
        n3.place(x=200,y=340)
        n4=ct.CTkButton(self,command=lambda:self.num("4"),text="4",width=75,corner_radius=50,hover_color="green")
        n4.place(x=20,y=270)
        n5=ct.CTkButton(self,command=lambda:self.num("5"),text="5",width=75,corner_radius=50,hover_color="green")
        n5.place(x=110,y=270)
        n6=ct.CTkButton(self,command=lambda:self.num("6"),text="6",width=75,corner_radius=50,hover_color="green")
        n6.place(x=200,y=270)
        n7=ct.CTkButton(self,command=lambda:self.num("7"),text="7",width=75,corner_radius=50,hover_color="green")
        n7.place(x=20,y=200)
        n8=ct.CTkButton(self,command=lambda:self.num("8"),text="8",width=75,corner_radius=50,hover_color="green")
        n8.place(x=110,y=200)
        n9=ct.CTkButton(self,command=lambda:self.num("9"),text="9",width=75,corner_radius=50,hover_color="green")
        n9.place(x=200,y=200)


        #calculating the sales
        def cal():
            data=db.calc()
            calc1.configure(text=f"CASH  :  {data[0]}")
            calc2.configure(text=f"UPI      :   {data[1]}")
        calc=ct.CTkButton(self,command=cal,text="CALCULATE",corner_radius=50,hover_color="green")
        calc.place(x=30,y=480)
        calc1=ct.CTkLabel(self,text="")
        calc1.place(x=200,y=480)
        calc2=ct.CTkLabel(self,text="")
        calc2.place(x=200,y=510)
        self.inf=ct.CTkLabel(self,text="")
        self.inf.place(x=400,y=170)


    def run(self):
        #calling the main window
        self.main_w()
        self.mainloop()



if __name__=="__main__":
    bill=App()
    bill.run()