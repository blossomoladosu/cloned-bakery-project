import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config(
    page_title="Blossom and Nandika's Bakery Delights", 
    layout="centered",
    initial_sidebar_state="expanded"
)
st.title("Blossom and Nandika's Bakery Delights")

# SESSION STATES
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "cart" not in st.session_state:
    st.session_state["cart"] = []

if "order_success" not in st.session_state:
    st.session_state["order_success"] = False

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "Assistant",
            "content": "Hi! How can I help you?"
        }
    ]

# JSON FILES
json_inv = Path("inventory.json")
if json_inv.exists():
    with open(json_inv, "r") as f:
        inventory = json.load(f)

json_user = Path("users.json")
if json_user.exists():
    with open(json_user, "r") as f:
        users = json.load(f)

json_order = Path("orders.json")
if json_order.exists():
    with open(json_order, "r") as f:
        orders = json.load(f)

# CUSTOMER DASHBOARD
if st.session_state['role'] == 'Customer' and st.session_state['logged_in']:
    user = st.session_state['user']
    if st.session_state['page'] == 'Home':
        st.sidebar.markdown(f"## Welcome {user['full_name']}! This is the Customer Dashboard!")
        st.sidebar.markdown("### Here, you can browse our delicious bakery items and place your orders!")
        st.sidebar.markdown(f"Cart Items: {len(st.session_state['cart'])}")

        if st.session_state["order_success"]:
            st.success("Order placed successfully!")
            st.session_state["order_success"] = False

        tab1, tab2, tab3, tab4 = st.tabs(["Browse Items","Cart", "My Orders", "Cancel Order"])

        with tab1:
            st.markdown('### Browse the Menu and Place an Order!')
            col1, col2 = st.columns([4,2])

            with col1:
                selected_item = st.selectbox(
                    'Items',
                    options = inventory,
                    key = 'inventory_selector',
                    format_func = lambda item: f"{item['name']}"
                )

                quantity = st.number_input('Enter the Quantity', min_value = 1, step = 1)

                if st.button('Add to Cart',
                             key = 'add_to_cart_btn',
                             type = 'primary',
                             use_container_width=True):

                    if quantity > selected_item['stock']:
                        st.error('Not enough stock available.')
                    else:
                        st.session_state["cart"].append({
                            "item_id": selected_item["item_id"],
                            "item_name": selected_item["name"],
                            "price": selected_item["price"],
                            "quantity": quantity
                        })
                        st.success("Added to cart!")
                        st.rerun()

                # AI Chatbox
                with col2:
                    st.subheader("AI Assistant")
                    st.caption("Try asking:")
                    st.caption("- How do I place an order?")
                    st.caption("- How do I cancel an order?")
                    st.caption("- What items are available?")

                    if st.button("Clear Messages"):
                        st.session_state["messages"] = []

                    for message in st.session_state["messages"]:
                        if message["role"] == "User":
                            with st.chat_message("user"):
                                st.write(message["content"])
                        else:
                            with st.chat_message("assistant"):
                                st.write(message["content"])

                    # User input
                    user_input = st.text_input("Ask a question:")

                    if st.button("Send"):
                        if user_input:
                            
                            st.session_state["messages"].append({
                                "role": "User",
                                "content": user_input
                            })

                            # Generate AI response
                            if "order" in user_input.lower():
                                ai_response = "To place an order, go to Browse Items, add items to cart, then checkout."

                            elif "cancel" in user_input.lower():
                                ai_response = "Go to the Cancel Order tab and choose an order."

                            elif "items" in user_input.lower():
                                ai_response = "All items are listed in the Browse Items tab."

                            else:
                                ai_response = "Try one of the suggested questions."

                            st.session_state["messages"].append({
                                "role": "Assistant",
                                "content": ai_response
                            })

                            st.rerun()  

                if st.button("Go to Cart"):
                    st.info("Click on the Cart tab at the top to view your cart.")
        
        with tab2:
            st.subheader("Your Cart")

            cart = st.session_state["cart"]

            if cart == []:
                st.info("Your cart is empty.")
            else:
                total_cost = 0

                for item in cart:
                    item_total = item['price'] * item['quantity']
                    total_cost += item_total

                    st.write(f"{item['item_name']} | Qty: {item['quantity']} | Total: ${item_total}")

                st.markdown(f'### Total: ${total_cost}')

                if st.button("Checkout", key="checkout_tab2"):

                    for cart_item in cart:

                        # Update inventory
                        for inv_item in inventory:
                            if inv_item["item_id"] == cart_item["item_id"]:
                                inv_item["stock"] -= cart_item["quantity"]

                        # Add order
                        orders.append({
                            "id": str(uuid.uuid4()),
                            "customer_email": user["email"],
                            "item_id": cart_item["item_id"],
                            "item_name": cart_item["item_name"],
                            "quantity": cart_item["quantity"],
                            "status": "Placed",
                            "total": cart_item["price"] * cart_item["quantity"]
                        })

                    
                    with open(json_inv, "w") as f:
                        json.dump(inventory, f)

                    with open(json_order, "w") as f:
                        json.dump(orders, f)

                    st.session_state["cart"] = []
                    st.session_state["order_success"] = True
                    st.rerun()

        with tab3:
            st.subheader("My Orders")

            user_orders = []

            for order in orders:
                if order["customer_email"] == user["email"]:
                    user_orders.append(order)

            if user_orders == []:
                st.info("No orders yet.")
            else:
                for order in user_orders:
                    st.write(f"Order ID: {order['id']}")
                    st.write(f"Item: {order['item_name']}")
                    st.write(f"Quantity: {order['quantity']}")
                    st.write(f"Status: {order['status']}")
                    st.write("---")

                st.write("")

            edit_orders = []
            for order in user_orders:
                if order["status"] == "Placed":
                    edit_orders.append(order)

            if edit_orders == []:
                st.info("No placed orders available to edit.")
            else:
                st.markdown("### Edit a Placed Order")
                # LIST OF ORDERS
                order_ids = []
                for order in edit_orders:
                    order_ids.append(order["id"])
                
                selected_order_id = st.selectbox("Select Order to Edit", order_ids)

                # FINDING ORDER
                selected_order = None
                for order in edit_orders:
                    if order["id"] == selected_order_id:
                        selected_order = order
                        break

                if selected_order:
                    new_quantity = st.number_input("New Quantity", min_value=1, step=1, value=selected_order["quantity"])

                    if st.button("Update Order"):

                        # RESTORING OLD STOCK
                        for inv_item in inventory:
                            if inv_item["name"] == selected_order["item_name"]:
                                inv_item["stock"] += selected_order["quantity"]
                                break

                        # DEDUCT NEW STOCK
                        for inv_item in inventory:
                            if inv_item["name"] == selected_order["item_name"]:
                                inv_item["stock"] -= new_quantity
                                break

                        # UPDATING ORDER
                        selected_order["quantity"] = new_quantity

                        with open(json_inv, "w") as f:
                            json.dump(inventory, f)

                        with open(json_order, "w") as f:
                            json.dump(orders, f)

                        st.success("Order updated!")
                        st.rerun()

        with tab4:
            st.subheader("Cancel Order")

            cancelled_orders = []

            for order in orders:
                if order["customer_email"] == user["email"] and order["status"] == "Placed":
                    cancelled_orders.append(order)

            if cancelled_orders == []:
                st.info("No orders to cancel.")
            else:
                order_ids = []

                for order in cancelled_orders:
                    order_ids.append(order["id"])

                selected_order_id = st.selectbox("Select Order to Cancel", order_ids)

                if st.button("Cancel Selected Order"):
                    for order in orders:
                        if order["id"] == selected_order_id:
                            order["status"] = "Cancelled"

                            # RESTORE INVENTORY
                            for item in inventory:
                                if item["name"] == order["item_name"]:
                                    item["stock"] += order["quantity"]

                    with open(json_inv, "w") as f:
                        json.dump(inventory, f)

                    with open(json_order, "w") as f:
                        json.dump(orders, f)

                    st.success("Order cancelled.")
                    st.rerun()

# OWNER DASHBOARD
elif st.session_state['role'] == 'Owner':
    user = st.session_state["user"]

    st.sidebar.markdown(f"Logged in as: {user['full_name']} ({user['email']})")
    st.markdown(f"## Welcome, {user['full_name']}!")
    st.markdown("## Owner Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["View Orders", "View Inventory","Restock Inventory","Update Order Status"])

    with tab1:
        st.subheader("Orders Placed")
        for order in orders:
            st.write("Order ID:", order["id"])
            st.write("Customer:", order["customer_email"])
            st.write("Item:", order["item_name"])
            st.write("Quantity:", order["quantity"])
            st.write("Status:", order["status"])
            st.write("---")

    with tab2:
        st.subheader("Inventory:")
        for item in inventory:
            st.write("Item Name:", item["name"])
            st.write("Stock:", item["stock"])
            st.write("---")

    with tab3:
        st.subheader("Restock Inventory")

        item_names = [item["name"] for item in inventory]

        selected_item = st.selectbox("Select Item to Restock", item_names)
        add_quantity = st.number_input("Add Amount", min_value=1, step=1)

        if st.button("Update Stock"):
            for item in inventory:
                if item["name"] == selected_item:
                    with st.spinner("Updating stock..."):
                        time.sleep(2)

                    item["stock"] += add_quantity

                    with open(json_inv, "w") as f:
                        json.dump(inventory, f)

                    st.success(f"Stock updated for {selected_item}!")
                    time.sleep(2)
                    st.rerun()

    with tab4:
        st.subheader("Update Order Status")
        col1, col2 = st.columns([3,3])

        with col1:
            st.markdown(f"#### Orders Placed:")
            for order in orders:
                st.write("Order ID:", order["id"])
                st.write("Customer:", order["customer_email"])
                st.write("Item:", order["item_name"])
                st.write("Quantity:", order["quantity"])
                st.write("Status:", order["status"])
                st.write("---")


        with col2:
            st.markdown(f"#### Update Status:")
            order_ids = [order["id"] for order in orders]
            selected_order = st.selectbox("Select Order to Update", order_ids, key="order_select")

            new_status = st.selectbox("Select New Status", ["Placed", "Completed", "Shipped", "Cancelled"], key="new_status")

            if st.button("Update Status", key="update_status"):
                for order in orders:
                    if order["id"] == selected_order:
                        order["status"] = new_status
                        break

                with open(json_order, "w") as f:
                    json.dump(orders, f)

                st.success("Order " + selected_order + " status updated to " + new_status + "!")
                time.sleep(2)
                st.rerun()

else:

    # --- LOGIN --
    st.subheader("Log In")
    with st.container(border=True):
        email_input = st.text_input("Email", key= "email_login")
        password_input = st.text_input("Password", type="password",key="password_login")
        
        if st.button("Log In", type="secondary", use_container_width=True):
            with st.spinner("Logging in..."):
                time.sleep(2) # Fake backend delay
                
                # Find user
                found_user = None
                for user in users:
                    if user["email"].strip().lower() == email_input.strip().lower() and user["password"] == password_input:
                        found_user = user
                        break
                
                if found_user:
                    st.success(f"Welcome back, {found_user['email']}!")
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = found_user
                    st.session_state["role"] = found_user["role"]
                    st.session_state["page"] = "Home"


                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    # --- REGISTRATION ---
    st.subheader("New Customer Account")
    with st.container(border=True):
        new_email = st.text_input("Email", key= "email_register")
        new_password = st.text_input("Password", type="password", key= "password_edit")
        
        if st.button("Create Account", key= "register_btn", type="primary", use_container_width=True):
            with st.spinner("Creating account..."):
                time.sleep(2) 
                existing_user = None
                for user in users:
                    if user["email"].lower() == new_email.lower():
                        existing_user = user
                        break

                if existing_user:
                    st.error("An account with that email already exists.")

                else:
                    users.append({
                        "id": str(uuid.uuid4()),
                        "email": new_email,
                        "password": new_password,
                        "role": "Customer"
                    })
                    
                    with open(json_user, "w") as f:
                        json.dump(users,f)

                    st.success("Account created!")
                    st.rerun()

    st.write("---")
    st.dataframe(users)

with st.sidebar:
    if  st.session_state["logged_in"] == True:
        user = st.session_state["user"]
        st.markdown(f"Logged User Email: {user['email']}")

# LOG OUT BUTTON
if st.session_state['logged_in']:
    if st.sidebar.button('Log out', type = 'primary', use_container_width = True):
        with st.spinner('Logging out...'):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            time.sleep(2)
            st.rerun()






