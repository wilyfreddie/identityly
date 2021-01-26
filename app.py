from facerecog_module import *
import mysql.connector
import os

def edit_menu():
     userlist = []
     mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database = "users"
     )

     mycursor = mydb.cursor()
     mycursor.execute("""
        SELECT Person FROM ImageDB;
     """)

     rows = mycursor.fetchall() #returns tuples with one entry (Name)

     count = 1
     print("Which entry do you want to edit?\n")

     for x in rows:
        print("{0}. {1}".format(count, x[0]))
        userlist.append(x[0])
        count += 1

     print("{0}. Back".format(count))

     try:
        selection = int(input("\n Enter number: "))
        if selection == count:
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
        elif selection < count:
            os.system('cls' if os.name == 'nt' else 'clear')
            edit_entry(userlist[selection-1])
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Not valid input!")
            edit_menu()

        os.system('cls' if os.name == 'nt' else 'clear')
     except:
        print("Not a valid input!")
        edit_menu()

def edit_entry(name):
    print("Editing: ", name)
    print("1. Read from file")
    print("2. Manual Input")
    print("3. Back")
    try:
        select = int(input("Enter number: "))

        if select == 1:
            read_file(name)
        elif select == 2:
            print("======ENTER NEW DETAILS======")
            schoolid = int(input("Enter new ID: "))
            age = int(input("Age: "))
            course = input("Course: ")
            graduate = input("Graduate (true/false): ")
            
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database = "users"
            )

            mycursor = mydb.cursor()
            
            mycursor.execute("""UPDATE ImageDB SET ID = {0}, Age = {1}, Course = '{2}', Graduate = {3} WHERE Person = '{4}'""".format(schoolid, age, course, graduate, name))
            mydb.commit()
            # mycursor.close()
            # os.system('cls' if os.name == 'nt' else 'clear')
            print("User details for {0} have been updated in the database!".format(name))
            

        elif select == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            edit_menu()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Not a valid input!")
            edit_entry(name)

    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Not a valid input!")
        edit_entry(name)
        
def read_file(name):
    path = input("Enter file: ")
    try: 
        f = open(path, "r")
        info = f.readlines()
        mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database = "users"
            )

        mycursor = mydb.cursor()
        
        mycursor.execute("""UPDATE ImageDB SET ID = {0}, Age = {1}, Course = '{2}', Graduate = {3} WHERE Person = '{4}'""".format(info[0], info[1], info[2], info[3], name))
        mydb.commit()
        mycursor.close()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("User details for {0} have been updated in the database!".format(name))
        main()
    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("No such file!")
        edit_entry(name)

def get_data(name):
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database = "users"
    )
    mycursordict = mydb.cursor(dictionary=True)
    mycursordict.execute("SELECT ID, Age, Course, Graduate FROM ImageDB WHERE Person = '{0}'".format(name))
    match = mycursordict.fetchall() #returns dictionary
    print("Name: ",name)
    for info in match:
        print("ID: ", info["ID"])
        print("Age: ", info["Age"])
        print("Course: ", info["Course"])
        if info["Graduate"] == 0:
            print("Graduate: True")
        else:
            print("Graduate: False")
    main()

def view_entry():
     userlist = []
     mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database = "users"
     )

     mycursor = mydb.cursor()
     mycursordict = mydb.cursor(dictionary=True)
     mycursor.execute("""
        SELECT Person FROM ImageDB;
     """)

     rows = mycursor.fetchall() #returns tuples with one entry (Name)

     count = 1
     print("Which entry do you want to view?\n")

     for x in rows:
        print("{0}. {1}".format(count, x[0]))
        userlist.append(x[0])
        count += 1

     print("{0}. Back".format(count))

     try:
        selection = int(input("\nEnter number: "))
        print("selection: " ,selection)
        if selection == count:
            os.system('cls' if os.name == 'nt' else 'clear')
            return
        else:
            get_data(userlist[selection-1])

     except:
        print("Not a valid input!")
        view_entry()

def main():
    print(
        """
        Welcome! Choose an action below:

        1. Match image to database
        2. Add entry to database
        3. Edit entry in database
        4. View entry
        5. Exit
        """
    )

    try:
        choice = int(input("""
        Enter number of choice:
        """))
        if choice == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            CheckFace()
            
        elif choice == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            AddFace()
            
        elif choice == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            edit_menu()
            
        elif choice == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
            view_entry()
            
        elif choice == 5:
            pass
        else:
            print("Not a valid input!\n")
    
    except:
        print("Not a valid input!\n")
    



if __name__ == "__main__":
    main()
