import streamlit as st
from pathlib import Path

from data.bakery_store import BakeryStore
from services.bakery_manager import BakeryManager

from ui.bakery_dashboard import BakeryDashboard
from ui.customer_dashboard import CustomerDashboard
from ui.owner_dashboard import OwnerDashboard


st.set_page_config(
    page_title="Blossom and Nandika's Bakery Delights",
    layout="centered",
    initial_sidebar_state="expanded"
)


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


# Data & Object Handler
store = BakeryStore(Path("data"))

inventory = store.load_inventory()
users = store.load_users()
orders = store.load_orders()

manager = BakeryManager(inventory, users, orders)


# Handling Pages
if st.session_state["logged_in"] == False:
    bakery_dashboard = BakeryDashboard(manager, store)
    bakery_dashboard.main()

else:
    if st.session_state["role"] == "Customer":
        customer_dashboard = CustomerDashboard(manager, store, store)
        customer_dashboard.main()

    elif st.session_state["role"] == "Owner":
        owner_dashboard = OwnerDashboard(manager, store, store)
        owner_dashboard.main()


# Log Out
if st.session_state["logged_in"] == True:
    if st.sidebar.button("Log out", type="primary", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["role"] = None
        st.session_state["page"] = "login"
        st.session_state["cart"] = []

        st.rerun()