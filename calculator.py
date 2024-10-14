import streamlit as st
from math import *

# Function to evaluate the expression
def evaluate_expression(expression):
    try:
        result = eval(expression)
        return result
    except:
        return "Error"

# Streamlit calculator layout
st.title("Scientific Calculator")

# Display field
if 'expression' not in st.session_state:
    st.session_state.expression = ""

# Display the current expression
st.text_input("Input", st.session_state.expression, key="display", disabled=True)

# Calculator buttons layout
buttons = [
    '(', ')', 'C', '/',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '0', '.', '=', '√',
    'x²', 'π'
]

# Define button columns (to simulate grid layout)
button_cols = [st.columns(4) for _ in range(6)]

# Function to handle button clicks
def handle_click(label):
    if label == "=":
        st.session_state.expression = str(evaluate_expression(st.session_state.expression))
    elif label == "C":
        st.session_state.expression = ""
    elif label == "√":
        st.session_state.expression += "sqrt("
    elif label == "x²":
        st.session_state.expression += "**2"
    elif label == "π":
        st.session_state.expression += str(pi)
    else:
        st.session_state.expression += label

# Add buttons to the columns
button_index = 0
for row in button_cols:
    for col in row:
        if button_index < len(buttons):
            button_label = buttons[button_index]
            # Customize the "=" and "C" buttons to be blue
            if button_label in ["=", "C"]:
                if col.button(button_label, key=button_label, use_container_width=True, type="primary"):
                    handle_click(button_label)
            else:
                if col.button(button_label, key=button_label, use_container_width=True):
                    handle_click(button_label)
            button_index += 1
