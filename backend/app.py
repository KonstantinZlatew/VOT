from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, count INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row:
        count = row[0] + 1
        cursor.execute('UPDATE users SET count = ? WHERE username = ?', (count, username))
    else:
        count = 1
        cursor.execute('INSERT INTO users (username, count) VALUES (?, ?)', (username, count))
    conn.commit()
    conn.close()
    return jsonify({'username': username, 'count': count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
