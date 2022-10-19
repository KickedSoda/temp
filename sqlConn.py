from operator import indexOf
from unicodedata import decimal
import mysql.connnector
import uuid
from datetime import datetime
from cryptography.fernet import Fernet
from tkinter import *

root = Tk()
root.title('Login/Signup')
root.geometry("300x200")

#connects to the sql data base
myDB = mysql.connector.connect(
    user = "root",
    password = "^NmQH%y=s!0,n2XH6@2TMRZH-!ZfoW:#W#CjqfN1T@,ho!yu]%w0bBpJ%5b^}-TDxga,r",
    host = "127.0.0.1",
    database = "landing_page"
)

#sets the client to be the database's cursor
client = myDB.cursor()

#loads_key
def load_key():
    return open("key.key", "rb").read()

#loads key from the function
key = load_key()

#sets f as out key "client"
f = Fernet(key)
    
#checks to see if the uuid is the same as any others
def checkRandom(userID):
    client.execute(f"SELECT user_id FROM login_data WHERE user_id = '{userID}'")
    if client.fetchone() != None:
        print("userid taken, making new id")
        return True
    else:
        return False
        
#signs a user up and stores data into the sql database
def signUp(username, password):
    now = datetime.now()
    dt_string = now.strftime("%y-%m-%d %H:%M:%S")
    
    password = f.encrypt(password.encode())
    
    personal_key = Fernet.generate_key()
    p = Fernet(personal_key)
    
    personal_key = f.encrypt(personal_key)
    password = p.encrypt(password)
    
    userID = uuid.uuid4()
    while checkRandom(userID) == True:
        userID = uuid.uuid4()
        print(userID)
        checkRandom(userID)
        
    insert = f"INSERT INTO login_data VALUES('{userID}', '{username}', \"{password}\", '{dt_string}', \"{personal_key}\");"
    
    client.execute(insert)
    client.execute("SELECT * FROM login_data")
    print(client.fetchall())
    callSignUp("Account created!", "green")
    

def logIn(username, password):
    client.execute(f"SELECT password FROM login_data WHERE username = '{username}';")
    passData = str(client.fetchone())
    client.execute(f"SELECT personal_key FROM login_data WHERE username = '{username}';")
    persoanlKeyData = str(client.fetchone())
    decrypted_personal_key = str(f.decrypt(persoanlKeyData[4: len(persoanlKeyData) - 4].encode()))
    p = Fernet(decrypted_personal_key[2: len(passData) - 5])
    passData = p.decrypt((passData[4: len(passData) - 4]).encode())
    decrypted_pass = str(f.decrypt(passData))
    if decrypted_pass[2: len(decrypted_pass) - 1] == password:
        callLogin(f"{username} is logged in!", "green")
    else:
        callLogin("Password incorrect!", "red")
    

def usernameExists(username):
    client.execute(f"SELECT username FROM login_data WHERE username = '{username}'")
    if client.fetchone() != None:
        return True
    else:
        return False
    
l5 = Label(root)
l6 = Label(root)
def callLogin(err, color):
    l5.config(text = err, fg = color)
    l5.grid(row = 3, column = 0, sticky = W, pady = 2)  

def callSignUp(err, color):
    l6.config(text = err, fg = color)
    l6.grid(row = 8, column = 0, sticky = W, pady = 2)


def getLoginInfo():
    username = e1.get()
    password = e2.get()
    if usernameExists(username) == False:
        callLogin("Username Does not exists!", "red")
    else:
        logIn(username, password)
    
def getSignUpInfo():
    username = e3.get()
    password = e4.get()
    if usernameExists(username) == True:
        callSignUp("Username already exists!", "red")
    elif len(password) > 25:
        callSignUp("That password is too long!", "red")
    elif len(password) < 6:
        callSignUp("That password is too short!", "red")
    else:
        signUp(username, password)
def main():   
    '''# this will create a label widget
    l1 = Label(root, text = "Username:")
    l2 = Label(root, text = "Password:")
    
    # grid method to arrange labels in respective
    # rows and columns as specified
    l1.grid(row = 0, column = 0, sticky = W, pady = 2)
    l2.grid(row = 1, column = 0, sticky = W, pady = 2)
    
    # this will arrange entry widgets
    e1.grid(row = 0, column = 1, pady = 2)
    e2.grid(row = 1, column = 1, pady = 2)
    
    b1 = Button(root, text="Log In", command = getLoginInfo)
    b1.grid(row = 3, column = 1, pady = 4)
    
    l3 = Label(root, text = "Dont have an account?")
    l3.grid(row = 5, column = 0, sticky = W, pady = 3)
    
    # this will create a label widget
    l4 = Label(root, text = "Username:")
    l5 = Label(root, text = "Password:")
    
    # grid method to arrange labels in respective
    # rows and columns as specified
    l4.grid(row = 6, column = 0, sticky = W, pady = 2)
    l5.grid(row = 7, column = 0, sticky = W, pady = 2)
    
    # this will arrange entry widgets
    e3.grid(row = 6, column = 1, pady = 2)
    e4.grid(row = 7, column = 1, pady = 2)
    
    b2 = Button(root, text="Sign Up", command = getSignUpInfo,)
    b2.grid(row = 8, column = 1, pady = 4)
    
    root.mainloop()'''   
    client.execute("SELECT COUNT(password) FROM login_data")
    print(client.fetchone())
      
e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root)
e4 = Entry(root)  
   
main()



myDB.commit()
client.close()
myDB.close()