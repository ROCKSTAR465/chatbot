import chainlit as cl
import pandas as pd
import sqlite3
import json
import torch
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

# Load tokenizer and model for text-to-SQL conversion
tokenizer = AutoTokenizer.from_pretrained("cssupport/t5-small-awesome-text-to-sql", use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained("cssupport/t5-small-awesome-text-to-sql")

# Paths for database and chat history storage
db_path = "chatbot_data.db"

def init_db():
    conn = sqlite3.connect(db_path)
    return conn

def upload_and_store_data(file_path, conn):
    df = pd.read_excel(file_path)
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

@cl.on_chat_start
async def start():
    cl.user_session.set("db_conn", init_db())
    await cl.Message("Upload an Excel file to start querying!").send()

@cl.on_message
async def handle_query(message: cl.Message):
    conn = cl.user_session.get("db_conn")
    table_name = "data_table"
    
    try:
        sql_query = generate_sql_query(message.content, table_name)
        if sql_query:
            result = pd.read_sql_query(sql_query, conn)
            response = f"**Generated SQL Query:**\n```sql\n{sql_query}\n```\n\n**Query Result:**"
            await cl.Message(response).send()
            await cl.Message(result.to_markdown()).send()
        else:
            await cl.Message("Sorry, I couldn't generate a valid SQL query.").send()
    except Exception as e:
        await cl.Message(f"Error processing query: {e}").send()

# @cl.on_file_upload
async def handle_upload(file: cl.File):
    conn = cl.user_session.get("db_conn")
    file_path = file.path
    df = upload_and_store_data(file_path, conn)
    await cl.Message("File uploaded and stored successfully! Here is a preview:").send()
    await cl.Message(df.head().to_markdown()).send()
