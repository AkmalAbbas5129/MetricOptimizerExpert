from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory, ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
import streamlit as st

load_dotenv()


def get_llm_model():
    llm = AzureChatOpenAI(
        model_name="gpt-35-turbo-16k",
        deployment_name=st.secrets.openai["deployment_name"],
        openai_api_key=st.secrets.openai["openai_api_key"],
        azure_endpoint=st.secrets.openai["azure_endpoint"],
        openai_api_type="azure",
        openai_api_version="2023-03-15-preview",
    )

    return llm


llm = get_llm_model()
demo_ephemeral_chat_history = ChatMessageHistory()


def summarize_messages(chain_input):
    stored_messages = demo_ephemeral_chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "user",
                "Summarize the chat messages into meaningful summarise which contains all specific details"
            ),
        ]
    )
    summarization_chain = summarization_prompt | llm

    summary_message = summarization_chain.invoke({"chat_history": stored_messages})

    demo_ephemeral_chat_history.clear()

    demo_ephemeral_chat_history.add_message(summary_message)

    return True


class InsightsModel(BaseModel):
    """SQL Generated by LLM"""
    report: str = Field(description="Code written in Python or reply from Model")


def get_response_ai(human_msg):

    """
    After this being acting as an expert in the field you will also write your insights as a report in a nice format so
    that user can understand it better.
    """

    # Initial Version
    # template = """I want you to act like an Expert in Linear Programming and Mathematical Expert who can optimize the
    # workflows and can give insights on the problems. User will ask you to optimize something about their businesses.
    # You will ask questions if necessary from them so that to complete your formulation. Once you have asked possible
    # questions then you will do calculation with your extensive knowledge and give the optimal solution to optimize the
    # metrics asked by user and will write a report in a way so that a layman can also understand it.
    #
    #
    # Current conversation:
    # {chat_history}
    # Human: {input}
    # AI Assistant:"""

    #------------------------------------------------------------------
    template = """
    I want you to act like an Expert Mathematics and Linear Programming Expert who solves optimization problems computationaly.
    You will be given a problem by Human to optimize metrics. Your Job is to ask questions to complete your
    prerequiste to solve the optimiztion problems.
    Once you have completed your formulation then you will do the calculations and will provide the Human with
    optimal solution and conclusions. 
    First perform an initial calculation and then recheck it so that no mistake should be there.
    Once the calculation and optimal solution is found, then you will switch role to being an expert writer and will
    write the conclusion in such a way that even a layman can understand it. Your answer should contain steps which you have
    performed to solve the optimization problem and conclusion in the end.

    Current conversation:
    {chat_history}
    Human: {input}
    AI Assistant:"""

    #-------------------------------------------------------------------
    # Pulp Version
    # template = """
    # I want you to act as an expert programmer who can write code using Pulp library to solve optimization problems
    # using your extensive knowledge of Mathematics and Linear Programming.
    # User will ask you to optimize metrics of their choice.
    # You can ask follow up questions from the user to formulate the problem in programming if necessary.
    # Once your understanding is complete then you will write the code in your mind in python using Pulp library to
    # solve the problem. Once the code is written and understood then you will solve it yourself being a python interpreter
    # and show the result.
    #
    # Current conversation:
    # {chat_history}
    # Human: {input}
    # AI Assistant:"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                template,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    parser = PydanticOutputParser(pydantic_object=InsightsModel)

    chain = prompt | get_llm_model()

    chain_with_message_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: demo_ephemeral_chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        verbose=True
    )

    # chain_with_message_history = RunnableWithMessageHistory(
    #     chain,
    #     lambda session_id: demo_ephemeral_chat_history,
    #     input_messages_key="input",
    #     history_messages_key="chat_history",
    # )

    chain_with_summarization = (
            RunnablePassthrough.assign(messages_summarized=summarize_messages)
            | chain_with_message_history
    )

    msg = chain_with_summarization.invoke(
        {"input": human_msg},
        {"configurable": {"session_id": "unused"}},
    )

    # print(demo_ephemeral_chat_history.messages)
    return msg.content


def python_tool():

    from langchain.agents import Tool
    from langchain_experimental.utilities import PythonREPL

    code = """
import pulp

# Create the problem
problem = pulp.LpProblem("GlassProduction", pulp.LpMaximize)

# Define the decision variables
x = pulp.LpVariable("x", lowBound=0, cat='Integer')  # Number of wine glass batches
y = pulp.LpVariable("y", lowBound=0, cat='Integer')  # Number of beer glass batches

# Define the objective function
profit = 5 * x + 4.5 * y
problem += profit

# Define the constraints
production_hours = 6 * x + 5 * y <= 60  # Production capacity constraint
warehouse_capacity = 10 * x + 20 * y <= 150  # Warehouse capacity constraint
wine_glass_batches = x == 6  # Number of wine glass batches constraint

problem += production_hours
problem += warehouse_capacity
problem += wine_glass_batches

# Solve the problem
problem.solve()

# Check if the problem has an optimal solution
if problem.status == pulp.LpStatusOptimal:
    # Get the optimal values of the decision variables
    wine_glass_batches = x.value()
    beer_glass_batches = y.value()
    max_profit = pulp.value(problem.objective)

    # Print the optimal production plan and maximum profit
    print("Optimal production plan:")
    print("Number of wine glass batches:", wine_glass_batches)
    print("Number of beer glass batches:", beer_glass_batches)
    print("Maximum profit:", max_profit)
else:
    print("No optimal solution found.")
    """

    code = """
from pulp import *

# Create the problem
prob = LpProblem("Exercise Optimization", LpMaximize)

# Decision variables
pushups = LpVariable("Pushups", lowBound=0, cat='Integer')
running = LpVariable("Running", lowBound=0, cat='Integer')

# Objective function
prob += 3 * pushups + 10 * running, "Calorie Burn"

# Constraints
prob += pushups <= 5 * 10, "Pushups Constraint"
prob += running <= 1 * 10, "Running Constraint"

# Solve the problem
prob.solve()

# Print the optimal solution
print("Optimal Exercise Plan:")
print("Pushups:", value(pushups))
print("Running:", value(running))
    """

    python_repl = PythonREPL()
    out = python_repl.run(code)
    print(out)
    # repl_tool = Tool(
    #     name="python_repl",
    #     description="A Python shell. Use this to execute python commands. Input should be a valid python command. If "
    #                 "you want to see the output of a value, you should print it out with `print(...)`. If there is not package install"
    #                 "please install it using pip",
    #     func=python_repl.run,
    # )

    # repl_tool.invoke("print('hey')")


if __name__ == "__main__":
    # get_response_ai()
    python_tool()
