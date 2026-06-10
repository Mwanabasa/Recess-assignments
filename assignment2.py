# Predefined users and passwords
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "customer": {"password": "cust123", "role": "Customer"},
    "cashier": {"password": "cash123", "role": "Cashier"}
}

print("=== LOGIN SYSTEM ===")
username = input("Enter username: ")
password = input("Enter password: ")

if username in users:
    if password == users[username]["password"]:
        role = users[username]["role"]
        print(f"Login successful! Welcome, {role}")
    else:
        print("Incorrect password")
        exit()
else:
    print("Username not found")
    exit()

# E-COMMERCE PRICE CALCULATION
print("\n E-COMMERCE PRICE CALCULATOR ")

subtotal = float(input("Enter subtotal amount: "))
coupon = input("Enter coupon code (SAVE10, SAVE20, NONE): ").upper()
location = input("Enter location (UG, KE, TZ): ").upper()


# DISCOUNT BASED ON SUBTOTAL
if subtotal >= 500:
    discount_rate = 0.20
elif subtotal >= 200:
    discount_rate = 0.10
elif subtotal >= 100:
    discount_rate = 0.05
else:
    discount_rate = 0.00


# COUPON CODE HANDLING
if coupon == "SAVE10":
    coupon_discount = 0.10
elif coupon == "SAVE20":
    coupon_discount = 0.20
elif coupon == "NONE":
    coupon_discount = 0.00
else:
    print("Invalid coupon code! No coupon applied.")
    coupon_discount = 0.00


# TAX RATE BASED ON LOCATION
if location == "UG":
    tax_rate = 0.18
elif location == "KE":
    tax_rate = 0.16
elif location == "TZ":
    tax_rate = 0.15
else:
    print("Unknown location! Default tax = 0%")
    tax_rate = 0.00


# FINAL PRICE CALCULATION
discount_amount = subtotal * discount_rate
coupon_amount = subtotal * coupon_discount
tax_amount = subtotal * tax_rate

final_price = subtotal - discount_amount - coupon_amount + tax_amount

# OUTPUT
print("\n--- RECEIPT ---")
print(f"Subtotal: {subtotal}")
print(f"Discount ({discount_rate*100}%): -{discount_amount}")
print(f"Coupon ({coupon_discount*100}%): -{coupon_amount}")
print(f"Tax ({tax_rate*100}%): +{tax_amount}")
print(f"Final Price: {final_price}")
