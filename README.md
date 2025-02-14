# 📊 Text-to-SQL Chatbot

## 📝 Overview
This is a **Text-to-SQL Chatbot** built with **Streamlit** that allows users to upload an **Excel file**, ask **natural language queries**, and get **SQL-generated results** from the stored data. The chatbot uses a **Transformer-based model** (`cssupport/t5-small-awesome-text-to-sql`) to convert natural language into SQL queries. [Streamlit app link](https://chatbotic.streamlit.app/)

## 🚀 Features
- Upload an **Excel file** (provided within the repo) and store it in a SQLite database.
- Enter a **natural language query**, and the chatbot generates the corresponding **SQL query**.
- Retrieve and display **query results** from the database.
- **Interactive UI** built with Streamlit.

## 🔧 Installation
### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-username/text-to-sql-chatbot.git
cd text-to-sql-chatbot
```

### **Step 2: Install Dependencies**
Make sure you have Python 3.8+ installed, then run:
```bash
pip install streamlit pandas sqlite3 openpyxl torch transformers
```

### **Step 3: Run the Application**
```bash
streamlit run app.py
```

## 🎮 Usage
1. **Upload an Excel file** using the sidebar.
2. **Enter a question** (e.g., "What is total cost?") in the text box.
3. Click **Generate SQL Query**.
4. View the **generated SQL query** and **query results**.

## 🏗️ Example Prompts
- `What is item?`
- `What is total cost?`
- `What is all cost?`
- `What is cost?`
- `What is profit?`
- `what is total profit?`

