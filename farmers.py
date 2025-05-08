import mysql.connector
import requests
import json
from PIL import Image
import bcrypt
import os
import re
db = mysql.connector.connect(
   host= "localhost",
   user = "root",
   password = "Omosh2021@",
   database = "Farmers_management_system"
)
print("Connected Successfuly!")
raw_password = "Omosh2021@"
hashed_pasword= bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
def sign_up():
    up = {
        "user_name": input("Enter your username: ").strip(),
        "email": input("Enter your email: ").strip().lower(),
        "password": input("Enter your password: ").strip(),
        "role": input("Enter your role (farmer/supplier/vet): ").strip().lower()
    }

    raw_password = up['password']

    if len(raw_password) < 8:
        print("Password MUST have at least 8 characters.")
        return
    if not re.search(r"[A-Z]", raw_password):
        print("Password MUST have an uppercase letter.")
        return
    if not re.search(r"[0-9]", raw_password):
        print("Password MUST have a digit.")
        return
    if not re.search(r"[a-z]", raw_password):
        print("Password MUST have a lowercase letter.")
        return
    if not re.search(r"[!&()%@$#]", raw_password):
        print("Password MUST have a special symbol.")
        return

    hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
    up['password'] = hashed_password.decode('utf-8')  # Store as string

    print("Sign-up Successful!")
    return up

def insert_sign_up(up):
    cursor = db.cursor()
    sql = "INSERT INTO Login(user_name, email, password, role) VALUES(%s, %s, %s, %s)"
    values = (up['user_name'], up['email'], up['password'], up['role'])
    cursor.execute(sql, values)
    db.commit()
    print("User registered and saved to database.")

def sign_in():
    login = {
        "email": input("Enter your email: ").strip().lower(),
        "password": input("Enter your password: ").strip()
    }

    cursor = db.cursor()
    sql = "SELECT password FROM Login WHERE email=%s"
    cursor.execute(sql, (login['email'],))
    result = cursor.fetchone()

    if result:
        stored_hash = result[0].encode('utf-8')
        if bcrypt.checkpw(login['password'].encode('utf-8'), stored_hash):
            print("Login Successful")
        else:
            print("Incorrect password")
    else:
        print("User not found")

  
def get_farmer():
    farmer = {"first_name":input("Enter first_name ").strip().title(),
    "last_name":input("Enter last_name ").strip().title(),
    "email": input("Enter email ").strip().lower(),
    "phone":int(input("Enter your phone number ")),
    "location":input("Enter your location ").strip()}
    return farmer

def insert_farmer(farmer):
    cursor = db.cursor()
    sql = "INSERT INTO farmer(first_name, last_name, email, phone, location)VALUES (%s, %s, %s, %s, %s)"
    values = (farmer['first_name'],
        farmer['last_name'],
        farmer['email'],
        farmer['phone'],
        farmer['location'])
    cursor.execute(sql,values)
    db.commit()
    print("Farmer added successfully!")
#def get_supplier():
    #supplier = {"supplier_name": input("Enter your first and last name ").strip().title(),
    #"phone_number": input("Enter your phone number ").strip(),
    #"email": input("Enter your email ").strip().lower(),
    #"location": input("Enter your location").strip()}
    #return supplier
#def insert_supplier(supplier):
    #cursor = db.cursor()
    #sql = "INSERT INTO supplier (supplier_name, phone_number, email, location) VALUES(%s, %s, %s, %s)"
    #values= (supplier['supplier_name'], supplier['phone_number'], supplier['email'], supplier['location'])
    #cursor.execute(sql, values)
    #db.commit()
    #print("Supplier added successfully!")
def get_products():
    product = {"product_name": input("Enter the product name ").strip().lower(),
    "category": input("Enter the product category ").strip().lower(),
    "price": float(input("Enter the price ").strip()),
    "stock_quantity": int(input("Enter the quantity in stock ").strip()),
    "descriptions": input("Enter product description ").strip().lower(),
    "image_url": input("Enter the image url ").strip().lower()}
    return product
def insert_product(product):
    cursor = db.cursor()
    sql = "INSERT INTO products(product_name, category, price, stock_quantity, descriptions, image_url) VALUES(%s, %s, %s, %s, %s, %s)"
    values = (product['product_name'], 
    product['category'], 
    product['price'], 
    product['stock_quantity'], 
    product['descriptions'], 
    product['image_url'])
    cursor.execute(sql, values)
    db.commit()
    print("Product added successfully!")
def get_orders():
    order = {"quantity": int(input("Enter the quantity ").strip()),
    "total_price": float(input("Enter the total price ").strip()),
    "order_status": input("Enter the status of the order ").strip().lower(),
    "delivery_date": input("Enter the date of delivery "),# I understand we need to import datetime, but I can't be bothered right now
    "payment_status": input("Enter payment status ").strip().lower()
    }
    return order
def insert_orders(order):
    cursor = db.cursor()
    sql = "INSERT INTO orders(quantity, total_price, order_status, delivery_date, payment_status) VALUES (%s, %s, %s, %s, %s)"
    values = (order['quantity'],
    order['total_price'],
    order['order_status'],
    order['delivery_date'],
    order['payment_status'])
    cursor.execute(sql, values)
    db.commit()
    print("Order added successfully!")
def get_reports():
    report = {"descriptions": input("Write a short report ").strip().title(),
    "image_url": input("Enter the image url ").strip().lower()}
    return report
def insert_report(report):
    cursor = db.cursor()
    sql = "INSERT INTO reports (descriptions, image_url) VALUES (%s, %s)"
    values = (report['descriptions'], report['image_url'])
    cursor.execute(sql, values)
    db.commit()
    print("Report added successfully!")
def get_vet():
    vet = {"full_name": input("Enter your name ").strip().title(),
    "speciality": input("Enter your speciality ").strip().lower(),
    "phone_number": input("Enter your phone number ").strip(),
    "email":input("Enter your email ").strip().lower(),
    "location": input("Enter your current location ").strip().title()}
    return vet
def insert_vet(vet):
    cursor= db.cursor()
    sql = "INSERT INTO vet (full_name, speciality, phone_number, email, location) VALUES (%s, %s, %s, %s, %s)"
    values = (vet['full_name'],
    vet['speciality'],
    vet['phone_number'],
    vet['email'],
    vet['location'])
    cursor.execute(sql, values)
    db.commit()
    print("Vetinary added successfully!")
def get_consultation():
    consultation = {"farmer_id": int(input("Enter farmer's id ")).strip(),
    "vet_id": int(input("Enter vet's id ")).strip(),
    "report_id":int(input("Enter report_id ")).strip(),
    "issue": input("Please describe your issue ").strip(),
    "notes": input("Write some notes ").strip(),
    "recommendation": input("What do you recommend? ").strip(),
    "consultation_date":input("Enter the date of consultation ")}#datetime, I know
    return consultation
def insert_consultation(consultation):
    cursor = db.cursor()
    sql = "INSERT INTO consultation (farmer_id, vet_id, report_id, issue, notes, recommendation, consultation_date) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    values = (consultation['farmer_id'],
    consultation['vet_id'],
    consultation['report_id'],
    consultation['issue'],
    consultation['notes'],
    consultation['recommendation'],
    consultation['consultation_date'])
    cursor.execute(sql, values)
    db.commit()
    print("Successfull Consultation")
def get_ai():
    ai= {"farmer_id":int(input("Enter farmer's id ")).strip(),
    "report_id": int(input("Enter report's id ")).strip(),
    "confidence_score": float(input("Enter the confidence score ")).strip(),
    "diagnosis": input("Enter your diagnosis ").strip().title(),
    "recommended_product": input("Which medication do you recommend? ").strip()}
    return ai
def insert_ai(ai):
    cursor = db.cursor()
    sql = "INSERT INTO ai (farmer_id, report_id, confidence_score, diagnosis, recommended_product) VALUES(%s, %s, %s, %s, %s) "
    values = (ai['farmer_id'],
    ai['report_id'],
    ai['confidence_score'],
    ai['diagnosis'],
    ai['recommended_product'])
    cursor.execute(sql, values)
    db.commit()
    print("Ai diagnosis successful!")
def menu():
    while True:
        print("=== MAIN MENU ===")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Add Farmer")
        print("4. Add Product")
        print("5. Add Order")
        print("6. Add Report")
        print("7. Add Vet")
        print("8. Add Consultation")
        print("9. Add AI Diagnosis")
        print("10. Exit")
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == "1":
            user = sign_up()
            if user: insert_sign_up(user)
        elif choice == "2":
            sign_in()
        elif choice == "3":
            insert_farmer(get_farmer())
        elif choice == "4":
            insert_product(get_products())
        elif choice == "5":
            insert_orders(get_orders())
        elif choice == "6":
            insert_report(get_reports())
        elif choice == "7":
            insert_vet(get_vet())
        elif choice == "8":
            insert_consultation(get_consultation())
        elif choice == "9":
            insert_ai(get_ai())
        elif choice == "10":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("=== SCRIPT STARTED ===")
    main()  
    print("=== END OF FILE ===")


