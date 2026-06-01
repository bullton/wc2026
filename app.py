from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from database import init_db

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

def get_db_connection():
    conn = sqlite3.connect('worldcup.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/matches', methods=['GET'])
def get_matches():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    year = request.args.get('year', '2026')
    cursor.execute('''
        SELECT * FROM matches 
        WHERE match_date LIKE ?
        ORDER BY match_date, match_time
    ''', (f'{year}-%',))
    
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(matches)

@app.route('/api/matches/<date>', methods=['GET'])
def get_matches_by_date(date):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM matches 
        WHERE match_date = ?
        ORDER BY match_time
    ''', (date,))
    
    matches = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(matches)

@app.route('/api/groups', methods=['GET'])
def get_groups():
    groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    return jsonify(groups)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
