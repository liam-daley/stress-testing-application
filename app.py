import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Call redis method with 5 retries
def retry(cache_function):
    retries = 5
    while True:
        try:
            return cache_function()
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# Check if the number is in redis cache
def in_redis(number):
    return retry(lambda: cache.hexists("prime_numbers", number))

# Store the number in redis cache
def store_number_in_redis(number):
    retry(lambda: cache.hset("prime_numbers", number, number))

# Check if number is prime
def is_prime_number(number):
    #sys.maxint
    if in_redis(number):
       return True
    if number > 1:
        for i in range(2,number):
            if (number % i) == 0:
                return False;
                break
            else:
                store_number_in_redis(number)
                return True;
    else:
        return False
    

# Check if number is prime and return appropriate message
@app.route('/isPrime/<number>')
def check_number(number):
    #try:
    number = int(number)
    if is_prime_number(number):
        return "%d is prime" % number
    return "%d is not prime" % number
    #except:
        #pass

# Returns a list with all the primes stored in the connected Redis service
@app.route('/primesStored')
def get_prime_numbers():
    return str([int(key) for key in retry(lambda: cache.hkeys("prime_numbers"))])
