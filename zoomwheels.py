import mysql.connector
import random

# Function to establish database connection
def connect_to_database():
    db = mysql.connector.connect(
        host="localhost",
        user="abrar",
        password="1234",
        database="zoomwheels"
    )
    return db

# Function for user login
def user_login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM customer WHERE name = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

# Function for admin login
def admin_login():
    admin_name = input("Enter admin name: ")
    password = input("Enter password: ")
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM admin WHERE name = %s AND password = %s"
    cursor.execute(query, (admin_name, password))
    admin = cursor.fetchone()
    cursor.close()
    db.close()
    return admin

# Function to register a new user
def register_user():
    # Generate random CID
    CID = random.randint(1000, 9999)
    name = input("Enter name: ")
    phone = input("Enter phone (11 digits): ")
    address = input("Enter address: ")
    NID = input("Enter NID: ")
    licence = input("Enter licence: ")
    password = input("Enter password: ")
    db = connect_to_database()
    cursor = db.cursor()
    query = "INSERT INTO customer (CID, name, phone, address, NID, licence, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (CID, name, phone, address, NID, licence, password))
    db.commit()
    cursor.close()
    db.close()

# Function to add a new vehicle
def add_new_vehicle():
    # Generate random VID
    VID = random.randint(1000, 9999)
    plate = input("Enter plate: ")
    vehicle_type = input("Enter vehicle type: ")
    model = input("Enter model: ")
    brand = input("Enter brand: ")
    price = float(input("Enter price: "))
    db = connect_to_database()
    cursor = db.cursor()
    query = "INSERT INTO vehicle (VID, plate, vehicle_type, model, brand, price) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (VID, plate, vehicle_type, model, brand, price))
    db.commit()
    cursor.close()
    db.close()

# Function to delete a user
def delete_user():
    CID = input("Enter CID of the user to delete: ")
    db = connect_to_database()
    cursor = db.cursor()
    query = "DELETE FROM customer WHERE CID = %s"
    cursor.execute(query, (CID,))
    db.commit()
    cursor.close()
    db.close()

# Function to display available cars
def display_available_cars():
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT * FROM vehicle"
    cursor.execute(query)
    vehicles = cursor.fetchall()
    for vehicle in vehicles:
        print("VID:", vehicle[0])
        print("Plate:", vehicle[1])
        print("Type:", vehicle[2])
        print("Model:", vehicle[3])
        print("Brand:", vehicle[4])
        print("Price:", vehicle[5])
        print("---------------------------")
    cursor.close()
    db.close()

# Function to save reservation to record table
def save_reservation_to_record(RID, CID, VID, bill):
    db = connect_to_database()
    cursor = db.cursor()
    query = "INSERT INTO record (RID, CID, VID, bill) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (RID, CID, VID, bill))
    db.commit()
    cursor.close()
    db.close()

# Function to calculate bill
def calculate_bill(total_amount):
    return total_amount

# Function to make a reservation
def make_reservation(user):
    VID = input("Enter VID of the vehicle to reserve: ")
    _date = input("Enter date: ")
    destination = input("Enter destination: ")
    total_amount = get_vehicle_price(VID)
    print("Reservation Details:")
    print("Vehicle: ", get_vehicle_details(VID))
    print("Destination: ", destination)
    print("Customer ID (CID): ", user[0])
    print("Total Amount: ", total_amount)
    proceed = input("Do you want to proceed with the reservation? (yes/no): ")
    if proceed.lower() == "yes":
        print("Reservation successful!")
        RID = random.randint(1000, 9999)
        save_to_reservation(RID, _date, destination)
        save_reservation_to_record(RID, user[0], VID, total_amount)  # Use total_amount as bill
    else:
        print("Reservation cancelled.")

# Function to save reservation to reservation table
def save_to_reservation(RID, _date, destination):
    db = connect_to_database()
    cursor = db.cursor()
    query = "INSERT INTO reservation (RID, _date, destination) VALUES (%s, %s, %s)"
    cursor.execute(query, (RID, _date, destination))
    db.commit()
    cursor.close()
    db.close()

# Function to view reservation history
def view_reservation_history(user):
    db = connect_to_database()
    cursor = db.cursor()
    query = """SELECT r.RID, r._date, r.destination, v.plate, v.model, rc.bill
               FROM reservation r
               JOIN record rc ON r.RID = rc.RID
               JOIN vehicle v ON rc.VID = v.VID
               WHERE rc.CID = %s"""
    cursor.execute(query, (user[0],))
    reservations = cursor.fetchall()
    if reservations:
        print("\nReservation History:")
        for reservation in reservations:
            print("Reservation ID:", reservation[0])
            print("Date:", reservation[1])
            print("Destination:", reservation[2])
            print("Plate:", reservation[3])
            print("Model:", reservation[4])
            print("Total Bill:", reservation[5])
            print("---------------------------")
    else:
        print("No reservation history found for this user.")
    cursor.close()
    db.close()

# Function to get vehicle price
def get_vehicle_price(VID):
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT price FROM vehicle WHERE VID = %s"
    cursor.execute(query, (VID,))
    price = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return price

# Function to get vehicle details
def get_vehicle_details(VID):
    db = connect_to_database()
    cursor = db.cursor()
    query = "SELECT model, plate FROM vehicle WHERE VID = %s"
    cursor.execute(query, (VID,))
    details = cursor.fetchone()
    cursor.close()
    db.close()
    return details

# Main function
def main():
    while True:
        print("\nWelcome to ZoomWheels Rent-a-Car System")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            user = user_login()
            if user:
                while True:
                    print("\nUser Menu:")
                    print("1. Display Available Cars")
                    print("2. Make Reservation")
                    print("3. View Reservation History")
                    print("4. Logout")
                    option = input("Enter your option: ")
                    if option == "1":
                        display_available_cars()
                    elif option == "2":
                        make_reservation(user)
                    elif option == "3":
                        view_reservation_history(user)
                    elif option == "4":
                        break
                    else:
                        print("Invalid option!")
            else:
                print("Invalid username or password.")

        elif choice == "2":
            admin = admin_login()
            if admin:
                while True:
                    print("\nAdmin Menu:")
                    print("1. Register New User")
                    print("2. Add New Vehicle")
                    print("3. Delete User")
                    print("4. Logout")
                    option = input("Enter your option: ")
                    if option == "1":
                        register_user()
                    elif option == "2":
                        add_new_vehicle()
                    elif option == "3":
                        delete_user()
                    elif option == "4":
                        break
                    else:
                        print("Invalid option!")
            else:
                print("Invalid admin name or password.")

        elif choice == "3":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()