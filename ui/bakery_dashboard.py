import streamlit as st
import time


class BakeryDashboard:
    
    def __init__(self, manager, user_store) -> None:
        self.manager = manager
        self.user_store = user_store

    def main(self):

        st.title("Blossom and Nandika's Bakery Delights")

        st.subheader("Log In")

        with st.container(border=True):
            email_input = st.text_input("Email", key="email_login")
            password_input = st.text_input("Password", type="password", key="password_login")

            if st.button("Log In", key="login_btn", type="primary", use_container_width=True):

                if email_input == "" or password_input == "":
                    st.error("Please enter both email and password")

                else:
                    with st.spinner("Logging in..."):
                        time.sleep(1)

                        found_user = self.manager.find_user(email_input, password_input)

                        if found_user:
                            st.success(f"Welcome, {found_user['full_name']}!")

                            st.session_state["logged_in"] = True
                            st.session_state["user"] = found_user
                            st.session_state["role"] = found_user["role"]
                            st.session_state["page"] = "Home"

                            time.sleep(1)
                            st.rerun()

                        else:
                            st.error("Invalid credentials")


        st.subheader("New Customer Account")

        with st.container(border=True):
            new_full_name = st.text_input("Full Name", key="full_name_register")
            new_email = st.text_input("Email", key="email_register")
            new_password = st.text_input("Password", type="password", key="password_register")

            if st.button("Create Account", key="register_btn", type="primary", use_container_width=True):

                result = self.manager.register_customer(
                    new_full_name,
                    new_email,
                    new_password
                )

                if result == "Success":
                    self.user_store.save_users(self.manager.users)
                    st.success("Account created!")
                    time.sleep(1)

                    st.rerun()
                else:
                    st.error(result)