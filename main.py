import requests
import sqlite3


def fetch_cat_facts(api_url):
    """
    Fetches cat facts from the given API URL.

    Args:
        api_url (str): The URL of the cat facts API.

    Returns:
        dict: A dictionary containing the fetched cat facts, or None if an error occurred.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def create_database(conn):
    """
    Creates the cat_facts table in the SQLite database if it does not exist.

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
    """
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS cat_facts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            fact TEXT,
                            length INTEGER
                        )''')


def insert_facts(conn, facts):
    """
    Inserts fetched cat facts into the cat_facts table.

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
        facts (dict): A dictionary containing the fetched cat facts.
    """
    with conn:
        conn.executemany('''INSERT INTO cat_facts (fact, length) VALUES (?, ?)''',
                         [(fact['fact'], fact['length']) for fact in facts['data']])


def display_facts(conn):
    """
    Displays all cat facts stored in the cat_facts table.

    Args:
        conn (sqlite3.Connection): The SQLite database connection.
    """
    with conn:
        for row in conn.execute('SELECT * FROM cat_facts'):
            print(row)


def main():
    """
    The main function that orchestrates fetching, storing, and displaying cat facts.
    """
    api_url = "https://catfact.ninja/facts"
    data = fetch_cat_facts(api_url)

    if data:
        with sqlite3.connect('cat_facts.db') as conn:
            create_database(conn)
            insert_facts(conn, data)
            display_facts(conn)


if __name__ == "__main__":
    main()
