import os
import pandas as pd
import sqlite3
import streamlit as st
from letta_client import Letta

# Install required dependencies
# Run the following command before executing the script:
# pip install pandas sqlite3 letta-client streamlit

# Initialize Letta for memory management
letta = Letta()

# Database setup
def setup_database():
    conn = sqlite3.connect("business.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS business_data (
                        id INTEGER PRIMARY KEY,
                        category TEXT,
                        revenue REAL,
                        profit REAL)''')
    conn.commit()
    conn.close()

# Load Excel data into SQL
def load_excel_to_sql(file_path):
    df = pd.read_excel(file_path)
    conn = sqlite3.connect("business.db")
    df.to_sql("business_data", conn, if_exists="replace", index=False)
    conn.close()

# Process user queries
def process_query(query):
    conn = sqlite3.connect("business.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Streamlit App
def main():
    st.title("🤖 Business Analysis Chatbot")
    st.write("Ask me anything about your business data!")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Load data and setup database
    file_path = "data.xlsx"  # Update this path to your Excel file
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found. Please ensure the file exists.")
        return

    setup_database()
    load_excel_to_sql(file_path)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your question here...")

    if user_input:
        # Append user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Process query using Letta memory
        letta.store_message(user_input)
        query = f"SELECT * FROM business_data WHERE category LIKE '%{user_input}%'"
        response = process_query(query)

        # Generate bot response
        if response:
            bot_response = f"Here's the data: {response}"
        else:
            bot_response = "No relevant data found."

        # Append bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Display bot response
        with st.chat_message("assistant"):
            st.write(bot_response)

# Run the Streamlit app
if __name__ == "__main__":
    main()
