#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Styling notebook
from IPython.core.display import HTML
def css_styling():
    styles = open("./styles/custom.css", "r").read()
    return HTML(styles)
css_styling()


# ### Circular (rotation) substitution cypher  
# 
# A substitution cypher replaces any character (or sequence of characters) by another one. The easiest are the ones that rotate characters by a certain offset. In order to deal with overflows, they just use remainders mod a given number.
# 
# In this examples we're using just lowercase characters mod 26, since this allows us to cover all 26 characters without any problems.

# **Rotate character 'c' by integer n mod 26**

# In[3]:


def rotN(c,n) :
    if not (c.islower()) : return c
    base = ord(c) - ord('a') # a = 0, b = 1, ...
    code = (base + n) % 26
    return chr(ord('a') + code)


# In[9]:


rotN('u',13) # try n = 13 ;-)
# https://en.wikipedia.org/wiki/ROT13


# In[5]:


def rotStringN(s,n) :
    return ''.join(map(lambda c : rotN(c,n),s))


# In[6]:


string = 'abcdefghijklmnopqrstuvwxyz'
print(string)
print(rotStringN(string,9))

# Behold! The magic of rot13
print(rotStringN(rotStringN('hello',13),13))


# ### Simple letter counting class  
# Just counts lowercase letters, nothing else  
# So, it converts the string to lowercase to begin with

# In[7]:


class Histogram :
    def __init__(self, string):
        self.freq = {} # That's a dictionary
        for c in string.lower() :
            self.incrementFreq(c)
            
    def incrementFreq(self,c) :
        if c.islower() :
            oldV = self.freq.get(c,None)  # lazy increment
            if oldV is None : oldV = 0
            self.freq[c] = oldV + 1 


# ### Sample run with a given text (Moby Dick)
# 1. Rotate with an abitrary n  
# 2. Run statistics over the cypher string
# 3. Pick the most common letter
# 4. Assume it's an 'e' and rotate back

# In[8]:


# Original text (copied and pasted, so it looks funny)
text = 'Call me Ishmael Some years ago never mind how long precisely having little or no money in my purse and nothing particular to interest me on shore I thought I would sail about a little and see the watery part of the world It is a way I have of driving off the spleen and regulating the circulation Whenever I find myself growing grim about the mouth; whenever it is a damp drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me that it requires a strong moral principle to prevent me from deliberately stepping into the street and methodically knocking people’s hats off—then I account it high time to get to sea as soon as I can This is my substitute for pistol and ball With a philosophical flourish Cato throws himself upon his sword; I quietly take to the ship There is nothing surprising in this If they but knew it almost all men in their degree some time or other cherish very nearly the same feelings towards the ocean with me'.lower()

# Change this to play with different n values
rot = rotStringN(text,17)
print(rot)

# Run statistics
h = Histogram(rot)
l = sorted(h.freq.items(),key=lambda item: -item[1]) # Sort result descending

# l[0][0] is the character (key) in the first result tuple

# So, that's the new n to rotate back:
rotBack = ord('e') - ord(l[0][0])

# and here we go!
rotStringN(rot,rotBack)


# In[ ]:




