import streamlit as st
import pandas as pd
import sqlite3
import torch
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load tokenizer and model for text-to-SQL conversion
tokenizer = AutoTokenizer.from_pretrained("cssupport/t5-small-awesome-text-to-sql", use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained("cssupport/t5-small-awesome-text-to-sql")

# Paths for database
db_path = "chatbot_data.db"

# Function to initialize the database
def init_db():
    conn = sqlite3.connect(db_path)
    return conn

# Function to upload and store data
def upload_and_store_data(file_path, conn):
    df = pd.read_excel(file_path)
    table_name = "data_table"
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    return df

# Function to generate SQL query from natural language input
def generate_sql_query(user_input, table_name):
    prompt = (
        f"Translate the following natural language query into an SQL query: "
        f"The table is named '{table_name}'. The query is: '{user_input}'."
    )

    input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(input_ids, max_length=150, num_beams=5, early_stopping=True)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)

    sql_match = re.search(r"select.*?from.*?(where.*?|);?$", result, re.IGNORECASE | re.DOTALL)
    return sql_match.group(0).strip() if sql_match else None

# Streamlit UI
st.title("📊 Text-to-SQL Chatbot")

# Initialize database connection
conn = init_db()

# File Upload Section
st.sidebar.header("Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = upload_and_store_data(uploaded_file, conn)
    st.sidebar.success("File uploaded and stored successfully!")
    st.sidebar.write("### Data Preview:")
    st.sidebar.dataframe(df.head())

# Query Input Section
st.subheader("Ask a question about your data:")
user_input = st.text_area("Enter your query in natural language")

if st.button("Generate SQL Query"):
    if uploaded_file:
        table_name = "data_table"
        try:
            sql_query = generate_sql_query(user_input, table_name)
            if sql_query:
                result = pd.read_sql_query(sql_query, conn)
                st.write("### **Generated SQL Query:**")
                st.code(sql_query, language="sql")
                
                st.write("### **Query Result:**")
                st.dataframe(result)
            else:
                st.error("Sorry, I couldn't generate a valid SQL query.")
        except Exception as e:
            st.error(f"Error processing query: {e}")
    else:
        st.warning("Please upload an Excel file first.")
