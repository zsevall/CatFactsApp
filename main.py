import requests
import sqlite3


def fetch_cat_facts(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def create_database(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cat_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fact TEXT,
                    length INTEGER
                )''')
    conn.commit()


def insert_facts(conn, facts):
    c = conn.cursor()
    for fact in facts['data']:
        c.execute('''INSERT INTO cat_facts (fact, length) VALUES (?, ?)''',
                  (fact['fact'], fact['length']))
    conn.commit()


def display_facts(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM cat_facts')
    rows = c.fetchall()
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
