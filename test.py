import sys
import time

def main():
   """
   Program to enumerate all fixed polyominos of order n.
   Revision 4. 
   """

   # Read n from command line.  Display usage and exit on illegal input. 
   try:
      n = int(sys.argv[1])
   except:
      usage()
   if n < 1:
      usage()

   # Mark start time
   start = time.time()

   # Copy normalized polyominos into a set to eliminate duplicates. 
   polyomino_set = {normalize(p) for p in polyominos(n)}

   # Convert set to a list, and sort in canonical order. 
   result = sorted(list(polyomino_set))

   # Measure elapsed time
   elapsed_time = time.time() - start

   # Print results.
   target = ((0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2))
   line = 1
   print(f"")
   print(f"Results:")
   for poly in result:
      print(f"{line:7}\t{poly}")
      print(f"")
      graph(poly)
      print(f"")
      line += 1
      if poly == target:
         break

   print(f"\tnumber of {prefix(n)}ominos = {len(result)}")
   print(f"\telapsed time = {elapsed_time:.3} seconds")

def usage():
   print(f"usage: python {sys.argv[0]} polyomino-order")
   sys.exit("")
   
def prefix(n):
   """
   Function to provide "omino" names
   """
   if n <= 12:
      pre = ["0-", "mon", "d", "tri", "tetr", "pent", "hex", "hept", "oct", "non", "dec", "undec", "dodec"][n]
   else:
      pre = f"{n}-"
   return pre

def polyominos(n):
   """
   Helper function to kick off polyomino generator with single cell seed
   """
   seed_poly = {(0, 0)}   # any pair works
   yield from polyominos_recursive(n, seed_poly )

def polyominos_recursive(n, poly):
   """
   Recursive generator of polyominos of order n.
   """
   if n == 1: 
      yield poly
   else:
      puffy = poly.copy()
      for cell in list(poly):
         x, y = cell
         puffy.add((x+1, y))
         puffy.add((x-1, y))
         puffy.add((x, y+1))
         puffy.add((x, y-1))
      hull = puffy - poly
      for cell in list(hull):
         new_poly = poly.copy()
         new_poly.add(cell)
         yield from polyominos_recursive(n-1, new_poly)

def normalize(polyomino):
   """
   Normalization function to position polyomino in the upper-left-hand-most
   position in row, column space.  Within the polyomino, cells are forced 
   into a canonical order for ease of comparison with other polyominos. 
   Returns a tuple of (row, column) pairs for ease of use in a set. 
   """
   n = len(polyomino)
   xmin, ymin = n, n
   for cell in polyomino:
      x, y = cell
      xmin = min(x, xmin)
      ymin = min(y, ymin)

   new_polyomino = []
   for cell in polyomino:
      x, y = cell
      xnorm, ynorm = x - xmin, y - ymin
      new_cell = (xnorm, ynorm)
      new_polyomino.append(new_cell)

   new_polyomino.sort(key = lambda x:n*x[0]+x[1])
   return tuple(new_polyomino)

def graph(poly):
   """
   Prints a text representation of polyomino. 
   """
   n_rows = max([row for (row, col) in poly]) + 1
   n_cols = max([col for (row, col) in poly]) + 1
   for row in range(n_rows):
      print(f"\t", end="")
      for col in range(n_cols):
         cell = (row, col)
         graphic = "#" if cell in poly else " "
         print(f"{graphic} ", end="")
      print(f"")

main()
