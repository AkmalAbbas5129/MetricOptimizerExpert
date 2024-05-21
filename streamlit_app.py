import streamlit as st
from openai_utils import solve_optimization_problem
import time

# Initialize session state keys
if 'solution' not in st.session_state:
    st.session_state['solution'] = ""
if 'solution_status' not in st.session_state:
    st.session_state['solution_status'] = ""
if 'problem_statement' not in st.session_state:
    st.session_state['problem_statement'] = ""
if 'objective_to_solve' not in st.session_state:
    st.session_state['objective_to_solve'] = ""
if 'constraints' not in st.session_state:
    st.session_state['constraints'] = ""

# Set the title of the app
st.title("Problem Solver")

# Create text areas for Problem Statement, Objective to Solve, and Constraints
st.session_state['problem_statement'] = st.text_area("Problem Statement", value=st.session_state['problem_statement'])
st.session_state['objective_to_solve'] = st.text_area("Objective to Solve", value=st.session_state['objective_to_solve'])
st.session_state['constraints'] = st.text_area("Constraints", value=st.session_state['constraints'])

# Define the function to get AI response
def generate_solution():
    with st.spinner("Generating solution..."):
        # Simulate a delay for demonstration purposes
        time.sleep(1)
        solution = solve_optimization_problem(st.session_state['problem_statement'], st.session_state['objective_to_solve'], st.session_state['constraints'])
        if solution:
            st.session_state['solution'] = solution
            st.session_state['solution_status'] = "Success"
        else:
            st.session_state['solution'] = "Failed to generate solution."
            st.session_state['solution_status'] = "Failed"

# Create Submit and Clear buttons
col1, col2 = st.columns(2)
with col1:
    st.button("Generate Solution", on_click=generate_solution)
with col2:
    clear_button = st.button("Clear")

# Display solution status box
if st.session_state.get('solution_status') == "Success":
    st.success("Solution found successfully!")
elif st.session_state.get('solution_status') == "Failed":
    st.error("Failed to generate solution.")

# Create a text area for Solution with a larger size
st.subheader("Solution:")
with st.expander("View Solution"):
    st.markdown(st.session_state.get('solution', ""))

# Add functionality to the Clear button
if clear_button:
    st.session_state['problem_statement'] = ""
    st.session_state['objective_to_solve'] = ""
    st.session_state['constraints'] = ""
    st.session_state['solution'] = ""  # Clear the solution as well
    st.session_state['solution_status'] = ""  # Clear the solution status as well
    st.rerun()
