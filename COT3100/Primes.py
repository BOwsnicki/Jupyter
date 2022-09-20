#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Styling notebook
from IPython.core.display import HTML
def css_styling():
    styles = open("./styles/custom.css", "r").read()
    return HTML(styles)
css_styling()


# ### Prime numbers
# 
# Prime numbers are some of the most "elementary" integers in the sense that any integer is somehow composed of primes. They also play a decisive role in today's cryptography - generally since they facilitate "complete arithmetic" by allowing all four arithmetic operations (addition, subtraction, multiplication and division) when used creatively.
# 
# There are a lot of questions as far as prime numbers are concerned:
# - Are the infinitely many? (Yes)
# - How can I find out if a number is prime? (It's complicated)
# - How can I generate prime numbers? (Also complicated, but there is a simple way that just takes a lot of time)
# 
# Testing if a number is prime is not overly important for the rest of this module, so it's going to be skipped for the moment. In case you're curious please refer to the "Miller-Rabin" section.
# 
# We start with the last problem which has a solution dating back to around 200 B.C.
# 
# **Prime Generation with the "Sieve of Eratosthenes"**  
# 
# A relatively simple iterative process, that starts with a list of integers and successively crosses out all composite numbers up to a given value $n:$
# 
# 1. Start with $k=2.$ In the next steps find the next $k$ that is not crossed out (that's a prime)
# 1. If $k > \sqrt{n},$ we're done - nothing more to cross out
# 1. Cross out all multiples of $k$ up to the limit $n.$
# 1. Find the next $k$ that is not crossed out (that's a prime) and continue with that.
# 
# Standard implementation over a boolean array (**True** means "it's a prime"). Initialize to all **True** and set any multiple of $k$ to **False**. What remains **True** to the end are the primes.

# In[4]:


def sieve(n) :
    sieve = [True for i in range(n + 1)]
    k = 2
    while (k * k <= n):        
        # Find next prime - mark all multiples as not prime
        if (sieve[k]) :
            for i in range(k*k, n + 1, k):
                sieve[i] = False
        k += 1

    # Collect/return primes off the sieve
    primes = []
    for p in range(2, n+1):
        if sieve[p] :
            primes.append(p)
    return primes


# In[32]:


print(sieve(2000))


# **Pick a random prime out of the list**  
# 
# Not quite as easy as it looks, since we need to pick them in a particular way to make brute force attempts difficult. They should be away from the "sides" of the interval so they cannot be found by exhaustive search from either side - but they shouldn't be too close together.
# 
# Also, the random number generators in normal programming languages are (at least theoretically) predictable - we don't want that. Cryptographically acceptable random numbers are tough to generate!!

# In[6]:


primesList = sieve(250000)


# In[7]:


import random

def randomPrime(primes, start = 1) :
    index = random.randrange(start,len(primes)) - 1
    return primes[index + start - 1]


# In[29]:


randomPrime(primesList)

