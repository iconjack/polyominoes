class Polyomino:
    def __init__(self, cells):
        self.cells = cells

    def __len__(self):
        return len(self.cells)

    @staticmethod
    def normalize_cells(cells):
        """
        Normalization function to position polyomino in the upper-left-hand-most
        position in row, column space.  Within the polyomino, cells are forced 
        into a canonical order for ease of comparison with other polyominos. 
        Returns a tuple of (row, column) pairs for ease of use in a set. 
        """
        n = len(self)
        xmin = min(x for (x, y) in self.cells)
        ymin = min(y for (x, y) in self.cells)

        cells = [(x-xmin, y-ymin) for (x, y) in self.cells]
        return sorted(cells, key = lambda x:n*x[0]+x[1])

    def normalize(self):
        self.cells = normalize_cells(self.cells)

    def normalized(self):
        poly = copy.deepcopy(self)
        poly.normalize()
        return poly

class FreePoly(Polyomino):
    pass

class OneSidedPoly(Polyomino):
    pass

class FixedPoly(Polyomino):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __hash__(self):
        return len(self.cells)
    def __eq__(self, other):
        return 
    



p = FixedPoly()
print(id(p))

