import mysql.connector as my

con=my.connect(host="localhost",user="root",passwd="harsh123",database="bank")
cursor=con.cursor()


#employee
def show():
    
    acc=input("\nenter account number:")
    
    cursor.execute("select exists(select * from info where accno=%s)",(acc,))
    ch=cursor.fetchone()
        
    if(ch[0]==0):
        print("\naccount does not exists\n")
    
    else:
        print("\n***customer details***")
        print("\n(name ,phone number ,account number ,balance)\n\n")
        cursor.execute("select * from info where AccNo=%s",(acc,))
        row=cursor.fetchone()
        print(row)
        print("\n")


def show_all():
    
    cursor.execute("select exists(select * from info)")
    ch=cursor.fetchone()
    
    if(ch[0]==0):
        print("\nno records found\n")
    
    else:
        print("\n***customers details***")
        print("\n(name ,phone number ,account number ,balance)\n")
        cursor.execute("select * from info")
   
        for row in cursor.fetchall():
            print(row)
        print("\n")


def insert():
    print("\n***enter details of user***\n")
    name=input("enter your name:") 
    pno=input("enter phone number:")
    acc=input("enter account number:")
    type=input("enter type of account:")
    balance=input("enter balance:")
    pas=input("enter default password:")
    cursor.execute("select exists(select * from info where accno=%s)",(acc,))
    ch=cursor.fetchone()
   
    if(ch[0]==1):
        print("\naccount number already exists\n")
   
    else:
        cursor.execute("insert into info values(%s,%s,%s,%s,%s,%s)",(name,pno,acc,type,balance,pas))
        con.commit()
        cursor.execute("insert into user_login values(%s,%s)",(acc,pas))
        con.commit()
        
        print("\ndetails inserted into database and login id and password is created you can change password later\n")



def delete():
   
    acc=input("\nenter account number:")
    
    cursor.execute("select exists(select * from info where accno=%s)",(acc,))
    ch=cursor.fetchone()
   
    if(ch[0]==0):
        print("\naccount does not exists\n")
   
    else:
        cursor.execute("delete from info where AccNo=%s",(acc,))
        con.commit()
        cursor.execute("delete from user_login where AccNo=%s",(acc,))
        con.commit()

        print("customers details deleted from the database\n")


def update():

    choice =1
    
    acc=input("\nenter account number:")
    while(choice):
       
        cursor.execute("select exists(select * from info where accno=%s)",(acc,))
        ch=cursor.fetchone()
       
        if(ch[0]==0):
            print("\naccount does not exists\n")
       
        else:
            choice=int(input("0:exit\n1:update name\n2:update phone number\nenter your choice:"))
        
            if(choice==0):
                print("\nthank you\n")
                break
            
            if(choice==1):
                name=input("enter new name:")
                cursor.execute("update info set name=%s where AccNo=%s",(name,acc))
                con.commit()
                print("name updated successfully")

            elif(choice==2):
                pno=input("enter new phone number:")
                cursor.execute("update info set pno=%s where accno=%s",(pno,acc))
                con.commit()
                print("phone number updated successfully")

            else:
                print("invalid")
            
            print("\n")


def emp_pas(id):
    p=input("\nenter new login password:")
    cursor.execute("update emp_login set pass=%s where id=%s",(p,id))
    con.commit()
    print("employees password changed\n")


#user
def withdrawal(amt,acc):
    cursor.execute("select balance from info where accno=%s",(acc,))
    total=cursor.fetchone()
    if(float(total[0])<amt):
        print("not enough balance\n")
    
    else:
        new=float(total[0])-amt

        cursor.execute("update info set balance=%s where accno=%s",(str(new),acc))
        con.commit()
        print("amount updated successfully")
       

def deposit(amt,acc):
    cursor.execute("select balance from info where accno=%s",(acc,))
    total=cursor.fetchone()
    new=float(total[0])+amt

    cursor.execute("update info set balance=%s where accno=%s",(str(new),acc))
    con.commit()
    print("amount updated successfully")
     

def check_bal(acc):
    cursor.execute("select balance from info where accno=%s",(acc,))
    bal=cursor.fetchone()
    print("\nbalance=",bal[0],"\n")
        

def user_pas(acc):
    p=input("\nenter new login password:")
    cursor.execute("update user_login set pass=%s where accno=%s",(p,acc))
    con.commit()
    print("users password changed\n")


#main
print("\n***welcome to banking record management system***\n")
login_choice=1

while(login_choice):
    login_choice=int(input ("0:exit\n1:employee login\n2:user login\n3:create employee id\nenter your choice:"))
       
    if(login_choice==0):
        print("\nthank you")
        
    elif(login_choice==1):
        print("\nEMPLOYEE LOGIN\n")
        id=input("enter id:")
        pas=input("enter password:")

        cursor.execute("select exists(select * from emp_login where id=%s and pass=%s)",(id,pas))
        check=cursor.fetchone()

        if(check[0]==0):
            print("\ninvalid username or password\n")
        
        else:
            emp_choice=1
            
            while(emp_choice):
                emp_choice=int(input("\n0:sign out\n1:insert\n2:delete\n3:update\n4:print\n5:change login password\nenter your choice:"))
                
                if(emp_choice==0):
                    print("\nthank you\n")
                    break

                elif(emp_choice==1):
                    insert()

                elif(emp_choice==2):
                    delete()
                
                elif(emp_choice==3):
                    update()
                
                elif(emp_choice==4):
                    print_choice=int(input("\n1:show all records\n2:show records of perticular user\nenter your choice:"))
                
                    if(print_choice==1):
                        show_all()
                
                    elif(print_choice==2):
                        show()
                
                    else:
                        print("\ninvalid choice\n")
                
                elif(emp_choice==5):
                    emp_pas(id)

                else:
                    print("\ninvalid choice\n")   
    
    elif(login_choice==2):
        print("\nUSER LOGIN\n")
        acc=input("enter account number:")
        pas=input("enter password:")

        cursor.execute("select exists(select * from user_login where accno=%s and pass=%s)",(acc,pas))
        check=cursor.fetchone()
        
        if(check[0]==0):
            print("\ninvalid username or password\n")
        
        else:
            user_choice=1
            
            while(user_choice):
                user_choice=int(input("\n0:sign out\n1:withdrawal\n2:deposit\n3:check balance\n4:change login password\nenter your choice:"))
                if(user_choice==0):
                    print("\nthank you\n")
                
                elif(user_choice==1):
                    ammount=float(input("\nenter ammount:"))
                    
                    if(ammount<1):
                        print("\ninvalid ammount\n")
                    
                    else:
                        withdrawal(ammount,acc)
                
                elif(user_choice==2):
                    ammount=float(input("\nenter ammount:"))
                    
                    if(ammount<1):
                        print("\ninvalid ammount\n")
                    
                    else:
                        deposit(ammount,acc)
                
                elif(user_choice==3):
                    check_bal(acc)

                elif(user_choice==4):
                    user_pas(acc)

                else:
                    print("\ninvalid choice\n")

    elif(login_choice==3):
        id=input("\nenter employee id:")
        pas=input("enter password:")

        cursor.execute("select exists(select * from emp_login where id=%s)",(id,))
        
        exists = cursor.fetchone()[0]
        if exists:
            print("\nid already exists\n")
        
        else:
            cursor.execute("insert into emp_login values(%s,%s)",(id,pas))
            con.commit()
            print("\n Employee Id Successfully Created\n")
            print("\n")

    else:
        print("\ninvalid choice\n")
