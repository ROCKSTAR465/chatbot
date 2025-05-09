# Import necessary libraries
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import torch

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")

# Function to generate SQL queries from user prompts
def generate_sql_query(prompt):
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    
    # Generate the output
    outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1)
    
    # Decode the generated text
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return sql_query

# Class to manage chat memory
class ChatMemory:
    def __init__(self):
        self.history = []

    def add_to_history(self, user_input, bot_response):
        self.history.append({"user": user_input, "bot": bot_response})

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

# Chatbot function
def chatbot():
    memory = ChatMemory()
    
    print("Welcome to the SQL Query Chatbot! Type 'exit' or 'quit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        
        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        
        # Add user input to history
        memory.add_to_history(user_input, "")
        
        # Generate SQL query
        sql_query = generate_sql_query(user_input)
        
        # Add bot response to history
        memory.add_to_history("", sql_query)
        
        # Print the generated SQL query
        print(f"Bot: Generated SQL Query: {sql_query}")
        
        # Optionally, print the conversation history
        print("\nConversation History:")
        for entry in memory.get_history():
            print(f"User: {entry['user']}")
            print(f"Bot: {entry['bot']}")
        print("\n")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
  
