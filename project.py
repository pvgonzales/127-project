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
    print('[2] View all establishments')
    print('[3] View reviews')
    print('[4] Search food items')
    print('[0] Log Out')
    choice = int(input('Enter choice: '))
    return choice


def registerAcc():
    try:
        user = None
        isLoggedin = False
        isRegistered = False
        print('\n[1] Sign up')
        print('[2] Sign in')
        print('[0] Exit')
        choice = int(input('Enter choice: '))
        if choice == 1:
            name = input('Enter name: ')
            strbday = input('Enter birthday (MM-DD-YYY): ')
            format_bday = "%m-%d-%Y"
            bday = datetime.strptime(strbday, format_bday)
            today = datetime.today()
            age = today.year - bday.year
            if (today.month, today.day) < (bday.month, bday.day):
                age -= 1
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
            insertCustomer = 'INSERT INTO customer (email, pass, full_name, bday, age) VALUES (%s, %s, %s, %s, %s)'
            customerValues = (email, password, name, bday, age)
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
    except:
        return False

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

def searchEstablishment(userInfo, estname):
    try:
        # estname = input("Enter establishment: ")
        select = ("SELECT * FROM establishment WHERE estname LIKE '%%%s%%'" % estname)
        cursor.execute(select)
        est = cursor.fetchall()
        if len(est) != 0:
            print(f"{'Establishment Name':<30}{'Capacity':<20}{'Contact Number':<30}")
            print('----------------------------------------------------------------------')
            for j in est:
                print(f"{j[1]:<30}{j[2]:<20}{j[3]:<30}")
                estid = j[0]
            while True:
                print("\n[1] Add an establihsment review")
                print("[2] Add a food item")
                print("[3] View food items")
                print("[4] Update the establishment")
                print("[5] Delete establishment")
                print("[0] Back to Main Menu")
                choice = int(input("Enter choice: "))
                if choice == 3:
                    selectFood = ("SELECT * FROM fooditem WHERE estid=%s ORDER BY price" %estid)
                    cursor.execute(selectFood)
                    foods = cursor.fetchall()
                    if len(foods) != 0:
                        print(f"{'Food Name':<30}{'Food Description':<50}{'Price':<10}")
                        print('-------------------------------------------------------------------------------------------')
                        for j in foods:
                            print(f"{j[1]:<30}{j[2]:<50}{float(j[3]):<10.2f}")
                        print("\n[1] Add a food review")
                        print("[2] Update food item")
                        print("[3] Delete food item")
                        print("[0] Back to Main Menu")
                        revchoice = int(input("Enter choice: "))
                        if revchoice == 1:
                            foodname = input("Enter food name: ")
                            selectFood = ("SELECT * FROM fooditem WHERE foodname LIKE '%%%s%%'" % foodname)
                            cursor.execute(selectFood)
                            food = cursor.fetchall()
                            for i in food:
                                foodid = i[0]                            
                            reviews = addReviews(userInfo, estid, foodid)
                            return reviews
                        elif revchoice == 2:
                            foodname = input("Enter food name: ")
                            selectFood = ("SELECT * FROM fooditem WHERE foodname LIKE '%%%s%%'" % foodname)
                            cursor.execute(selectFood)
                            food = cursor.fetchall()       
                            upds = updateFoodItem(est, food)
                            return upds
                        elif revchoice == 3:
                            foodname = input("Enter food name: ")
                            selectFood = ("SELECT * FROM fooditem WHERE foodname LIKE '%%%s%%'" % foodname)
                            cursor.execute(selectFood)
                            food = cursor.fetchall() 
                            delfood = deleteFoodItem(est, food)
                            return delfood
                        elif revchoice == 0:
                            return
                        break
                    else:
                        print("\nThere are not available food items.")
                elif choice == 1:
                    estrev = addReviewEst(userInfo, estid)
                    return estrev
                elif choice == 2:
                    estrev = addFoodItem(estid)
                    return estrev
                elif choice == 4:
                    updEst = updateEstablishment(est)
                    return updEst
                elif choice == 5:
                    delEst = deleteEstablishment(est)
                    return delEst
                elif choice == 0:
                    return
                else:
                    print("\nInvalid choice. Please try again.")
        else:
            print("\n"+estname+" does not exist.")
    except:
        return False
    
def deleteFoodItem(establishment, food):
    try:
        for i in establishment:
            estid = i[0]
        
        for i in food:
            foodid = i[0]
            foodname = i[1]
        while True:
            print("Are you sure deleting " + foodname + "?")
            print("This will delete all information including all reviews.")
            choice = input("Enter choice (Y|N): ")
            if choice == 'Y':
                try:                        
                    deleterevs = "DELETE FROM reviews WHERE estid=%s AND foodid=%s"
                    cursor.execute(deleterevs, (estid, foodid))
                    connection.commit()
                    
                    deleteftypes = "DELETE FROM foodtype WHERE foodid=%s"
                    cursor.execute(deleteftypes, (foodid,))
                    connection.commit()
                
                    deletefoods = "DELETE FROM fooditem WHERE estid=%s AND foodid=%s"
                    cursor.execute(deletefoods, (estid, foodid))
                    connection.commit()

                    print("\nFood item deleted successfully!")
                    return True
                except Exception as e:
                    print(f"Error in deleting food item. {e}")
            elif choice == 'N':
                print("\nDeleting " + foodname + " is cancelled.")
                return True
            else:
                print("\nInvalid choice. Please try again.")
    except:
        return False

def deleteEstablishment(establishment):
    try:
        for i in establishment:
                estid = i[0]
                estname = i[1]
        while True:
            print("Are you sure deleting " + estname + "?")
            print("This will delete all information including all food items and reviews.")
            choice = input("Enter choice (Y|N): ")
            if choice == 'Y':
                try:
                    foodid = []
                    deleterevest = "DELETE FROM reviewsest WHERE estid=%s"
                    cursor.execute(deleterevest, (estid,))
                    connection.commit()
                    
                    selectFood = "SELECT foodid FROM fooditem WHERE estid=%s"
                    cursor.execute(selectFood, (estid,))
                    food = cursor.fetchall()
                    
                    for i in food:
                        foodid.append(i[0])
                    
                    if foodid:
                        placeholders = ','.join(['%s'] * len(foodid))
                        deleterevs = "DELETE FROM reviews WHERE estid=%s AND foodid IN" + f"({placeholders})" #########################
                        cursor.execute(deleterevs, (estid, *foodid))
                        connection.commit()
                        
                        deleteftypes = f"DELETE FROM foodtype WHERE foodid IN ({placeholders})"
                        cursor.execute(deleteftypes, foodid)
                        connection.commit()
                    
                    deletefoods = "DELETE FROM fooditem WHERE estid=%s"
                    cursor.execute(deletefoods, (estid,))
                    connection.commit()
                    
                    deleteestadd = "DELETE FROM estaddress WHERE estid=%s"
                    cursor.execute(deleteestadd, (estid,))
                    connection.commit()
                    
                    deleteest = "DELETE FROM establishment WHERE estid=%s"
                    cursor.execute(deleteest, (estid,))
                    connection.commit()
                    print("\nDeleted successfully!")
                    return True
                except Exception as e:
                    print(f"Error in deleting establishment. {e}")
                    return False

            elif choice == 'N':
                print("\nDeleting " + estname + " is cancelled.")
                return True
            else:
                print("\nInvalid choice. Please try again.")
    except:
        return False


def updateFoodItem(establishment, food):
    try:
        while True:
            for i in establishment:
                estid = i[0]

            for i in food:
                foodid = i[0]
                foodname = i[1]
            print("Choose what you want to be updated")
            print("[1] Food Name")
            print("[2] Food Description")
            print("[3] Food Price")
            print("[4] Add a Food Type")
            print("[5] Edit a Food Type")
            choice = int(input("Enter choice: "))
            if choice == 1:
                foodname = input("Enter new food name: ")
                updname = 'UPDATE fooditem SET foodname=%s WHERE estid=%s AND foodid=%s'
                updvalname = (foodname, estid, foodid)
                try:
                    cursor.execute(updname, updvalname)
                    connection.commit()
                    print("Food name updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error in updating food name. {e}")
            elif choice == 2:
                fooddesc = input("Enter new food description: ")
                upddesc = 'UPDATE fooditem SET fooddesc=%s WHERE estid=%s AND foodid=%s'
                updvaldesc = (fooddesc, estid, foodid)
                try:
                    cursor.execute(upddesc, updvaldesc)
                    connection.commit()
                    print("Food description updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error in updating food description. {e}")
            elif choice == 3:
                price = float(input("Enter new food price: "))
                updprice = 'UPDATE fooditem SET foodprice=%s WHERE estid=%s AND foodid=%s'
                updvalprice = (price, estid, foodid)
                try:
                    cursor.execute(updprice, updvalprice)
                    connection.commit()
                    print("Food price updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error in updating price. {e}")
            elif choice == 4:
                foodtype = input("Enter new foodtype: ")
                instype = 'INSERT INTO foodtype (foodid, foodtype) VALUES (%s, %s)'
                insvaltype = (foodid, foodtype)
                try:
                    cursor.execute(instype, insvaltype)
                    connection.commit()
                    print("Food type added successfully!")
                    return True
                except Exception as e:
                    print(f"Error in adding a new food type. {e}")
            elif choice == 5:
                seltypes = ("SELECT * FROM foodtype WHERE foodid=%s" % foodid)
                cursor.execute(seltypes)
                types = cursor.fetchall()
                if types:
                    print(foodname + "'s Available Food Types")
                    print('-----------------------------------------')
                    for j in types:
                        print("★ " + j[1])
                    oldtype = input("\nEnter the food type to be updated: ")
                    newtype = input("Enter new food type: ")
                    updtype = "UPDATE foodtype SET foodtype=%s WHERE foodid=%s AND foodtype LIKE %s"
                    updvaltype = (newtype, foodid, f"%{oldtype}%")
                    try:
                        cursor.execute(updtype, updvaltype)
                        connection.commit()
                        print("Food type updated successfully!")
                        return True
                    except Exception as e:
                        print(f"Error in updating the food type. {e}")
                else:
                    print("\nNo food type available")
            else:
                print("Invalid choice. Please try again.")     
    except:
        return False

def updateEstablishment(establishment):
    try:
        while True:
            for i in establishment:
                estid = i[0]
                name = i[1]
            print("Choose what you want to be updated")
            print("[1] Establishment Name")
            print("[2] Capacity")
            print("[3] Contact Number")
            print("[4] Add an address")
            print("[5] Edit an address")
            choice = int(input("Enter choice: "))
            if choice == 1:
                estname = input("Enter new establishment name: ")
                updname = 'UPDATE establishment SET estname=%s WHERE estid=%s'
                updvalname = (estname, estid)
                try:
                    cursor.execute(updname, updvalname)
                    connection.commit()
                    print("Establishment name updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error in updating estbalishment name. {e}")
            elif choice == 2:
                estcap = input("Enter new establishment capacity: ")
                updcap = 'UPDATE establishment SET capacity=%s WHERE estid=%s'
                updvalcap = (estcap, estid)
                try:
                    cursor.execute(updcap, updvalcap)
                    connection.commit()
                    print("Establishment's capacity updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error in updating estbalishment capacity. {e}")
            elif choice == 3:
                estcont = input("Enter new contact number: ")
                updcont = 'UPDATE establishment SET contactno=%s WHERE estid=%s'
                updvalcont = (estcont, estid)
                try:
                    cursor.execute(updcont, updvalcont)
                    connection.commit()
                    print("Contact number updated successfully!")
                    return True
                except Exception as e:
                    print(f"Error in updating contact number. {e}")
            elif choice == 4:
                estloc = input("Enter new location: ")
                insloc = 'INSERT INTO estaddress (estid, loc) VALUES (%s, %s)'
                insvalloc = (estid, estloc)
                try:
                    cursor.execute(insloc, insvalloc)
                    connection.commit()
                    print("Address added successfully!")
                    return True
                except Exception as e:
                    print(f"Error in adding a new address. {e}")
            elif choice == 5:
                sellocs = ("SELECT * FROM estaddress WHERE estid=%s" % estid)
                cursor.execute(sellocs)
                locs = cursor.fetchall()
                if locs:
                    print(name + "'s Available Locations")
                    print('-----------------------------------------')
                    for j in locs:
                        print("★ " + j[1])
                    oldloc = input("\nEnter the location to be updated: ")
                    newloc = input("Enter new location: ")
                    updloc = "UPDATE estaddress SET loc=%s WHERE estid=%s AND loc LIKE %s"
                    updvalloc = (newloc, estid, f"%{oldloc}%")
                    try:
                        cursor.execute(updloc, updvalloc)
                        connection.commit()
                        print("Address updated successfully!")
                        return True
                    except Exception as e:
                        print(f"Error in updating the address. {e}")
                else:
                    print("\nNo location available")
            else:
                print("Invalid choice. Please try again.")     
    except:
        return False

def viewHighRatingEst():
    try:
        select = "SELECT e.*, AVG(r.rate) as 'Average Rating' FROM establishment e JOIN reviewsest r ON e.estid = r.estid GROUP BY e.estid HAVING `Average rating` >= 4"
        cursor.execute(select)
        result = cursor.fetchall()
        print(f"\n{'Establishment Name':<30}{'Capacity':<20}{'Contact Number':<25}{'Average Rating':<15}")
        print('-------------------------------------------------------------------------------------------')
        for i in result:
            print(f"{i[1]:<30}{int(i[2]):<20}{int(i[3]):<25}{float(i[4]):<15.2f}")
        return True
    except:
        return False

def viewAllEstablishments(userInfo):
    try:  
        selectEst = 'SELECT * FROM establishment'
        cursor.execute(selectEst)
        result = cursor.fetchall()
        print("Available Establishments:")
        for i in result:
            print("★ " + i[1])
        while True:
            print("\n[1] Show establishment details")
            print("[2] Show establishmenths high ratings")
            print("[0] Back to main menu")
            choice = int(input("Enter choice: "))
            if choice == 1:
                break
            elif choice == 2:
                estrate = viewHighRatingEst()
                return estrate
            elif choice == 0:
                return
            else:
                print('\nInvalid choice. Please try again.')
        estname = input("Enter establishment to be shown: ")
        search = searchEstablishment(userInfo, estname)
        return search
    except:
        return False


def viewReviews(userInfo):
    try:
        while True:
            print("[1] Search reviews for an establishment only")
            print("[2] Search reviews for establishment and food item")
            print("[3] View all establishment reviews made within a month")
            print("[4] View all food reviews made within a month")
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
                    while True:
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
                        print("[1] Update own reviews")
                        print("[2] Delete own reviews")
                        print("[0] Back to Main Menu")
                        revchoice = int(input("Enter choice: "))
                        if revchoice == 1:
                            updrev = updateReviewsEst(userInfo, ests)
                            return updrev
                        elif revchoice == 2:
                            delrev = deleteReviewsEst(userInfo, ests)
                            return delrev
                        elif revchoice == 0:
                            return
                        else:
                            print("\nInvalid choice. Please try again.")
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
                        estid = i[0]  
                    for i in food:
                        foodid = i[0]
                    select = ("SELECT * FROM reviews WHERE estid LIKE '%%%s%%' AND foodid LIKE '%%%s%%'" % (estid, foodid))
                    cursor.execute(select)
                    rev = cursor.fetchall()
                    while True:
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
                        print("[1] Update own reviews")
                        print("[2] Delete own reviews")
                        print("[0] Back to Main Menu")
                        revchoice = int(input("Enter choice: "))
                        if revchoice == 1:
                            updrev = updateReviewsEstFood(userInfo, ests, food)
                            return updrev
                        elif revchoice == 2:
                            delrev = deleteReviewsEstFood(userInfo, ests, food)
                            return delrev
                        elif revchoice == 0:
                            return
                        else:
                            print("\nInvalid choice. Please try again.")
                else:
                    print("\n" + estname + " and " + foodname + " does not exist.")
                    return
            elif choice == 3:
                sortrev = sortReviewEst()
                return sortrev
            elif choice == 4:
                sortrevfood = sortReviewEstFood()
                return sortrevfood
            else:
                print("\nInvalid Choice. Please try again. \n")
    except:
        return False
    
def sortReviewEstFood():
    try:
        selId = "SELECT * FROM establishment"
        cursor.execute(selId)
        ests = cursor.fetchall()          
        selFoodId = "SELECT * FROM fooditem"
        cursor.execute(selFoodId)
        food = cursor.fetchall()
        month = input("Enter month: ")
        sort = ("SELECT * FROM reviews WHERE MONTHNAME(reviewdate) LIKE '%%%s%%'" % month)
        cursor.execute(sort)
        rev = cursor.fetchall()
        if rev: 
            print(f"{'Customer Name':<30}{'Establishment Name':<30}{'Food Name':<20}{'Rating':<10}{'Date':<20}{'Time':<20}{'Feedback':<50}")
            print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            for k in rev:
                selCus = ("SELECT full_name FROM customer WHERE email LIKE '%%%s%%'" % k[0])
                cursor.execute(selCus)
                custs = cursor.fetchall()
                for i in ests:
                    for j in food:
                        if k[2] == j[0] and i[0] == k[1]:
                            foodname = j[1]
                            estname = i[1]
                for m in custs:
                    time_secs = int(k[5].total_seconds())
                    hours = time_secs // 3600
                    mins = (time_secs % 3600) // 60
                    secs = time_secs % 60
                    print(f"{m[0]:<30}{estname:<30}{foodname:<20}{k[3]:<10}{(k[4].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{k[6]:<50}")
            return True
        else:
            print("\nNo reviews made within that month.")
    except:
        return False

def sortReviewEst():
    try:
        selId = "SELECT * FROM establishment"
        cursor.execute(selId)
        ests = cursor.fetchall()          
        month = input("Enter month: ")
        sort = ("SELECT * FROM reviewsest WHERE MONTHNAME(reviewdate) LIKE '%%%s%%'" % month)
        cursor.execute(sort)
        rev = cursor.fetchall()
        print(f"{'Customer Name':<30}{'Establishment Name':<30}{'Rating':<10}{'Date':<20}{'Time':<20}{'Feedback':<50}")
        print('----------------------------------------------------------------------------------------------------------------------------------------------------')
        if rev:
            for k in rev:
                selCus = ("SELECT full_name FROM customer WHERE email LIKE '%%%s%%'" % k[0])
                cursor.execute(selCus)
                custs = cursor.fetchall()
                for i in ests:
                    if i[0] == k[1]:
                        estname = i[1]
                for m in custs:
                    time_secs = int(k[4].total_seconds())
                    hours = time_secs // 3600
                    mins = (time_secs % 3600) // 60
                    secs = time_secs % 60
                    print(f"{m[0]:<30}{estname:<30}{k[2]:<10}{(k[3].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{k[5]:<50}")
            return True
        else:
            print("\nNo reviews made within that month.")
    except:
        return False
    
def updateReviewsEstFood(userInfo, est, food):
    try:
        for i in est:
            estid = i[0]
            estname = i[1]
        for i in food:
            foodid = i[0]
            foodname = i[1]
        select = ("SELECT * FROM reviews WHERE estid=%s AND email LIKE '%%%s%%' AND foodid=%s" % (estid, userInfo, foodid))
        cursor.execute(select)
        rev = cursor.fetchall()
        print(f"{'Customer Name':<30}{'Establishment Name':<30}{'Food Name':<20}{'Rating':<10}{'Date':<20}{'Time':<20}{'Feedback':<50}")
        print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        for i in rev:
            selCus = ("SELECT full_name FROM customer WHERE email LIKE '%%%s%%'" % i[0])
            cursor.execute(selCus)
            custs = cursor.fetchall()
            for j in custs:
                time_secs = int(i[5].total_seconds())
                hours = time_secs // 3600
                mins = (time_secs % 3600) // 60
                secs = time_secs % 60
                print(f"\n{j[0]:<30}{estname:<30}{foodname:<20}{i[3]:<10}{(i[4].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{i[6]:<50}")
                while True:
                    revchoice = input("\nDo you want to edit this review? (Y|N): ")
                    if revchoice == 'Y':
                        rate = int(input("Enter rating (1-5): "))
                        feedback = input("Enter feedback: ")
                        updrate = "UPDATE reviews SET rate=%s, reviewdate=CURDATE(), reviewtime=CURTIME(), feedback=%s WHERE email LIKE %s AND estid=%s AND foodid=%s AND feedback LIKE %s"
                        ratevals = (rate, feedback, f"%{userInfo}%", estid, foodid, f"%{i[6]}%")
                        try:
                            cursor.execute(updrate, ratevals)
                            connection.commit()
                            print("Review updated successfully.")
                            return True
                        except Exception as e:
                            print(f"Error in editing review. {e}")
                    elif revchoice == 'N':
                        break
                    else:
                        print("\nInvalid choice. Please try again.")    
    except:
        return False

def deleteReviewsEstFood(userInfo, est, food):
    try:
        for i in est:
            estid = i[0]
            estname = i[1]
        for i in food:
            foodid = i[0]
            foodname = i[1]
        select = ("SELECT * FROM reviews WHERE estid=%s AND email LIKE '%%%s%%' AND foodid=%s" % (estid, userInfo, foodid))
        cursor.execute(select)
        rev = cursor.fetchall()
        print(f"{'Customer Name':<30}{'Establishment Name':<30}{'Food Name':<20}{'Rating':<10}{'Date':<20}{'Time':<20}{'Feedback':<50}")
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
                print(f"\n{j[0]:<30}{estname:<30}{foodname:<20}{i[3]:<10}{(i[4].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{i[6]:<50}")
                while True:
                    revchoice = input("\nDo you want to delete this review? (Y|N): ")
                    if revchoice == 'Y':
                        delrate = "DELETE FROM reviews WHERE email LIKE %s AND estid=%s AND foodid=%s AND feedback LIKE %s"
                        ratevals = (f"%{userInfo}%", estid, foodid, f"%{i[6]}%")
                        try:
                            cursor.execute(delrate, ratevals)
                            connection.commit()
                            print("Review deleted successfully.")
                            return True
                        except Exception as e:
                            print(f"Error in deleting review. {e}")
                    elif revchoice == 'N':
                        break
                    else:
                        print("\nInvalid choice. Please try again.")    
    except:
        return False

        
def updateReviewsEst(userInfo, est):
    try:
        for i in est:
            estid = i[0]
            estname = i[1]
        select = ("SELECT * FROM reviewsest WHERE estid LIKE '%%%s%%' AND email LIKE '%%%s%%'" % (estid, userInfo))
        cursor.execute(select)
        rev = cursor.fetchall()
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
                print(f"\n{j[0]:<30}{estname:<30}{i[2]:<10}{(i[3].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{i[5]:<50}")
                while True:
                    revchoice = input("\nDo you want to edit this review? (Y|N): ")
                    if revchoice == 'Y':
                        rate = int(input("Enter rating (1-5): "))
                        feedback = input("Enter feedback: ")
                        updrate = "UPDATE reviewsest SET rate=%s, reviewdate=CURDATE(), reviewtime=CURTIME(), feedback=%s WHERE email LIKE %s AND estid=%s AND feedback LIKE %s"
                        ratevals = (rate, feedback, f"%{userInfo}%", estid,f"%{i[5]}%")
                        try:
                            cursor.execute(updrate, ratevals)
                            connection.commit()
                            print("Review updated successfully.")
                            return True
                        except Exception as e:
                            print(f"Error in editing review. {e}")
                    elif revchoice == 'N':
                        break
                    else:
                        print("\nInvalid choice. Please try again.")    
    except:
        return False
    

def deleteReviewsEst(userInfo, est):
    try:
        for i in est:
            estid = i[0]
            estname = i[1]
        select = ("SELECT * FROM reviewsest WHERE estid LIKE '%%%s%%' AND email LIKE '%%%s%%'" % (estid, userInfo))
        cursor.execute(select)
        rev = cursor.fetchall()
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
                print(f"\n{j[0]:<30}{estname:<30}{i[2]:<10}{(i[3].strftime("%Y-%m-%d")):<20}{hours:02}:{mins:02}:{secs:02}{"":10}{i[5]:<50}")
                while True:
                    revchoice = input("\nDo you want to delete this review? (Y|N): ")
                    if revchoice == 'Y':
                        delrate = "DELETE FROM reviewsest WHERE email LIKE %s AND estid=%s AND feedback LIKE %s"
                        ratevals = (f"%{userInfo}%", estid, f"%{i[5]}%")
                        try:
                            cursor.execute(delrate, ratevals)
                            connection.commit()
                            print("Review deleted successfully.")
                            return True
                        except Exception as e:
                            print(f"Error in deleting review. {e}")
                    elif revchoice == 'N':
                        break
                    else:
                        print("\nInvalid choice. Please try again.")    
    except:
        return False

def searchFoodItems():
    try:
        while True:
            print('[1] Search food items by price')
            print('[2] Search food items by food type')
            print('[3] Search food items by both price and food type')
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
                    return True
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
                return True
            elif choice == 3:
                foodprice = input("Enter price range (separate by comma): ")
                price = foodprice.split(',')
                foodtype = input("Enter food type: ")
                selFood = ("SELECT * FROM fooditem NATURAL JOIN foodtype WHERE foodtype LIKE '%%%s%%' AND foodprice BETWEEN %s AND %s ORDER BY foodprice ASC" % (foodtype, float(price[0]), float(price[1])))
                cursor.execute(selFood)
                priceAndFtype = cursor.fetchall()
                if priceAndFtype:
                    print(f"{'Food Name':<30}{'Food Description':<60}{'Price':<15}{'Food Type':<20}{'Establishment Name':<20}")
                    print('----------------------------------------------------------------------------------------------------------------------------------------------------')
                    for j in priceAndFtype:
                        selEstName = ("SELECT estname FROM establishment WHERE estid LIKE %s" % j[4])
                        cursor.execute(selEstName)
                        ests = cursor.fetchall()
                        for k in ests:
                            print(f"{j[1]:<30}{j[2]:<60}{float(j[3]):<15.2f}{j[5]:<20}{k[0]:<20}")
                    return True
                else:
                    print("\nThere are no available products from the price and type indicated.")
            else:
                print("\nInvalid Choice. Please try again.\n")
    except:
        return False

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
                viewAllEstablishments(userCredentials)
            elif choice == 3:
                viewReviews(userCredentials)
            elif choice == 4:
                searchFoodItems()
            # elif choice == 7:
            #     viewAllEstablishments(userCredentials)
            elif choice == 0:
                break
            else:
                print('\nInvalid Choice')
    elif register:
        print('\nYour account has been registered.\n')
        continue
    else: 
        print('\nInvalid email or password')
        continue