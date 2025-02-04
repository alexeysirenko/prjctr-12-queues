from flask import Flask, request, jsonify
import beanstalkc
import redis
import os

app = Flask(__name__)

# Get connection settings from environment or use defaults
BEANSTALKD_HOST = os.environ.get("BEANSTALKD_HOST", "beanstalkd")
BEANSTALKD_PORT = int(os.environ.get("BEANSTALKD_PORT", 11300))

REDIS_RDB_HOST = os.environ.get("REDIS_RDB_HOST", "redis-rdb")
REDIS_RDB_PORT = int(os.environ.get("REDIS_RDB_PORT", 6379))

REDIS_AOF_HOST = os.environ.get("REDIS_AOF_HOST", "redis-aof")
REDIS_AOF_PORT = int(os.environ.get("REDIS_AOF_PORT", 6379))

# Initialize connections
beanstalk = beanstalkc.Connection(host=BEANSTALKD_HOST, port=BEANSTALKD_PORT)
redis_rdb = redis.Redis(host=REDIS_RDB_HOST, port=REDIS_RDB_PORT)
redis_aof = redis.Redis(host=REDIS_AOF_HOST, port=REDIS_AOF_PORT)

@app.route('/write/beanstalkd', methods=['POST'])
def write_beanstalkd():
    data = request.get_json() or {}
    message = data.get('message', 'Hello from beanstalkd')
    # Put the message in the default tube
    beanstalk.put(message)
    return jsonify({'status': 'success', 'queue': 'beanstalkd', 'message': message})

@app.route('/write/redis_rdb', methods=['POST'])
def write_redis_rdb():
    data = request.get_json() or {}
    message = data.get('message', 'Hello from redis rdb')
    # Push the message onto a Redis list called 'queue_rdb'
    redis_rdb.lpush('queue_rdb', message)
    return jsonify({'status': 'success', 'queue': 'redis_rdb', 'message': message})

@app.route('/write/redis_aof', methods=['POST'])
def write_redis_aof():
    data = request.get_json() or {}
    message = data.get('message', 'Hello from redis aof')
    # Push the message onto a Redis list called 'queue_aof'
    redis_aof.lpush('queue_aof', message)
    return jsonify({'status': 'success', 'queue': 'redis_aof', 'message': message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
