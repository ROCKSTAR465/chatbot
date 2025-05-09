import streamlit as st
import pandas as pd
import sqlite3
import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re
import os

# Load tokenizer and model for text-to-SQL conversion
tokenizer = AutoTokenizer.from_pretrained("cssupport/t5-small-awesome-text-to-sql", use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained("cssupport/t5-small-awesome-text-to-sql")

# Paths for database and chat history storage
db_path = "chatbot_data.db"
chat_memory_path = "chat_memory.json"

def init_db():
    conn = sqlite3.connect(db_path)
    return conn

def upload_and_store_data(file, conn):
    df = pd.read_excel(file)
    table_name = "data_table"
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    return df

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

def load_chat_memory():
    if os.path.exists(chat_memory_path):
        with open(chat_memory_path, "r") as f:
            return json.load(f)
    return []

def save_chat_memory(history):
    with open(chat_memory_path, "w") as f:
        json.dump(history, f)

st.title("Text-to-SQL Chatbot")
st.sidebar.header("Upload an Excel file")

conn = init_db()

uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx"])
if uploaded_file:
    df = upload_and_store_data(uploaded_file, conn)
    st.write("Data uploaded successfully! Here is a preview:")
    st.dataframe(df.head())

user_query = st.text_input("Ask your question about the data:")
if user_query:
    try:
        sql_query = generate_sql_query(user_query, "data_table")
        if sql_query:
            result = pd.read_sql_query(sql_query, conn)
            st.markdown(f"**Generated SQL Query:**\n```sql\n{sql_query}\n```")
            st.write("**Query Result:**")
            st.dataframe(result)
        else:
            st.error("Sorry, I couldn't generate a valid SQL query.")
    except Exception as e:
        st.error(f"Error processing query: {e}")
