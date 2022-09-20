#!/usr/bin/env python
# coding: utf-8

# ### Applications of RSA
# 
# **Identification of an individual by challenging the RSA key**  
#   
# Satoshi and Craig (say!) are two different persons, each with their own RSA key pair  
# Everyone knows Satoshi's public key (by calling getPublic(), no problem)  
# Craig pretends to be Satoshi
#   
# We pick a secret, encrypt it with Satoshi's public key  
# Let both decrypt it and see who's doing it right  
#   
# *Ignore the signString method for the moment - we'll deal with it in the second example*

# In[2]:


from RSA import Key, KeyPair
from Modular import fastExpMod
import random

class Person :
    def __init__(self):
        self._rsaKeys = KeyPair()
        
    def getPublic(self):
        return self._rsaKeys.public
    
    def decrypt(self, message):
        return self._rsaKeys.decrypt(message)
    
    def signString(self,string) :
        return string, self.decrypt(len(string)) # same as encrypt with the private key
    

# Satoshi is the "true" one and we know the public key
satoshi = Person()
satoshiKey = satoshi.getPublic()
print("I know the public key of Satoshi: ",satoshiKey)

# Craig says he's Satoshi - so, we don't need his public key, 
# he would give us Satoshi's public key anyway (everyone knows it)
craig = Person()

# We can find out who the real Satoshi is by
# 1. picking a secret message "secret"
# 2. encrypting it with Satoshi's public key
# 3. and asking both to decrypt it
#
# Only the "true" Satoshi will do that correctly!
#
secret = 1234

# Use P1's public key to encrypt the secret
challenge = fastExpMod(secret,satoshiKey.second,satoshiKey.first)
print("Challenging with",challenge)

# Let both decrypt it ==> We know who is Satoshi (the one answering with the secret)
print(satoshi.decrypt(challenge))
print(craig.decrypt(challenge))


# **Sketch of digital signatures**
# 
# That relies on the fact that you can *use your private key to encrypt* and *your public key to 
# decrypt* (opposite of normal, but we know that works)  
#   
# So P1 computes a property of the message (like a hash code, here it's just the length), and encrypts it with the *private* (!) key - that's the whole trick!  
# 
# The receiver can now use P1's public key to check this property and validate that P1 really signed it

# In[3]:


# Two persons with their RSA keys, public parts are known
p1 = Person()
p1Key = p1.getPublic()
p2 = Person()
p2Key = p2.getPublic()

# Now P1 signs this string with length 13 encrypted with the private (!) key
# So, the encrypted length of the string is the digital signature!
string, signature = p1.signString("Hello, world!")
print("String =",string,"Signature =",signature)

# Now decrypt the signature with each of the public keys
length1 = fastExpMod(signature,p1Key.second,p1Key.first)
length2 = fastExpMod(signature,p2Key.second,p2Key.first)
# And the authenticity is clear
print("Decrypted with P1's public key:",length1,
      " \t\tAuthentic: ",len(string) == length1)
print("Decrypted with P2's public key:",length2,
      " \tAuthentic: ",len(string) == length2)


# **Now we need some moment to clarify something about this text property**  
# 
# I used the length of the string as the property - for simplification purposes!  
# 
# Now, that means that an evil person could abuse this scheme:  
# 1. Intercept the string with the signature
# 1. Replace the string with another one of the same length
#   
# This string would now appear as being signed by P1, but it's not the authentic string anymore:  
# A string "Attack at dawn" could now be replaced with "Attack at noon" (note that "Attack at night" wouldn't work!) with possibly devastating consequences.
#   
# In fact, this scheme allows for signing, but doesn't preserve authenticity!
# 
# In practice these things go hand in hand, so we need to find a string property that's not easy to fake.  
# 
# **Hashing (More in "Algorithms and Data Structures")**  
# 
# Hashing means to assign to a data object a numerical value. Different data objects might or might not have different values. The data object itself cannot be reconstructed from this value.  
# 
# Actually, the length is a kind of such a hash value, it's just not good enough to protect against faking. Strong hash values make it practically impossible to find a string that has the same hash value as the authentic one. It's practically impossible to learn anything about the string given a strong hash:
# 

# In[4]:


import hashlib

hash_object = hashlib.sha256(b'John')
hex_dig = hash_object.hexdigest()
print(hex_dig)

hash_object = hashlib.sha256(b'Joan')
hex_dig = hash_object.hexdigest()
print(hex_dig)

hash_object = hashlib.sha256(b'There now is your insular city of the Manhattoes, belted round by wharves as Indian isles by coral reefs - commerce surrounds it with her surf.')
hex_dig = hash_object.hexdigest()
print(hex_dig)


# You can use hash values to encode passwords:  
# 1. Compute the hash for the password during sign-up
# 2. For each login attempt compute the hash of the provided password and compare it to the sign-up version
#   
# Note that this is **not** foolproof, since there are definitely many strings that have the same hash code. An attacker would not have to find the correct password but any string with the same hash - that's all. These strings are called *collisions* and an attack trying to find a suiting string is called a <a href="https://en.wikipedia.org/wiki/Collision_attack">*collision attack*</a>.

# In[8]:


import hashlib

password = 's3cr3t' # terrible password
hash_object = hashlib.sha256(password.encode('utf8'))
hex_dig_original = hash_object.hexdigest()
print(hex_dig_original)
attempt = 's3cr3t' # another terrible password
hash_object = hashlib.sha256(attempt.encode('utf8'))
hex_dig_attempt = hash_object.hexdigest()
print(hex_dig_attempt)
if hex_dig_original == hex_dig_attempt : 
    print("accepted!")
else :
    print("rejected!")


# We "improve" the previous example with a weak hash that just adds the decimal value of the characters together. It's still weak, but it makes it much more difficult to sneak an unauthenticated replacement in - it needs to have the same "hash", not be complete gibberish and express something malicious.  
# 
# The reason I'm not using SHA here is that this toy implementaion of RSA cannot handle numbers that big. You certainly can work around that, by encrypting the string character character and somehow magically appending this into a value. 

# In[11]:


class SecurePerson (Person):
    @classmethod
    def hashStringBadly(cls,string) :
        sum = 0
        for c in string :
            sum += ord(c)
        return sum
    
    def signString(self,string) :
        return string, self.decrypt(SecurePerson.hashStringBadly(string)) # same as encrypt with the private key
    
# Same with safe persons:
p1 = SecurePerson()
p1Key = p1.getPublic()
p2 = SecurePerson()
p2Key = p2.getPublic()

string, signature = p1.signString("Hello, world!")
print("String =",string,"Signature =",signature)

# Now decrypt the signature with each of the public keys
hash1 = fastExpMod(signature,p1Key.second,p1Key.first)
hash2 = fastExpMod(signature,p2Key.second,p2Key.first)
# And the authenticity is clear
print("Decrypted with P1's public key:",hash1,
      " \t\tAuthentic: ",SecurePerson.hashStringBadly(string) == hash1)
print("Decrypted with P2's public key:",hash2,
      " \tAuthentic: ",SecurePerson.hashStringBadly(string) == hash2)


# ## A look at the standard RSA package in Python  
# 
# Nothing too special, one little thing that's not textbook: Public and private key are NOT interchangeable! The reason is (I assume) that the decryption method checks if the cyphertext has been properly encrypted with the public key (which is a part of the private key, if I see that correctly).  
# 
# That means you cannot really use it for Digital Signatures the way it was sketched, requiring a separate functionality to do that.

# In[13]:


import rsa

# Basic RSA encryption/decryption

# Key pair generation
(pubkey, privkey) = rsa.newkeys(2048)
print(pubkey,"\n",privkey,"\n\n")

# Encryption/Decryption
message = 'Hello, World!'.encode('utf8')
crypto = rsa.encrypt(message, pubkey)
print("Cyphertext:",crypto)
decrypt = rsa.decrypt(crypto, privkey)
print(message.decode('utf8'),"\n\n")

# Digital signature is extra, because (apparently) public and private key are not interchangeable
# Important is that the message is signed with the private key (as it should)
signature = rsa.sign(message, privkey, 'SHA-256')

# Verify with the public key!
print("Signature:",signature,"\nVerified as",rsa.verify(message, signature, pubkey))

# Wrong signature: Have to catch the exception (OHHH-KAYYY)
signature = "12345".encode('utf-8')
try:
    print("Signature:",signature,"\nVerified as",rsa.verify(message, signature, pubkey))
except rsa.VerificationError:
    print("Invalid signature")


# **Here's the improved Person - not a subclass, since it redefines everything**

# In[15]:


import rsa

class SecurestPerson :
    def __init__(self):
        (self._pubkey, self._privkey) = rsa.newkeys(2048)
        
    def getPublic(self):
        return self._pubkey
    
    def decrypt(self, message):
        return rsa.decrypt(message,self._privkey)
    
    def signString(self,string) :
        return string, rsa.sign(string, self._privkey, 'SHA-256')


# **That's now the Satoshi example again**  
# 
# Slightly recoded to fit the RSA API

# In[16]:


import rsa

# Satoshi
satoshi = SecurestPerson()
satoshiKey = satoshi.getPublic()
print("I know the public key of Satoshi: ",satoshiKey)

# Craig
craig = SecurestPerson()

# Secret message
secret = "1234".encode('utf8')

# Use P1's public key to encrypt the secret
challenge = rsa.encrypt(secret, satoshiKey)
print("Challenging with",challenge)

# Let both decrypt it ==> We know who is Satoshi (the one answering with the secret)
try:
    print(satoshi.decrypt(challenge).decode('utf8'))
except rsa.DecryptionError :
    print("Satoshi cannot decrypt!")
try:
    print(craig.decrypt(challenge).decode('utf8'))
except rsa.DecryptionError :
    print("Craig cannot decrypt!")

