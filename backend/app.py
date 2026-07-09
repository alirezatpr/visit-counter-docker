from flask import Flask, jsonify, request
from flask_cors import CORS
import redis
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# اتصال به Redis
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379,
    decode_responses=True
)

# اتصال به PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'database'),
        database=os.getenv('DB_NAME', 'visitdb'),
        user=os.getenv('DB_USER', 'admin'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    return conn

# ساخت جدول اگر وجود نداره
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                ip_address VARCHAR(50),
                visit_time TIMESTAMP,
                visit_count INTEGER
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/api/visit', methods=['GET'])
def visit():
    try:
        # افزایش شمارنده در Redis
        visit_count = redis_client.incr('visit_counter')
        
        # دریافت IP کاربر
        ip_address = request.remote_addr
        
        # ذخیره در PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO visits (ip_address, visit_time, visit_count) VALUES (%s, %s, %s)',
            (ip_address, datetime.now(), visit_count)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'visit_count': visit_count,
            'ip': ip_address,
            'message': f'You are visitor number {visit_count}!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
