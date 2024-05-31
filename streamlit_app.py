import streamlit as st
from openai_utils import solve_optimization_problem
import time
from azure_blob_utils import get_blob_service_client, append_to_csv
import pandas as pd

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
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = ""

# Set the title of the app
st.title("The GenOptimzer")

# Create text areas for Problem Statement, Objective to Solve, and Constraints
st.session_state['problem_statement'] = st.text_area("Problem Statement", value=st.session_state['problem_statement'])
st.session_state['objective_to_solve'] = st.text_area("Objective to Solve",
                                                      value=st.session_state['objective_to_solve'])
st.session_state['constraints'] = st.text_area("Constraints", value=st.session_state['constraints'])


# Define the function to get AI response
def generate_solution():
    with st.spinner("Generating solution..."):
        # Simulate a delay for demonstration purposes
        time.sleep(1)
        solution = solve_optimization_problem(st.session_state['problem_statement'],
                                              st.session_state['objective_to_solve'], st.session_state['constraints'])
        if solution:
            st.session_state['solution'] = solution
            st.session_state['solution_status'] = "Success"
        else:
            st.session_state['solution'] = "Failed to generate solution."
            st.session_state['solution_status'] = "Failed"


# Log user interaction to Azure Blob Storage
def log_user_interaction(problem_statement, objective, constraints, solution, feedback):
    connection_string = st.secrets.blob["connection_string"]
    container_name = st.secrets.blob["container_name"]
    blob_name = "supply_chain_optimizer_data_log.csv"

    problem_statement = '"""' + problem_statement + '"""'
    objective = '"""' + objective + '"""'
    constraints = '"""' + constraints + '"""'
    solution = '"""' + solution + '"""'

    # Create a DataFrame with the new record
    new_data = pd.DataFrame([{
        'Problem Statement': problem_statement,
        'Objective': objective,
        'Constraints': constraints,
        'Solution': solution,
        'Feedback': feedback
    }])

    # Get the blob service client
    blob_service_client = get_blob_service_client(connection_string)

    # Append the new record to the CSV in Azure Blob Storage
    append_to_csv(blob_service_client, container_name, blob_name, new_data)


# Create Submit and Clear buttons
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Generate Solution", on_click=generate_solution)
with col3:
    clear_button = st.button("Clear")

# Display solution status box
if st.session_state.get('solution_status') == "Success":
    st.success("Solution found successfully!")

# Create a text area for Solution with a larger size
st.subheader("Solution:")
with st.expander("View Solution"):
    st.markdown(st.session_state.get('solution', ""))

    if st.session_state.get('solution_status') == "Success":
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("👍"):
                st.session_state['feedback'] = "correct"
                log_user_interaction(st.session_state['problem_statement'],
                                     st.session_state['objective_to_solve'],
                                     st.session_state['constraints'],
                                     st.session_state['solution'],
                                     st.session_state['feedback'])
                st.success("Thank you for your feedback!")
        with col2:
            if st.button("👎"):
                st.session_state['feedback'] = "incorrect"
                log_user_interaction(st.session_state['problem_statement'],
                                     st.session_state['objective_to_solve'],
                                     st.session_state['constraints'],
                                     st.session_state['solution'],
                                     st.session_state['feedback'])
                st.success("Thank you for your feedback!")

    elif st.session_state.get('solution_status') == "Failed":
        st.error("Failed to generate solution.")

# Add functionality to the Clear button
if clear_button:
    st.session_state['problem_statement'] = ""
    st.session_state['objective_to_solve'] = ""
    st.session_state['constraints'] = ""
    st.session_state['solution'] = ""
    st.session_state['solution_status'] = ""
    st.session_state['feedback'] = ""
    st.rerun()
