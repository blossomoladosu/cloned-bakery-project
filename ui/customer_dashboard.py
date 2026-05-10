import streamlit as st
import time


class CustomerDashboard:

    def __init__(self, manager, inventory_store, order_store) -> None:
        self.manager = manager
        self.inventory_store = inventory_store
        self.order_store = order_store


    def save_all(self):
        self.inventory_store.save_inventory(self.manager.inventory)
        self.order_store.save_orders(self.manager.orders)


    def main(self):
        user = st.session_state["user"]

        st.sidebar.markdown(f"## Welcome {user['full_name']}!")
        st.sidebar.markdown(f"Cart Items: {len(st.session_state['cart'])}")

        if st.session_state["order_success"]:
            st.success("Order placed successfully!")
            st.session_state["order_success"] = False

        st.markdown(f"## Welcome, {user['full_name']}!")
        st.markdown("#### This is the Customer Dashboard")

        tab1, tab2, tab3, tab4 = st.tabs(["Browse Items", "Cart", "My Orders", "Cancel Order"])

        with tab1:
            self.browse_items()

        with tab2:
            self.cart_page(user)

        with tab3:
            self.my_orders(user)

        with tab4:
            self.cancel_order(user)


    def browse_items(self):
        col_header, col_cart_btn = st.columns([5, 1])

        with col_header:
            st.markdown("### Place your order!")

        with col_cart_btn:
            if st.button("Go to Cart", key="goto_cart_btn"):
                st.info("Click on the Cart tab at the top to view your cart.")

        selected_item = st.selectbox(
            "Items",
            options=self.manager.inventory,
            key="inventory_selector",
            format_func=lambda item: f"{item['name']}"
        )

        quantity = st.number_input(
            "Enter the Quantity",
            min_value=1,
            step=1
        )

        if st.button(
            "Add to Cart",
            key="add_to_cart_btn",
            type="primary",
            use_container_width=True
        ):

            result = self.manager.add_to_cart(
                st.session_state["cart"],
                selected_item,
                quantity
            )

            if result == "Success":
                st.success("Added to cart!")
                st.rerun()
            else:
                st.error(result)


    def cart_page(self, user):
        st.subheader("Your Cart")
        cart = st.session_state["cart"]

        if cart == []:
            st.info("Your cart is empty.")
        else:
            total_cost = 0

            for item in cart:
                item_total = item["price"] * item["quantity"]
                total_cost += item_total
                st.write(
                    f"{item['item_name']} | Qty: {item['quantity']} | Total: ${item_total:.2f}"
                )

            st.markdown(f"### Total: ${total_cost:.2f}")

            if st.button(
                "Checkout",
                key="checkout_tab2",
                type="primary",
                use_container_width=True
            ):

                result = self.manager.checkout(
                    cart,
                    user["email"]
                )

                if result == "Success":
                    self.save_all()
                    st.session_state["cart"] = []
                    st.session_state["order_success"] = True
                    st.rerun()
                else:
                    st.error(result)


    def my_orders(self, user):
        st.subheader("My Orders")
        user_orders = self.manager.find_orders_by_customer(user["email"])

        if user_orders == []:
            st.info("No orders yet.")
        else:
            for order in user_orders:
                st.write(f"Order ID: {order['id']}")
                st.write(f"Item: {order['item_name']}")
                st.write(f"Quantity: {order['quantity']}")
                st.write(f"Status: {order['status']}")

                st.write("---")

        edit_orders = self.manager.find_placed_orders_by_customer(user["email"])

        if edit_orders == []:
            st.info("No placed orders available to edit.")

        else:
            st.markdown("### Edit a Placed Order")
            order_ids = []
            for order in edit_orders:
                order_ids.append(order["id"])

            selected_order_id = st.selectbox("Select Order to Edit", order_ids)

            new_quantity = st.number_input(
                "New Quantity",
                min_value=1,
                step=1
            )

            if st.button(
                "Update Order",
                key="update_order_btn",
                type="primary",
                use_container_width=True
            ):

                result = self.manager.update_order_quantity(
                    selected_order_id,
                    new_quantity
                )

                if result == "Success":
                    self.save_all()
                    st.success("Order updated!")
                    time.sleep(1)

                    st.rerun()
                else:
                    st.error(result)


    def cancel_order(self, user):
        st.subheader("Cancel Order")
        placed_orders = self.manager.find_placed_orders_by_customer(user["email"])

        if placed_orders == []:
            st.info("No orders to cancel.")

        else:
            order_ids = []
            for order in placed_orders:
                order_ids.append(order["id"])

            selected_order_id = st.selectbox(
                "Select Order to Cancel",
                order_ids
            )

            if st.button(
                "Cancel Selected Order",
                key="cancel_order_btn",
                type="primary",
                use_container_width=True
            ):

                result = self.manager.cancel_order(selected_order_id)

                if result == "Success":
                    self.save_all()
                    st.success("Order cancelled.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(result)