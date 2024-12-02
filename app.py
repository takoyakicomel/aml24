import streamlit as st
import pandas as pd
import random
import time

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

# Promo codes and their discount percentages
promo_codes = {
    "MEOW20": 0.20,  # 20% discount
}

# Initialize session state
if "ticket_quantities" not in st.session_state:
    st.session_state["ticket_quantities"] = {category: 0 for category in ticket_prices}
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "promo_code" not in st.session_state:
    st.session_state["promo_code"] = ""

# Function to reset ticket quantities
def reset_tickets():
    for category in st.session_state["ticket_quantities"]:
        st.session_state["ticket_quantities"][category] = 0

# Title and introduction
st.title("🎶 Anugerah Malaysia Live 2024")
st.subheader("Featuring Siti Nurhaliza, Yuna, and Faizal Tahir")
st.write(""" 
**📅 Date**: 25th December 2024  
**📍 Venue**: Bukit Jalil National Stadium  
Secure your spot for this unforgettable concert! Choose your ticket category below and book now!  
""")

# Display a much smaller concert image
st.image("https://i.imgflip.com/41aizo.jpg", width=400)  # Smaller width value

# Ticket categories and prices section
st.header("🎫 Ticket Categories")
with st.expander("Click to View Details"):
    for category, price in ticket_prices.items():
        st.write(f"**{category}**: RM {price}")
        st.write(f"🔎 *{ticket_descriptions[category]}*")

# Ticket selection
st.header("🎟 Select Your Tickets")
for category, price in ticket_prices.items():
    st.session_state["ticket_quantities"][category] = st.number_input(
        f"{category} (RM {price} each)",
        min_value=0,
        step=1,
        value=st.session_state["ticket_quantities"][category],
        key=f"quantity_{category}",
    )

# Ticket Overview without Plotly (using basic text summary)
st.header("📊 Ticket Overview")
data = {
    "Category": list(st.session_state["ticket_quantities"].keys()),
    "Tickets": list(st.session_state["ticket_quantities"].values()),
}
df = pd.DataFrame(data)

# Display the ticket selection summary as text
st.write(df.to_string(index=False))

# Sidebar summary
st.sidebar.title("📊 Booking Summary")
total_tickets = sum(st.session_state["ticket_quantities"].values())
total_amount = sum(
    st.session_state["ticket_quantities"][category] * price
    for category, price in ticket_prices.items()
)

# Apply discount if promo code is valid
discount_applied = False
discount_amount = 0
if st.session_state["promo_code"]:
    discount_amount = total_amount * promo_codes[st.session_state["promo_code"]]
    total_amount -= discount_amount
    discount_applied = True

# Update sidebar with total
if total_tickets > 0:
    st.sidebar.write(f"**Total Tickets**: {total_tickets}")
    
    if discount_applied:
        st.sidebar.write(f"**Original Total**: RM {total_amount + discount_amount:.2f}")
        st.sidebar.write(f"**Discount Applied**: -RM {discount_amount:.2f}")
        st.sidebar.write(f"**Total Amount (After Discount)**: RM {total_amount:.2f}")
        st.sidebar.write("🎉 Discount Applied!")
    else:
        st.sidebar.write(f"**Total Amount**: RM {total_amount:.2f}")
    
    st.sidebar.write("**Breakdown**:")
    for category, quantity in st.session_state["ticket_quantities"].items():
        if quantity > 0:
            st.sidebar.write(f"- {category}: {quantity} ticket(s)")
else:
    st.sidebar.write("No tickets selected yet.")

# Promo Code Section
st.header("💸 Promo Code")
promo_code_input = st.text_input("Enter your promo code (if any):", value=st.session_state["promo_code"])

# Apply Promo Code
if promo_code_input:
    if promo_code_input in promo_codes:
        discount = promo_codes[promo_code_input]
        st.session_state["promo_code"] = promo_code_input
        st.sidebar.write(f"🎉 Promo code applied! You get a {int(discount * 100)}% discount.")
    else:
        st.sidebar.write("❌ Invalid promo code. Please check and try again.")
else:
    st.sidebar.write("Enter a promo code to get a discount!")

# User information and checkout
st.header("Checkout")
user_name = st.text_input("Enter your name:", value=st.session_state["user_name"])
if total_tickets > 0 and st.button("Proceed to Checkout"):
    if user_name:
        st.session_state["user_name"] = user_name
        
        # Generate unique ticket number
        ticket_number = f"TKT-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Generate plain text ticket summary formatted like a real ticket
        ticket_summary = []
        for category, quantity in st.session_state["ticket_quantities"].items():
            if quantity > 0:
                ticket_summary.append(f"{category}: {quantity} ticket(s)")

        ticket_text = f"""
---------------------------------------------------------
                    🎶 Anugerah Malaysia Live 2024
---------------------------------------------------------
Date: 25th December 2024
Venue: Bukit Jalil National Stadium

Name: {user_name}
Ticket Number: {ticket_number}
Total Tickets: {total_tickets}
---------------------------------------------------------
Ticket Breakdown:
---------------------------------------------------------
"""
        
        for category, quantity in st.session_state["ticket_quantities"].items():
            if quantity > 0:
                ticket_text += f"{category}: {quantity} ticket(s)\n"

        ticket_text += f"""
Total Amount: RM {total_amount:.2f}
"""
        
        if discount_applied:
            ticket_text += f"Discount Applied: RM {discount_amount:.2f}\n"
        
        ticket_text += """
---------------------------------------------------------

Thank you for your purchase! We look forward to seeing you at the concert.

Note: This is a digital ticket. Please show it at the venue entrance.
---------------------------------------------------------
"""

        # Display success message
        st.success("Your ticket has been generated!")
        
        # Display balloons
        st.balloons()

        st.write("Here are your ticket details:")
        st.text(ticket_text)
        
        # Download button for the formatted ticket text file
        st.download_button(
            label="Download Your Ticket",
            data=ticket_text,
            file_name=f"{user_name}_ticket.txt",
            mime="text/plain",
        )
    else:
        st.warning("Please enter your name to proceed.")
else:
    st.warning("Please select tickets before proceeding.")

# Reset button
if st.button("Reset Tickets"):
    reset_tickets()
    st.success("Ticket selections reset!")
