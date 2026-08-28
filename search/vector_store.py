import math,re
from collections import Counter
def _tokens(text): return re.findall(r"[a-z0-9_]+",text.lower())
def hashed_vector(text, dimensions=256):
    v=[0.0]*dimensions
    for token in _tokens(text):
        v[hash(token)%dimensions]+=1.0
    norm=math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/norm for x in v]
def cosine(a,b): return sum(x*y for x,y in zip(a,b))
def vector_score(query, text): return cosine(hashed_vector(query),hashed_vector(text))
