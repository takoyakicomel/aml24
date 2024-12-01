import streamlit as st
from datetime import datetime

# Ticket categories and prices (in RM)
ticket_prices = {
    "Meet & Greet (Ultimate Fan Experience)": 1000,
    "VIP (Front Row)": 500,
    "Premium (Middle Section)": 300,
    "Regular (Back Row)": 100,
}

ticket_descriptions = {
    "Meet & Greet (Ultimate Fan Experience)": "Exclusive access to meet the artists backstage.",
    "VIP (Front Row)": "Enjoy front-row seats for the best view of the concert.",
    "Premium (Middle Section)": "Perfect view from the middle section of the stadium.",
    "Regular (Back Row)": "Affordable seats with a great atmosphere at the back.",
}

# Initialize session state for ticket quantities
if "ticket_quantities" not in st.session_state:
    st.session_state["ticket_quantities"] = {category: 0 for category in ticket_prices}
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "discount" not in st.session_state:
    st.session_state["discount"] = 0

# Function to reset ticket quantities
def reset_tickets():
    for category in st.session_state["ticket_quantities"]:
        st.session_state["ticket_quantities"][category] = 0
    st.session_state["discount"] = 0

# Title and introduction
st.title("🎶 Anugerah Malaysia Live 2024")
st.subheader("Featuring Siti Nurhaliza, Yuna, and Faizal Tahir")
st.write("""  
**📅 Date**: 25th December 2024  
**📍 Venue**: Bukit Jalil National Stadium  
Secure your spot for this unforgettable concert! Choose your ticket category below and book now!  
""")

# Countdown timer
event_date = datetime(2024, 12, 25)
remaining_time = event_date - datetime.now()
st.sidebar.title("⏳ Countdown to Event")
st.sidebar.write(f"**{remaining_time.days} days** left until the concert!")

# Add space and an image
st.image("https://i.imgflip.com/41aizo.jpg", use_column_width=False, width=400)

# Interactive ticket selection
st.header("🎟 Select Your Tickets Below:")
for category in ticket_prices:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"**{category}**: RM {ticket_prices[category]} per ticket")
    with col2:
        if st.button(f"➖ {category}", key=f"decrease_{category}"):
            if st.session_state["ticket_quantities"][category] > 0:
                st.session_state["ticket_quantities"][category] -= 1
    with col3:
        if st.button(f"➕ {category}", key=f"increase_{category}"):
            st.session_state["ticket_quantities"][category] += 1

# Sidebar: Booking summary
st.sidebar.title("📊 Booking Summary")
total_tickets = sum(st.session_state["ticket_quantities"].values())
total_amount = sum(
    st.session_state["ticket_quantities"][category] * price
    for category, price in ticket_prices.items()
)
if total_tickets > 0:
    st.sidebar.write(f"**Total Tickets**: {total_tickets}")
    for category, quantity in st.session_state["ticket_quantities"].items():
        if quantity > 0:
            st.sidebar.write(f"{category}: {quantity} tickets")
    st.sidebar.write(f"**Total Price**: RM {total_amount}")
else:
    st.sidebar.write("No tickets selected yet.")

# Promo code feature
st.header("🎟️ Promo Code (Optional)")
promo_code = st.text_input("Enter Promo Code")
if promo_code == "FAN20":
    st.session_state["discount"] = total_amount * 0.2
    st.success(f"Promo code applied! You saved RM {st.session_state['discount']:.2f}")
else:
    st.session_state["discount"] = 0

# Final amount after discount
final_amount = total_amount - st.session_state["discount"]
st.write(f"💸 **Final Amount**: RM {final_amount:.2f}")

# Name input and checkout
if total_tickets > 0:
    st.header("📋 Enter Your Details")
    st.text_input("Your Name", key="user_name", value=st.session_state["user_name"])

    if st.button("Proceed to Checkout"):
        user_name = st.session_state["user_name"]
        if user_name:
            st.image("https://i.imgflip.com/5563ph.jpg", width=200)
            st.write(f"🎉 Thank you for your booking, {user_name}!")
            st.write(f"Your total amount is **RM {final_amount:.2f}**.")
            st.write("You have selected the following tickets:")
            for category, quantity in st.session_state["ticket_quantities"].items():
                if quantity > 0:
                    st.write(f"- {category}: {quantity} tickets")
            st.write("We look forward to seeing you at the concert!")
            st.balloons()

            # Download ticket
            ticket_data = f"Name: {user_name}\nTickets:\n"
            for category, quantity in st.session_state["ticket_quantities"].items():
                if quantity > 0:
                    ticket_data += f"- {category}: {quantity} tickets\n"
            ticket_data += f"Total Amount: RM {final_amount:.2f}"
            st.download_button(
                label="Download Your Ticket",
                data=ticket_data,
                file_name=f"{user_name}_tickets.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please enter your name to proceed.")
else:
    st.warning("Please select at least one ticket to proceed.")

# Reset tickets
if st.button("Reset Tickets"):
    reset_tickets()
    st.success("Selections have been reset!")
