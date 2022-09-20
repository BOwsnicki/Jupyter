#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Styling notebook
from IPython.core.display import HTML
def css_styling():
    styles = open("./styles/custom.css", "r").read()
    return HTML(styles)
css_styling()


# ### Key Exchange (Diffie-Hellman) ###
# Alice and Bob publicly agree to use numbers $p = 23$ and $g = 5$ (fixed here)    
# Alice: chooses secret integer a, sends Bob $A = g^a\: {\rm mod}\: p$  
# Bob: chooses secret integer b, sends Alice $B = g^b\:  {\rm mod}\: p$  
# Alice: computes $s = B^a\: {\rm mod}\: p\: \leftarrow$ Shared secret  
# Bob: computes $s = A^b\:  {\rm mod}\: p\: \leftarrow$ Shared secret
# 
# Why? From Bob's side: $A^b {\rm mod}\; p = g^{ab} {\rm mod}\; p = g^{ba} {\rm mod}\; p = B^a {\rm mod}\; p$
# 

# In[1]:


import random
from Modular import fastExpMod

# Alice and Bob publicly agree to use numbers p = 23 and g = 5.
g = 5
p = 23
print('Alice and Bob agree on g =',g,'and p =',p)

# Alice: chooses secret integer a, sends Bob A = g^a mod p
a = random.randrange(3,100)
A = fastExpMod(g,a,p)
print('Alice sends A:',A)

# Bob: chooses secret integer b, sends Alice B = g^b mod p
b = random.randrange(3,100)
B = fastExpMod(g,b,p)
print('Bob sends B:',B)

# Alice: computes s = B^a mod p
sAlice = fastExpMod(B,a,p)
print('Alice knows',sAlice)

# Bob: computes s = A^b mod p
sBob = fastExpMod(A,b,p)
print('Bob knows',sBob)


# ## Breaking Diffie-Hellman ##
# Scenarion: An eavesdropper can only hear <span style="color:blue">g, p, A, B</span>. This is how the secret $s$ can be recomputed from that:
# 
# 1. Solve (for $b$) the *Discrete Logarithm Problem* <span style="color:blue">$B = g^b\: {\rm mod}\: p$</span> (or symmetric for $A = g^a\: {\rm mod}\: p$) 
# That's not as easy as it looks - we have a solution that uses brute force in the [Modular Notebook](Modular.ipynb#dlog).
# 1. Compute <span style="color:blue">$s = A^b\: {\rm mod}\: p$</span> with the $b$ you just found

# In[3]:


from Modular import fastExpMod, dLog

def breakDH(g,p,A,B) :
    return fastExpMod(A,dLog(g,p,B),p)


# In[4]:


breakDH(5,23,19,6)

