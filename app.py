import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# TODO Check if the number is in redis
def in_redis(number):
    return False

# TODO Store the number in redis
def store_number_in_redis(number):
    return "stored the number"

# Check if number is prime
def is_prime_number(number):
    #if in_redis(number):
    #   return true
    # Check if prime number
    #sys.maxint
    if number > 1:
        for i in range(2,number):
            if (number % i) == 0:
                return False;
                break
            else:
                #store_number_in_redis(number)
                return True;
    else:
        return False
    

# Checks if number is prime and returns appropriate message
@app.route('/isPrime/<number>')
def check_number(number):
    #try:
    number = int(number)
    if is_prime_number(number):
        return "%d is prime" % number
    return "%d is not prime" % number
    #except:
        #pass

# TODO Returns a list with all the primes stored in the connected Redis service
@app.route('/primesStored')
def get_prime_numbers():
    return "all prime numbers"
