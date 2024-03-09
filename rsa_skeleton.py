#Matthew Kearney - RSA 

import random
import math

# For the lab, complete modexp(), RSA_enc(), and RSA_dec().
# HW 2 will allow you to submit the fully completed code from the lab,
#   as well as egcd(), mulinv(), and keygen(), for HW2
#   
# You must work independently since this assignment will be part of HW 2.

# test constants
test_p = 23
test_q = 47
test_e =  35
test_d = 347
message = "Hello world!ÿ" 

def calc_n(p, q):
    # do not modify!
    return p * q

def calc_phi(p, q):
    # do not modify!
    return (p - 1) * (q - 1)

def modexp(b, e, m):
    # returns b^e % m efficiently
    # use the binary modular exponentiation algorithm explained in the lab slides
    # Complete this part during the lab
    if m==1:
        return 0
    # assert((m-1)*(m-1)<= b)
    result = 1
    # b = b % m
    if (type(b)==int):
        b = b % m
    else:
        b = int(b, 2) % m
    # if (type(e)!=int):
    #     e = int(e, 2)
    while e > 0:
        if(e % 2 == 1):
            result = (result * b) % m
        e = e >> 1
        b = b**2 % m
    return result

#padding each representation to size 8 ~ UTF-8
def pad(binary, size):
    zero = '0'
    while(len(binary) < size):
        new = zero + binary 
        binary = new
    return binary


def RSA_enc(plaintext, key):
    # key should be a tuple (n, e)
    # the ord() function will be useful here
    # we recommend extracting the components of the key from the tuple for efficiency purposes
    # return a list of integers
    # Complete this part during the lab
    n, e = key
    result = []
    
    #a. convert plaintext to byte representation (8-bit/1 byte)
    for i in plaintext:
        ch = i
        result.append(pad(bin(ord(ch))[2:], 8))
        
    #b. for each converted a in plaintext 
    C = []
    for a in result:
        c=modexp(a, e, n)
        C.append(c)
    return C

def RSA_dec(ciphertext, key):
    # key should be a tuple (n, e)
    # the chr() function will be useful here
    # we recommend extracting the components of the key from the tuple for efficiency purposes
    # return a string
    # Complete this part during the lab
    n, e = key
    A = []
    for c in ciphertext:
        a = modexp(c, e, n)
        A.append(a)

    result = ''
    for a in A:
        result = result + chr(a)
    return result

def test():
    # do not modify!
    n       = calc_n(test_p, test_q)
    private = [n, test_d]
    public  = [n, test_e]
    
    print("Public key:",public)
    print("Private key:",private)
    
    ciphertext = RSA_enc(message,public)
    # print(ciphertext)
    plaintext  = RSA_dec(ciphertext,private)

    print("Original message:",message)
    print("Encrypted message:",ciphertext)
    print("Decrypted message:",plaintext)

# === Below this comment is the portions of this assignment that contribute to HW 2 ===

def egcd(b, n):
    # runs the extended Euclidean algorithm on b and n
    # returns a triple (g, x, y) s.t. bx + ny = g = gcd(b, n)
    # review the extended Euclidean algorithm on Wikipedia
    # Complete for HW 2 
    a = b 
    b = n
    (old_r, r) = (a,b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
        quotient = old_r // r
        (old_r, r) = (r, old_r - (quotient*r))
        (old_s, s) = (s, old_s - (quotient*s))
        (old_t, t) = (t, old_t - (quotient*t))
    return (old_r, old_s, old_t)


def mulinv(e, n):
    # returns the multiplicative inverse of e in n
    # make use of the egcd above
    # Complete for HW 2 
    print(e,n)
    (g, x, y) = egcd(e, n)
    print(g)
    if g != 1:
        raise ValueError("The inverse does not exist")
    else:
        return x % n

def checkprime(n, size):
    # do not modify!
    # determine if a number is prime
    if n % 2 == 0 or n % 3 == 0: return False
    i = 0

    # fermat primality test, complexity ~(log n)^4
    while i < size:
        if modexp(random.randint(1, n - 1), n - 1, n) != 1: return False
        i += 1

    # division primality test
    i = 5
    while i * i <= n:
        if n % i == 0: return False
        i += 2
        if n % i == 0: return False
        i += 4
    return True

def primegen(size):
    # do not modify!
    # generates a <size> digit prime
    if(size == 1): return random.choice([2, 3, 5, 7])
    lower = 10 ** (size - 1)
    upper = 10 ** size - 1
    p = random.randint(lower, upper)
    p -= (p % 6)
    p += 1
    if p < lower: p += 6
    elif p > upper: p -= 6
    q = p - 2
    while p < upper or q > lower:
        if p < upper:
            if checkprime(p, size): return p
            p += 4
        if q > lower:
            if checkprime(q, size): return q
            q -= 4
        if p < upper:
            if checkprime(p, size): return p
            p += 2
        if q > lower:
            if checkprime(q, size): return q
            q -= 2
        

def keygen(size):
    # generate a random public/private key pair
    # size is the digits in the rsa modulus, approximately. must be even, >2
    # return a tuple of tuples, [[n, e], [n, d]]
    # Complete this for HW 2 
    p = primegen(size)
    q = primegen(size)
    while(p==q):
        q = primegen(size)

    n = p*q
    totient= (p-1)*(q-1)

    e = random.randint(2, totient - 1)
    while math.gcd(e, totient) != 1:
        e = random.randint(2, totient - 1)

    d = mulinv(e, totient)

    assert(size % 2 == 0 and size > 2) # keep this line!
    return ((n, e),(n, d))

def customkeytest(text, size):
    keypair = keygen(size)
    
    print("Public key:",keypair[0])
    print("Private key:",keypair[1])
    
    ciphertext = RSA_enc(text,keypair[0])
    plaintext  = RSA_dec(ciphertext,keypair[1])

    print("Original message:",text)
    print("Encrypted message:",ciphertext)
    print("Decrypted message:",plaintext)

test()
customkeytest(message, 8)