import polynomials

def valence(poly):

// determines whether two grids are equal (equivalent)
    // i.e. the same mod rotations and reflections

    public override bool Equals(Object o)
    {
        Grid g = o as Grid;
        if (g == null) return false;
        int[,] a = g._a, b = this._a;

        bool b1 = true, b2 = true, b3 = true, b4 = true, b5 = true, b6 = true, b7 = true, b8 = true;

        for (int i = 0; i < _n; i++)
        {
            for (int j = 0; j < _n; j++)
            {
                int ibar = _n-1-i, jbar = _n-1-j;
                b1 &= a[i, j] == b[i, j];           // identity
                b2 &= a[i, j] == b[i, jbar];        // vertical center line
                b3 &= a[i, j] == b[ibar, j];        // horizontal center line
                b4 &= a[i, j] == b[ibar, jbar];     // main diagonal
                b5 &= a[i, j] == b[j, i];          
                b6 &= a[i, j] == b[jbar, i];
                b7 &= a[i, j] == b[j, ibar];
                b8 &= a[i, j] == b[jbar, ibar];
            }
        }
        return b1 || b2 || b3 || b4 || b5 || b6 || b7 || b8;
    }
}


