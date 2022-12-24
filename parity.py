import functools

def ibmcmp1(f,g):
   (a,b), (c,d) = f, g
   if f == g:
      return 0
   if a < c  or  (a == c) and (b > d):
      return -1
   else:
      return 1

def ibmcmp2(f,g):
   (a,b), (c,d) = f, g
   if f == g:
      return 0
   if b < d  or  (b == d) and (a < c):
      return -1
   else:
      return 1

def perm(poly):
   print(poly)
   s1 = sorted(poly, key=functools.cmp_to_key(ibmcmp1))
   s2 = sorted(poly, key=functools.cmp_to_key(ibmcmp2))
   print(f"{s1 = }")
   print(f"{s2 = }")
   p = [s1.index(x) for x in s2]
   return p

def parity(perm):
   p = 0
   seen = [False]*len(perm)
   while not all(seen):
      print(seen)
      i = seen.index(False)
      print(i)
      count = 1
      # seen[i] = True
      while not seen[i]:
         j = perm[i]
         seen[i] = True
         count += 1
         i = j
      p ^= (count - 1) & 1
   return p


# poly = ( (0,1), (1,1), (1,2), (1,3), (2,0), (2,1), (3,1), (3,2), (3,3) )
poly = ( (0,1), (0,2), (0,3), (1,0), (1,1), (2,1), (2,2), (2,3), (3,1) )
p = perm(poly)
print(p)
print(parity(p))
sys.exit()