import streamlit as st
import time


class OwnerDashboard:

    def __init__(self, manager, inventory_store, order_store) -> None:
        self.manager = manager
        self.inventory_store = inventory_store
        self.order_store = order_store


    def main(self):
        user = st.session_state["user"]

        st.sidebar.markdown(f"Logged in as: {user['full_name']} ({user['email']})")
        st.markdown(f"## Welcome, {user['full_name']}!")
        st.markdown("## Owner Dashboard")

        tab1, tab2, tab3, tab4 = st.tabs([
            "View Orders",
            "View Inventory",
            "Restock Inventory",
            "Update Order Status"
        ])

        with tab1:
            self.view_orders()

        with tab2:
            self.view_inventory()

        with tab3:
            self.restock_inventory()

        with tab4:
            self.update_order_status()


    def view_orders(self):
        st.subheader("Orders Placed")

        for order in self.manager.orders:
            st.write("Order ID:", order["id"])
            st.write("Customer:", order["customer_email"])
            st.write("Item:", order["item_name"])
            st.write("Quantity:", order["quantity"])
            st.write("Status:", order["status"])
            st.write("---")


    def view_inventory(self):
        st.subheader("Inventory")

        for item in self.manager.inventory:
            st.write("Item Name:", item["name"])
            st.write("Stock:", item["stock"])
            st.write("---")


    def restock_inventory(self):
        st.subheader("Restock Inventory")

        item_names = []

        for item in self.manager.inventory:
            item_names.append(item["name"])

        selected_item = st.selectbox("Select Item to Restock", item_names)
        add_quantity = st.number_input("Add Amount", min_value=1, step=1)

        if st.button("Update Stock"):

            result = self.manager.restock_inventory(selected_item, add_quantity)

            if result == "Success":
                self.inventory_store.save(self.manager.inventory)

                st.success(f"Stock updated for {selected_item}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(result)


    def update_order_status(self):
        st.subheader("Update Order Status")

        col1, col2 = st.columns([3, 3])

        with col1:
            st.markdown("#### Orders Placed")

            for order in self.manager.orders:
                st.write("Order ID:", order["id"])
                st.write("Customer:", order["customer_email"])
                st.write("Item:", order["item_name"])
                st.write("Quantity:", order["quantity"])
                st.write("Status:", order["status"])
                st.write("---")

        with col2:
            st.markdown("#### Update Status")

            order_ids = []

            for order in self.manager.orders:
                order_ids.append(order["id"])

            selected_order = st.selectbox("Select Order to Update", order_ids, key="order_select")

            new_status = st.selectbox(
                "Select New Status",
                ["Placed", "Completed", "Shipped", "Cancelled"],
                key="new_status"
            )

            if st.button("Update Status", key="update_status"):

                result = self.manager.update_order_status(selected_order, new_status)

                if result == "Success":
                    self.order_store.save(self.manager.orders)

                    st.success("Order " + selected_order + " status updated to " + new_status + "!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result)