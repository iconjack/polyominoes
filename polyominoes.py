import sys
import time
import argparse

def main():
   """
   Program to enumerate all fixed polyominoes of order n.
   Revision 7.
   """
   parser = argparse.ArgumentParser(
      description="Enumerate all fixed polyominoes or order n.",
      allow_abbrev=False)
   parser.add_argument('n', type=int, help="number of live cells")
   parser.add_argument('-d', '--display', dest='display', action='store_true',
      help="display generated polyominoes")
   parser.add_argument('-t', '--time', dest='timing', action='store_true',
      help="time the run")
   parser.set_defaults(display=False, timing=False)

   args = parser.parse_args()
   n = args.n

   # Mark start time
   start_time = time.time()

   # Copy normalized polyominoes into a set to eliminate duplicates. 
   polyomino_set = {normalized(p) for p in polyominoes(n)}

   # Convert set to a list, and sort in canonical order. 
   result = sorted(list(polyomino_set))

   # Mark stop time and measure elapsed time
   stop_time = time.time()
   elapsed_time = stop_time - start_time

   if args.display:
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
   if args.timing:
      print(f"\telapsed time = {elapsed_time:0.3f} seconds")

def prefix(n):
   """
   Function to provide polyomino name prefixes
   """
   try:
      pre = ["poly", "mon", "d", "tri", "tetr", "pent", "hex", "hept", "oct", "non", "dec", "undec", "dodec"][n]
   except:
      pre = f"{n}-"
   return pre

def polyominoes(n):
   """
   Helper generator to kick off recursive generator with single cell seed
   """
   seed_poly = {(0,0)}
   yield from polyominoes_recursive(n, seed_poly )

def polyominoes_recursive(n, poly):
   """
   Recursive generator of polyominoes of order n.
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
         yield from polyominoes_recursive(n-1, new_poly)

def normalized(polyomino):
   """
   Normalization function to position polyomino in the upper-left-hand-most
   position in row, column space.  Within the polyomino, cells are forced 
   into a canonical order for ease of comparison with other polyominoes. 
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

if __name__ == "__main__":
   main()
