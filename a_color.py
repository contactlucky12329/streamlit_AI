import streamlit as st

st.title("Lakhwinder")


response = st.sidebar.selectbox("Take your position",("BUY","SELL" ))


col1, col2, col3 = st.columns(3)


with col1:
    label3 = st.text("This is a label")

with col2:
    label4 = st.text("This is a label")

with col3:
    label5 = st.text("This is a label")

button1 = st.button("Click Me")

label1 = st.text("This is a label")

if response:
    label1.text(f"You selected {response} {button1}")
else:
    label1.text(f"Please select a choice")

label2 = st.text("This is a label")

button2 = st.button("Click Me1")

if button1:
    label2.text(f"Button1 Clicked")

if button2:
    label2.text(f"Button2 Clicked")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Button 1'):
        st.write('Button 1 clicked')

with col2:
    if st.button('Button 2'):
        st.write('Button 2 clicked')

with col3:
    if st.button('Button 3'):
        st.write('Button 3 clicked')