from flask import Flask, jsonify
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

@app.route('/read/beanstalkd', methods=['GET'])
def read_beanstalkd():
    try:
        job = beanstalk.reserve(timeout=1)
        if job:
            message = job.body
            job.delete()
            return jsonify({'status': 'success', 'queue': 'beanstalkd', 'message': message})
        else:
            return jsonify({'status': 'empty', 'queue': 'beanstalkd'})
    except Exception as e:
        return jsonify({'status': 'error', 'queue': 'beanstalkd', 'error': str(e)})

@app.route('/read/redis_rdb', methods=['GET'])
def read_redis_rdb():
    message = redis_rdb.rpop('queue_rdb')
    if message:
        return jsonify({'status': 'success', 'queue': 'redis_rdb', 'message': message.decode('utf-8')})
    else:
        return jsonify({'status': 'empty', 'queue': 'redis_rdb'})

@app.route('/read/redis_aof', methods=['GET'])
def read_redis_aof():
    message = redis_aof.rpop('queue_aof')
    if message:
        return jsonify({'status': 'success', 'queue': 'redis_aof', 'message': message.decode('utf-8')})
    else:
        return jsonify({'status': 'empty', 'queue': 'redis_aof'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
