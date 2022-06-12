import sys
import time

def main():
   """
   Program to enumerate all fixed polyominos of order n.
   Revision 7.
   """

   # Read n from command line.  On illegal input, display usage and exit.
   try:
      n = int(sys.argv[1])
   except:
      usage()
   if n < 1:
      usage()

   # Mark start time
   start_time = time.time()

   # Copy normalized polyominos into a set to eliminate duplicates. 
   polyomino_set = {normalized(p) for p in polyominos(n)}

   # Convert set to a list, and sort in canonical order. 
   result = sorted(list(polyomino_set))

   # Mark stop time and measure elapsed time
   stop_time = time.time()
   elapsed_time = time.time() - start_time

   # Print results.
   line = 1
   print(f"")
   print(f"Results:")
   for poly in result:
      print(f"{line:7}\t{list(poly)}")
      print()
      graph(poly)
      print()
      line += 1

   print(f"\tnumber of {prefix(n)}ominos = {len(result)}")
   print(f"\telapsed time = {elapsed_time:0.3f} seconds")

def usage():
   """
   Display usage message and exit.
   """
   print(f"usage: python {sys.argv[0]} polyomino-order")
   sys.exit("")
   
def prefix(n):
   """
   Function to provide polyomino name prefixes
   """
   try:
      pre = ["poly", "mon", "d", "tri", "tetr", "pent", "hex", "hept", "oct", "non", "dec", "undec", "dodec"][n]
   except:
      pre = f"{n}-"
   return pre

def polyominos(n):
   """
   Helper generator to kick off recursive generator with single cell seed
   """
   seed_poly = {(0,0)}
   yield from polyominos_recursive(n, seed_poly )

def polyominos_recursive(n, poly):
   """
   Recursive generator of polyominos of order n.
   """
   if n == 1: 
      yield poly
   else:
      puffy = poly.copy()
      puffy.update(*[[(x+1,y), (x-1,y), (x, y+1), (x,y-1)] for (x, y) in poly])
      hull = puffy - poly
      for cell in list(hull):
         new_poly = poly.copy()
         new_poly.add(cell)
         yield from polyominos_recursive(n-1, new_poly)

def normalized(polyomino):
   """
   Normalization function to position polyomino in the upper-left-hand-most
   position in row, column space.  Within the polyomino, cells are forced 
   into a canonical order for ease of comparison with other polyominos. 
   Returns a tuple of (row, column) pairs for ease of use in a set. 
   """
   n = len(polyomino)
   xmin = min(x for (x, y) in polyomino)
   ymin = min(y for (x, y) in polyomino)

   new_polyomino = [(x-xmin, y-ymin) for (x, y) in polyomino]
   new_polyomino.sort(key = lambda x:n*x[0]+x[1])
   return tuple(new_polyomino)

def graph(poly):
   """
   Prints a text representation of polyomino. 
   """
   n_rows = max(row for (row, col) in poly) + 1
   n_cols = max(col for (row, col) in poly) + 1
   for row in range(n_rows):
      print(f"\t", end="")
      for col in range(n_cols):
         cell = (row, col)
         graphic = "#" if cell in poly else " "
         print(f"{graphic} ", end="")
      print()

main()
