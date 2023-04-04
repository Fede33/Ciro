import streamlit as st

# Define a list of orders
orders = ["Pizza", "Burger", "Salad", "Pasta"]

# Display each order in an expander with a button to mark it as complete
for i, order in enumerate(orders):
    with st.expander(order):
        button = st.button(f"Mark as complete {i}")
        if button:
            st.write(f"{order} marked as complete")
