import chainlit as cl
from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

# Function to generate SQL queries
def generate_sql_query(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql_query

# Chainlit app
@cl.on_chat_start
async def start_chat():
    await cl.Message(content="Welcome to the SQL Query Chatbot! Type your prompt below.").send()

@cl.on_message
async def main(message: str):
    # Generate SQL query
    sql_query = generate_sql_query(message)
    
    # Send the response back to the user
    await cl.Message(content=f"Generated SQL Query: {sql_query}").send()
