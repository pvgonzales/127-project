# SUPER IMPORTANT REMINDERS:
# Make sure that you have installed python and mysql-connector-python on your device
# For guides, https://youtu.be/sdZMlv1ZSK8?feature=shared
# Must also have mariadb installed, run the sql files (create and insert queries ONLY) from project milestone 3
import mysql.connector as mariadb 
from datetime import datetime

connection = mariadb.connect(user='project', password='127', database='review', host='localhost')
cursor = connection.cursor()

# SAMPLES:
# select = 'SELECT * FROM establishment'
# cursor.execute(select) --> use execute for all queries
# result = cursor.fetchall() --> use fetchall() for SELECT statements
# connection.commit() --> for INSERT and UPDATE
# for DELETE, just use .execute ONLY

# REMINDER:
#   When using variables for insert statements, store the variable as the 2nd argument in .execute()
# - Example: 
#   insert = 'INSERT INTO establishment (estid, estname) VALUES (%d, %s)'
#   variable = (4, 'Jollibee')
#   cursor.execute(insert, variable)
#   connection.commit()
# IMPORTANT VARIABLES FOR THIS PROGRAM: 
#    - connection
#    - cursor
# LAST REMINDER: 
#   Do not forget to close mariadb if you wish to exit the program
#    - connection.close()


def mainMenu():
    print('\n[1] Add an establishment')
   # print('[2] Add a food item')
   # print('[3] Add a review')
    print('[2] Search an establishment')
    print('[3] View reviews')
    print('[4] Search food items')
   # print('[7] Reports')
    print('[0] Log Out')
    choice = int(input('Enter choice: '))
    return choice


def registerAcc():
    user = None
    isLoggedin = False
    isRegistered = False
    print('\n[1] Sign up')
    print('[2] Sign in')
    print('[0] Exit')
    choice = int(input('Enter choice: '))
    if choice == 1:
        name = input('Enter name: ')
        strbday = input('Enter birthday: ')
        format_bday = "%m-%d-%Y"
        bday = datetime.strptime(strbday, format_bday)
        while True:
            email = input('Enter email address: ')
            select = 'SELECT email FROM customer'
            cursor.execute(select)
            customerList = cursor.fetchall()
            for i in customerList:
                if email == i[0]:
                    emailunique = False
                    print('\nEmail already exists.\n')
                    break
                else:
                    emailunique = True
            if emailunique == True:
                break
            else:
                continue
        password = input('Enter password: ')
        while True:
            verifyPass = input('Re-enter password: ')
            if password != verifyPass:
                print('\nPasswords do not match. Please try again.\n')
                continue
            else:
                break
        insertCustomer = 'INSERT INTO customer (email, pass, full_name, bday) VALUES (%s, %s, %s, %s)'
        customerValues = (email, password, name, bday)
        cursor.execute(insertCustomer, customerValues)
        connection.commit()
        isRegistered = True
    elif choice == 2:
        email = input("Enter email: ")
        password = input("Enter password: ")
        select = 'SELECT email, pass FROM customer'
        cursor.execute(select)
        customerList = cursor.fetchall()
        for i in customerList:
            if email == i[0] and password == i[1]:
                isLoggedin = True
                user = email
    elif choice == 0:
        connection.close()
        exit()
    else:
        print('\nInvalid choice. Please try again.')
    return isLoggedin, isRegistered, user

def addEstablishment():
    try:
        estname = input('Enter establishment name: ')
        capacity = int(input("Enter " + estname +"'s capacity: "))
        contact = int(input("Enter contact number: "))
        insertEst = 'INSERT INTO establishment (estname, capacity, contactno) VALUES (%s, %s, %s)'
        estValues = (estname, capacity, contact)
        cursor.execute(insertEst, estValues)
        connection.commit()
        while True:
            loc = input("Enter establishment's address: ")
            selectEst = ("SELECT e.estid FROM establishment e WHERE estname LIKE '%%%s%%'" % estname)
            cursor.execute(selectEst)
            selEst = cursor.fetchall()
            for i in selEst:
                estid = i[0]
            insertAdd = 'INSERT INTO estaddress (estid, loc) VALUES (%s, %s)'
            addValues = (estid, loc)
            cursor.execute(insertAdd, addValues)
            connection.commit()
            while True:
                choice = input('Add another address? (Y|N): ')
                if choice == 'Y':
                    break
                elif choice == 'N':
                    print('Would you like to add food items? (Y/N)')
                    addChoice = input('Enter choice: ')
                    if addChoice == 'Y':
                        addFood = addFoodItem(estid)
                        return addFood
                    elif addChoice == 'N':
                        return True
                else:
                    print('\nInvalid choice. Please try again.\n')
    except:
        return False

def addFoodItem(estid):
    try: 
        foodname = input('Enter food name: ')
        fooddesc = input('Enter food description: ')
        foodprice = float(input('Enter food price: '))
        # selectEst = ("SELECT e.estid FROM establishment e WHERE estname LIKE '%%%s%%'" % estname)
        # cursor.execute(selectEst)
        # selEst = cursor.fetchall()
        # for i in selEst:
        #     estid = i[0]
        insertFood = 'INSERT INTO fooditem (foodname, fooddesc, foodprice, estid) VALUES (%s, %s, %s, %s)'
        foodValues = (foodname, fooddesc, foodprice, estid)
        cursor.execute(insertFood, foodValues)
        connection.commit()
        while True:
            foodtype = input('Enter food type: ')
            selectFood = ("SELECT f.foodid FROM fooditem f WHERE foodname LIKE '%%%s%%'" % foodname)
            cursor.execute(selectFood)
            selFood = cursor.fetchall()
            for i in selFood:
                foodid = i[0]
            insertType = 'INSERT INTO foodtype (foodid, foodtype) VALUES (%s, %s)'
            typeValues = (foodid, foodtype)
            cursor.execute(insertType, typeValues)
            connection.commit()
            while True:
                choice = input('Add another food type? (Y|N): ')
                if choice == 'Y':
                    break
                elif choice == 'N':
                    return True
                else:
                    print('\nInvalid choice. Please try again.\n')
    except:
        return False

def addReviews(userInfo, estid, foodid):
    try:
        rate = int(input('Enter rating (1-5): '))
        feedback = input('Share your experience: ')
        insertreview = 'INSERT INTO reviews (email, estid, foodid, rate, reviewdate, reviewtime, feedback) VALUES (%s, %s, %s, %s, CURDATE(), CURTIME(), %s)'
        revValues = (userInfo, estid, foodid, rate, feedback)
        cursor.execute(insertreview, revValues)
        connection.commit()
        return True
    except:
        return False

def addReviewEst(userInfo, estid):
    try:
        rate = int(input('Enter rating (1-5): '))
        feedback = input('Share your experience: ')
        insertreview = 'INSERT INTO reviewsest (email, estid, rate, reviewdate, reviewtime, feedback) VALUES (%s, %s, %s, CURDATE(), CURTIME(), %s)'
        revValues = (userInfo, estid, rate, feedback)
        cursor.execute(insertreview, revValues)
        connection.commit()
        return True
    except:
        return False

def searchEstablishment(userInfo):
    try:
        estname = input("Enter establishment: ")
        select = ("SELECT * FROM establishment WHERE estname LIKE '%%%s%%'" % estname)
        cursor.execute(select)
        est = cursor.fetchall()
        if len(est) != 0:
            print(f"{'Establishment Name':<30}{'Capacity':<20}{'Contact Number':<30}")
            print('-------------------------------------------------------------')
            for j in est:
                print(f"{j[1]:<30}{j[2]:<20}{j[3]:<30}")
                estid = j[0]
            while True:
                print("\n[1] Add an establihsment review")
                print("[2] Search food items")
                print("[3] Update the establishment")
                print("[4] Delete establishment")
                print("[0] Back to Main Menu")
                choice = int(input("Enter choice: "))
                if choice == 2:
                    foodname = input("Enter food name: ")
                    selectFood = ("SELECT * FROM fooditem WHERE foodname LIKE '%%%s%%'" % foodname)
                    cursor.execute(selectFood)
                    food = cursor.fetchall()
                    if len(food) != 0:
                        print(f"{'Food Name':<30}{'Food Description':<50}{'Price':<10}")
                        print('-------------------------------------------------------------------------------------------')
                        for j in food:
                            print(f"{j[1]:<30}{j[2]:<50}{float(j[3]):<10.2f}")
                            foodid = j[0]
                        print("\n[1] Add a food review")
                        print("[2] Update food item")
                        print("[3] Delete food item")
                        print("[0] Back to Main Menu")
                        revchoice = int(input("Enter choice: "))
                        if revchoice == 1:
                            reviews = addReviews(userInfo, estid, foodid)
                            return reviews
                        elif revchoice == 2:
                            return ############################################
                        elif revchoice == 3:
                            return ############################################
                        elif revchoice == 0:
                            return
                        break
                    else:
                        print("\n"+foodname+" does not exist.")
                elif choice == 1:
                    estrev = addReviewEst(userInfo, estid)
                    return estrev
                elif choice == 3:
                    updEst = updateEstablishment(est) ########################
                    return updEst
                elif choice == 4:
                    return #####################################################
                elif choice == 0:
                    return
                else:
                    print("\nInvalid choice. Please try again.")
        else:
            print("\n"+estname+" does not exist.")
    except:
        return False

def updateEstablishment(establishment): #########################################
    try:
        print('UPDATE')
    except:
        return False

def viewAllEstablishments():
    selectEst = 'SELECT * FROM establishment'
    cursor.execute(selectEst)
    result = cursor.fetchall()
    print("Available Establishments:")
    for i in result:
        print("★ " + i[1])
    while True:
        print("\n[1] Show establishment details")
        print("[0] Back to main menu")
        choice = int(input("Enter choice: "))
        if choice == 1:
            break
        elif choice == 0:
            return
        else:
            print('\nInvalid choice. Please try again.')
    estname = input("Enter establishment to be shown: ")
    for i in result:
        if estname == i[1]:
            estid = i[0]
            print("★ "+ estname +" ★")
            print("Capacity:", i[2])
            print("Contact number:", i[3])
            print("\n★ " + estname + "'s Food Items ★\n")
            selectFood = ("SELECT * FROM fooditem WHERE estid LIKE '%%%s%%'" % estid)
            cursor.execute(selectFood)
            foods = cursor.fetchall()
            print(f"{'Food Name':<30}{'Food Description':<50}{'Price':<10}")
            print('-------------------------------------------------------------------------------------------')
            for j in foods:
                print(f"{j[1]:<30}{j[2]:<50}{float(j[3]):<10.2f}")
            return


def viewReviews():
    while True:
        print("[1] Search reviews for an establishment only")
        print("[2] Search reviews for establishment and food item")
        choice = int(input("Enter choice: "))
        if choice == 1:
            estname = input("Enter establishment name: ")
            selId = ("SELECT * FROM establishment WHERE estname LIKE '%%%s%%'" % estname)
            cursor.execute(selId)
            ests = cursor.fetchall()
            if len(ests) != 0:
                for i in ests:
                    if estname == i[1]:
                        estid = i[0]
                select = ("SELECT * FROM reviewsest WHERE estid LIKE '%%%s%%'" % estid)
                cursor.execute(select)
                rev = cursor.fetchall()
                print("Customer Reviews for " + estname + "\n")
                print(f"{'Customer Name':<30}{'Establishment Name':<30}{'Rating':<10}{'Date':<20}{'Time':<20}{'Feedback':<50}")
                print('---------------------------------------------------------------------------------------------------------------------------------------------')
                for i in rev:
                    selCus = ("SELECT full_name FROM customer WHERE email LIKE '%%%s%%'" % i[0])
                    cursor.execute(selCus)
                    custs = cursor.fetchall()
                    for j in custs:
                        time_secs = int(i[4].total_seconds())
                        hours = time_secs // 3600
                        mins = (time_secs % 3600) // 60
                        secs = time_secs % 60
                        print(f"{j[0]:<30}{estname:<30}{i[2]:<10}{(i[3].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{i[5]:<50}")
                return
            else:
                print("\n" + estname + " does not exist.")
        if choice == 2:
            estname = input("Enter establishment name: ")
            foodname = input("Enter food item: ")
            selId = ("SELECT * FROM establishment WHERE estname LIKE '%%%s%%'" % estname)
            cursor.execute(selId)
            ests = cursor.fetchall()          
            selFoodId = ("SELECT * FROM fooditem WHERE foodname LIKE '%%%s%%'" % foodname)
            cursor.execute(selFoodId)
            food = cursor.fetchall()
            if len(ests) != 0 and len(food) != 0:
                for i in ests:
                    if estname == i[1]:
                        estid = i[0]  
                for i in food:
                    if foodname == i[1]:
                        foodid = i[0]
                select = ("SELECT * FROM reviews WHERE estid LIKE '%%%s%%' AND foodid LIKE '%%%s%%'" % (estid, foodid))
                cursor.execute(select)
                rev = cursor.fetchall()
                print("Customer Reviews for " + foodname + " of " + estname + "\n")
                print(f"{'Customer Name':<25}{'Establishment Name':<30}{'Food Name':<20}{'Rating':<10}{'Date':<20}{'Time':<20}{'Feedback':<50}")
                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                for i in rev:
                    selCus = ("SELECT full_name FROM customer WHERE email LIKE '%%%s%%'" % i[0])
                    cursor.execute(selCus)
                    custs = cursor.fetchall()
                    for j in custs:
                        time_secs = int(i[5].total_seconds())
                        hours = time_secs // 3600
                        mins = (time_secs % 3600) // 60
                        secs = time_secs % 60
                        print(f"{j[0]:<25}{estname:<30}{foodname:<20}{i[3]:<10}{(i[4].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{i[6]:<50}")
                return
            else:
                print("\n" + estname + " and " + foodname + " does not exist.")
        else:
            print("\nInvalid Choice. Please try again. \n")
        
def searchFoodItems():
    while True:
        print('[1] Search food items by price')
        print('[2] Search food items by food type')
        # print('[3] Search food items by both price and food type') --> not sure yet, ang hirap nya T__T
        choice = int(input("Enter choice: "))
        if choice == 1:
            foodprice = input("Enter price range (separate by comma): ")
            price = foodprice.split(',')
            selFood = ("SELECT * FROM fooditem WHERE foodprice BETWEEN %s AND %s ORDER BY foodprice ASC" % (float(price[0]), float(price[1])))
            cursor.execute(selFood)
            price = cursor.fetchall()
            if len(price) != 0:
                print("\n")
                print(f"{'Food Name':<30}{'Food Description':<60}{'Price':<30}{'Establishment Name':<20}")
                print('--------------------------------------------------------------------------------------------------------------------------------------------')
                for j in price:
                    selEstName = ("SELECT estname FROM establishment WHERE estid LIKE %s" % j[4])
                    cursor.execute(selEstName)
                    ests = cursor.fetchall()
                    for k in ests:
                        print(f"{j[1]:<30}{j[2]:<60}{float(j[3]):<30.2f}{k[0]:<20}")
                return
        elif choice == 2:
            foodtype = input("Enter food type: ")
            selFood = ("SELECT * FROM foodtype WHERE foodtype LIKE '%%%s%%'" % foodtype)
            cursor.execute(selFood)
            ftype = cursor.fetchall()                
            if len(ftype) != 0:
                print("\n")
                print(f"{'Food Name':<30}{'Food Description':<60}{'Price':<15}{'Food Type':<20}{'Establishment Name':<20}")
                print('----------------------------------------------------------------------------------------------------------------------------------------------------')
                for i in ftype:
                    selFoodInfo = ("SELECT * FROM fooditem WHERE foodid LIKE %s" % i[0])
                    cursor.execute(selFoodInfo)
                    foods = cursor.fetchall()
                    for j in foods:
                        selEstName = ("SELECT estname FROM establishment WHERE estid LIKE %s" % j[4])
                        cursor.execute(selEstName)
                        ests = cursor.fetchall()
                        for k in ests:
                            print(f"{j[1]:<30}{j[2]:<60}{float(j[3]):<15.2f}{i[1]:<20}{k[0]:<20}")
            return
        elif choice == 3:
            return
        else:
            print("\nInvalid Choice. Please try again.\n")

# Main Program
while True:
    account, register, userCredentials = registerAcc()
    if account:
        print('\nLogged in successfully!')
        while True:
            choice = mainMenu()
            if choice == 1:
                est = addEstablishment()
                if est:
                    print('\nEstablishment added successfully.')
            # elif choice == 2:
            #     food = addFoodItem()
            #     if food:
            #         print('\nFood item added successfully.')
            # elif choice == 3:
            #     rev = addReviews(userCredentials)
            #     if rev:
            #         print('\nReview submitted successfully.')
            elif choice == 2:
                searchEstablishment(userCredentials)
            elif choice == 3:
                viewReviews()
            elif choice == 4:
                searchFoodItems()
            # elif choice == 7:
            #     viewAllEstablishments()
            elif choice == 0:
                break
            else:
                print('\nInvalid Choice')
    elif register:
        print('\nYour account has been registered.\n')
        continue
    else: # May bug itong part na ito
        print('\nInvalid email or password')
        continue