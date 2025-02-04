1. **Build and Start the Containers:**

   Run the following command in the project root directory:

   ```bash
   docker-compose up --build
   ```

2. **Test the Endpoints:**

   - **Writer Endpoints (POST requests with JSON payload):**

     - **beanstalkd:** `http://localhost:5000/write/beanstalkd`
     - **redis-rdb:** `http://localhost:5000/write/redis_rdb`
     - **redis-aof:** `http://localhost:5000/write/redis_aof`

     _Example using curl:_

     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello from beanstalkd"}' http://localhost:5000/write/beanstalkd
     ```

   - **Reader Endpoints (GET requests):**
     - **beanstalkd:** `http://localhost:5001/read/beanstalkd`
     - **redis-rdb:** `http://localhost:5001/read/redis_rdb`
     - **redis-aof:** `http://localhost:5001/read/redis_aof`

3. **Run Performance Tests with Siege:**

   The `siege` directory contains three files to test the performance of each queue system. For example, to run a test for beanstalkd:

   ```bash
   siege -f siege/beanstalkd.siege
   siege -f siege/redis_rdb.siege
   siege -f siege/redis_aof.siege
   ```
