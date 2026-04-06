# Best Buy Retail Store - Point of Sale (POS) System
# Authors: Javane Martin, Moya Codner (Clean Data Crew)
# Course: ITT103

#CONSTANTS
#Fixed values used for tax, discount rules, and low-stock alerts.
TAX_RATE = 0.10
DISCOUNT_THRESHOLD = 5000.00
DISCOUNT_RATE = 0.05
LOW_STOCK_LIMIT = 5

#PRODUCT CATALOG
#A list of dictionaries — each holds a product's name, price, and available stock.
product_list = [
    {"name": "Rice",        "price": 450.00, "stock": 50},
    {"name": "Flour",       "price": 320.00, "stock": 40},
    {"name": "Sugar",       "price": 380.00, "stock": 35},
    {"name": "Cooking Oil", "price": 650.00, "stock": 25},
    {"name": "Milk",        "price": 290.00, "stock": 30},
    {"name": "Bread",       "price": 350.00, "stock": 20},
    {"name": "Eggs",        "price": 500.00, "stock": 15},
    {"name": "Butter",      "price": 420.00, "stock": 18},
    {"name": "Juice",       "price": 250.00, "stock": 60},
    {"name": "Water",       "price": 100.00, "stock": 100},
    {"name": "Chicken",     "price": 890.00, "stock": 12},
    {"name": "Soap",        "price": 175.00, "stock": 45},
]

#SHOPPING CART
#Starts empty. Items are added as dictionaries with name, price, and qty.
shopping_cart = []


#DISPLAY MENU
#Prints the main menu options so the cashier can choose an action.
def display_menu():
    print("=" * 45)
    print("     BEST BUY RETAIL STORE - POS MENU")
    print("=" * 45)
    print("  1. View Products")
    print("  2. Add Item to Cart")
    print("  3. Remove Item from Cart")
    print("  4. View Cart")
    print("  5. Checkout")
    print("  6. Exit")
    print("=" * 45)


#VIEW PRODUCTS
#Lists all products with their number, price, and stock. Flags items below the low-stock limit.
def view_products():
    print("=" * 55)
    print(f"  {'#':<4} {'Product':<15} {'Price':>10} {'Stock':>8}")
    print("-" * 55)
    for i, product in enumerate(product_list, start=1):
        # Attach a warning label if stock is critically low
        stock_note = " *** LOW STOCK ***" if product["stock"] < LOW_STOCK_LIMIT else ""
        print(f"  {i:<4} {product['name']:<15} ${product['price']:>9.2f} {product['stock']:>8}{stock_note}")
    print("=" * 55)


#ADD ITEM TO CART
#Asks for a product name and quantity, checks available stock, then adds
#the item to the cart (or updates its quantity if it's already there).
def add_item():
    name = input("Enter product name: ").strip()

    # Keep asking until a valid positive integer is entered
    while True:
        try:
            qty = int(input("Enter quantity: "))
            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Search for the product by name (case-insensitive)
    for product in product_list:
        if product["name"].lower() == name.lower():
            if qty <= product["stock"]:
                # If the item is already in the cart, just increase its quantity
                for cart_item in shopping_cart:
                    if cart_item["name"].lower() == product["name"].lower():
                        cart_item["qty"] += qty
                        product["stock"] -= qty
                        print(f"Updated cart: {cart_item['qty']} x {product['name']}")
                        if product["stock"] < LOW_STOCK_LIMIT:
                            print(f"  *** LOW STOCK ALERT: Only {product['stock']} units of {product['name']} remaining! ***")
                        return
                # Otherwise, add it as a new cart entry
                shopping_cart.append({"name": product["name"], "price": product["price"], "qty": qty})
                product["stock"] -= qty
                print(f"Added to cart: {qty} x {product['name']}")
                if product["stock"] < LOW_STOCK_LIMIT:
                    print(f"  *** LOW STOCK ALERT: Only {product['stock']} units of {product['name']} remaining! ***")
            else:
                print(f"Insufficient stock. Only {product['stock']} units available.")
            return

    print("Product not found. Please check the name and try again.")


#REMOVE ITEM FROM CART
#Reduces or removes an item from the cart and returns that quantity back to stock.
def remove_item():
    if not shopping_cart:
        print("Cart is empty.")
        return

    name = input("Enter item name to remove: ").strip()

    # Keep asking until a valid positive integer is entered
    while True:
        try:
            qty = int(input("Enter quantity to remove: "))
            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    for cart_item in shopping_cart:
        if cart_item["name"].lower() == name.lower():
            if qty <= cart_item["qty"]:
                cart_item["qty"] -= qty
                # Give the stock back to the product catalog
                for product in product_list:
                    if product["name"].lower() == name.lower():
                        product["stock"] += qty
                        break
                # Remove the entry entirely if quantity reaches zero
                if cart_item["qty"] == 0:
                    shopping_cart.remove(cart_item)
                    print(f"Removed {name} from cart.")
                else:
                    print(f"Removed {qty} x {name}. Remaining in cart: {cart_item['qty']}")
            else:
                print(f"Cannot remove {qty} — only {cart_item['qty']} in cart.")
            return

    print("Item not found in cart.")


#VIEW CART
#Displays every item in the cart with its quantity, unit price, line total, and the overall cart total.
def view_cart():
    if not shopping_cart:
        print("Cart is empty.")
        return

    print("-" * 55)
    print(f"  {'Item':<15} {'Qty':>5} {'Unit Price':>12} {'Total':>10}")
    print("-" * 55)

    cart_total = 0
    for item in shopping_cart:
        item_total = item["qty"] * item["price"]
        cart_total += item_total
        print(f"  {item['name']:<15} {item['qty']:>5} ${item['price']:>11.2f} ${item_total:>9.2f}")

    print("-" * 55)
    print(f"  {'Cart Total:':<33} ${cart_total:>9.2f}")
    print("-" * 55)


#GENERATE RECEIPT
#Prints a formatted receipt with all items, subtotal, discount (if any),
#tax, total, amount paid, and change due.
def generate_receipt(cart_snapshot, subtotal, discount, tax, total, payment, change):
    print("=" * 45)
    print("         BEST BUY RETAIL STORE")
    print("       Your Everyday Essentials Shop")
    print("=" * 45)
    print("                 RECEIPT")
    print("-" * 45)
    print(f"{'Item':<15} {'Qty':>5} {'Unit Price':>12} {'Total':>10}")
    print("-" * 45)
    for item in cart_snapshot:
        item_total = item["qty"] * item["price"]
        print(f"{item['name']:<15} {item['qty']:>5} ${item['price']:>11.2f} ${item_total:>9.2f}")
    print("-" * 45)
    print(f"{'Subtotal:':<35} ${subtotal:>7.2f}")
    if discount > 0:
        print(f"{'Discount (5%):':<35} -${discount:>6.2f}")
    print(f"{'Tax (10%):':<35} ${tax:>7.2f}")
    print(f"{'TOTAL DUE:':<35} ${total:>7.2f}")
    print("-" * 45)
    print(f"{'Amount Paid:':<35} ${payment:>7.2f}")
    print(f"{'Change:':<35} ${change:>7.2f}")
    print("=" * 45)
    print("    Thank you for shopping with us!")
    print("        Please come again soon!")
    print("=" * 45)


#CHECKOUT
#Calculates the subtotal, applies a 5% discount if the subtotal hits $5,000+,
#adds 10% tax, collects payment, prints the receipt, then clears the cart.
def checkout():
    if not shopping_cart:
        print("Cart is empty. Nothing to checkout.")
        return


    subtotal = sum(item["qty"] * item["price"] for item in shopping_cart)


    discount = subtotal * DISCOUNT_RATE if subtotal >= DISCOUNT_THRESHOLD else 0


    taxable_amount = subtotal - discount
    tax = taxable_amount * TAX_RATE
    total = taxable_amount + tax


    print("-" * 45)
    print(f"{'Subtotal:':<35} ${subtotal:>7.2f}")
    if discount > 0:
        print(f"{'Discount (5%):':<35} -${discount:>6.2f}")
    print(f"{'Tax (10%):':<35} ${tax:>7.2f}")
    print(f"{'TOTAL DUE:':<35} ${total:>7.2f}")
    print("-" * 45)


    while True:
        try:
            payment = float(input("Enter payment amount: $"))
            if payment < total:
                print(f"Insufficient payment. Total due is ${total:.2f}. Please try again.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a numeric amount.")

    change = payment - total

    cart_snapshot = [item.copy() for item in shopping_cart]

    generate_receipt(cart_snapshot, subtotal, discount, tax, total, payment, change)


    shopping_cart.clear()
    print("Cart cleared. Ready for next transaction.")


#MAIN LOOP
#Continuously shows the menu and routes the cashier's input to the correct function.
#The loop only exits when the cashier chooses option 6.
while True:
    display_menu()
    choice = input("Enter your choice (1-6): ").strip()

    if choice == "1":
        view_products()
    elif choice == "2":
        add_item()
    elif choice == "3":
        remove_item()
    elif choice == "4":
        view_cart()
    elif choice == "5":
        checkout()
    elif choice == "6":
        print("Thank you for using Best Buy POS. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
