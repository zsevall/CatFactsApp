# CatFactsApp

## Overview
**CatFactsApp** is a Python application designed to fetch interesting cat facts from an API and store them in an SQLite database. The application also retrieves and displays the stored facts, making it a fun and educational project for learning about API integration, database handling, and data manipulation in Python. 

This project is part of a Upschool AI Developper course assignment.

## Features
- Fetches random cat facts from the [Cat Fact Ninja API](https://catfact.ninja/facts).
- Stores the fetched facts in an SQLite database.
- Retrieves and displays the stored cat facts in the terminal.

## Requirements
- Python 3.x
- `requests` library
- `sqlite3` library (included with Python)

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/CatFactsApp.git
   cd CatFactsApp
2. **Create a virtual environment (optional but recommended):**
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3.**Install the required packages:**
   pip install requests

## Usage
**1.Run the main application:**
python main.py

**2.Output:**
The application will fetch cat facts from the API, store them in the SQLite database, and display the stored facts in the terminal.

## Project Structure
CatFactsApp/

├── .venv/ # Virtual environment (optional)

├── cat_facts.db # SQLite database file

├── main.py # Main Python script

├── requirements.txt # List of required packages

└── README.md # Project documentation


## Code Explanation

### main.py
```python
import requests
import sqlite3

def fetch_cat_facts(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print('Failed to retrieve data')
        return []

def create_database(connection):
    with connection:
        connection.execute('''CREATE TABLE IF NOT EXISTS CatFacts (
                                id INTEGER PRIMARY KEY,
                                fact TEXT NOT NULL)''')

def insert_facts(connection, facts):
    with connection:
        connection.executemany('INSERT INTO CatFacts (fact) VALUES (?)', [(fact['fact'],) for fact in facts])

def display_facts(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM CatFacts')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def main():
    api_url = "https://catfact.ninja/facts"
    data = fetch_cat_facts(api_url)
    
    if data:
        conn = sqlite3.connect('cat_facts.db')
        create_database(conn)
        insert_facts(conn, data)
        display_facts(conn)
        conn.close()

if __name__ == "__main__":
    main()



