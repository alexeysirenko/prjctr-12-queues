1. **Build and Start the Containers:**

   Run the following command in the project root directory:

   ```bash
   docker-compose up --build -d
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
   siege --content-type "application/json" -f siege/beanstalkd.siege -t30s -c100
   siege --content-type "application/json" -f siege/redis_aof.siege -t30s -c100
   siege --content-type "application/json" -f siege/redis_rdb.siege -t30s -c100
   ```

   **Test Results (number of transactions per 30 seconds)**
   | | 10 users | 100 users |
   |:----------------|:----------------:|:----------------:|
   |Beanstalk |12917 | 14491 |
   |Redis append only (save on every write)| 21612 | 18806 |
   |Redis snapshots (save every 10 seconds) | 19768 | 21413 |
