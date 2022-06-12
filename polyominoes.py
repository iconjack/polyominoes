import sys

def main():
   """
   Program to enumerate all fixed polyominos of order n.
   Revision 3. 
   """

   # Read n from command line.  Display usage and exit on illegal input. 
   try:
      n = int(sys.argv[1])
   except:
      usage()
   if n < 1:
      usage()

   # Copy normalized polyominos into a set to eliminate duplicates. 
   polyomino_set = set()
   for polyomino in polyominos(n):
      polyomino_set.add(normalize(polyomino))

   # Convert set to a list, and sort in canonical order. 
   result = sorted(list(polyomino_set))

   # Print results.
   line = 1
   print(f"")
   print(f"Results:")
   for poly in result:
      print(f"{line:7}\t{list(poly)}")
      print(f"")
      graph(poly)
      print(f"")
      line += 1

   print(f"\tnumber of {prefix(n)}ominos = {len(result)}")

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
   Wrapper for polyomino generator
   """
   yield from polyominos_recursive(n, {(0, 0)} )

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
