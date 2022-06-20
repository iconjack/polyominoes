
#include <iostream>
#include <time.h>

#define max(a,b) ((a)>(b)) ? (a) : (b)
#define min(a,b) ((a)<(b)) ? (a) : (b)

typedef unsigned int uint32;
typedef signed int int32;

typedef struct poly
{
    struct poly * next;

    uint32 row[32];
    uint32 min_row, max_row;
    uint32 col_mask;
} poly_t, *poly_ptr;

poly_ptr poly_list;
int n_polys;

char* polyomino_name(int n)
{
    const int bufsize = 40;
    char s[bufsize];

    const char* names[] = { "0-ominoes", "monominoes", "dominoes", "triominos", "tetrominoes",
            "pentominoes", "hexominoes", "septominoes", "octominos", "nonominos", "decominos" };

    if (n <= 10)
    {
        sprintf_s(s, bufsize, "%s", names[n]);
    }
    else
    {
        sprintf_s(s, bufsize, "%d-ominos", n);
    }
    return s;
}

void display_poly(poly_t *p)
{
    uint32 i, row, col_mask;

    for (i = p->min_row; i <= p->max_row; i++)
    {
        row = p->row[i];
        col_mask = p->col_mask;

        while (col_mask)
        {
            if (col_mask & 1)
            {
                printf("%c ", (row & 1) ? '#' : ' ');
            }
            col_mask >>= 1;
            row >>= 1;
        }
        printf("\n");
    }
    printf("\n");
}

int debug_target;

void display_poly_big(poly_t* p)
{
    uint32 i, j, row;
    uint32 col_mask, fixed_col_mask;
    char c, foreground, background, deepbackground;
    bool out_of_bounds;

    fixed_col_mask = 0;
    for (i = 0; i < 32; i++)
    {
        fixed_col_mask |= p->row[i];
    }
    
    for (i = 0; i < 32; i++)
    {
        col_mask = fixed_col_mask;
        printf("\t");
        deepbackground = (i == 16) ? '-' : '.';
        row = p->row[i];
        for (j = 0; j < 32; j++)
        {
            background = (j == 16) ? ':' : deepbackground;
            foreground = (row & 1) ? '#' : ' ';
            out_of_bounds = 
                i < p->min_row ||
                i > p->max_row ||
                (col_mask & 1) == 0;

            c = out_of_bounds ? background : foreground;
            printf("%c ", c);
            row >>= 1;
            col_mask >>= 1;
        }

        printf("\n");
    }
    printf("\n");
}


void display_polys()
{
    poly_ptr p;
    int n_polys = 0;

    p = poly_list->next;
    while (p)
    {
        n_polys += 1;
        printf("\n%6d\n", n_polys);
        display_poly(p);
        p = p->next;
    }
    printf("\n");
}

poly_ptr create_poly(void)
{
    poly_ptr p;

    p = (poly_ptr)calloc(1, sizeof(poly_t));
    if (p == NULL)
    {
        exit(-1);
    }
    p->next = NULL;
    return p;
}

void normalize(poly_ptr poly)
{
    uint32 min_row, max_row, n_rows;
    uint32 col_mask;
    uint32 i;

    min_row = poly->min_row;
    max_row = poly->max_row;
    n_rows = max_row - min_row + 1;

    // normalize rows and build column mask
    col_mask = 0;
    for (i = min_row; i <= max_row; i++)
    {
        col_mask |= poly->row[i];
        poly->row[i - min_row] = poly->row[i];
        poly->row[i] = 0;
    }
    poly->min_row = 0;
    poly->max_row = n_rows - 1;;

    // normalize column
    if (col_mask) // should be true, but tested to prevent an endless loop
    {
        while ((col_mask & 1) == 0)
        {
            for (i = 0; i < n_rows; i++)
            {
                poly->row[i] >>= 1;
            }
            col_mask >>= 1;
        }
    }
    poly->col_mask = col_mask;
}

// Function to compare two polyominos of the same order
// Returns 0 if equal, -1 of a < b, +1 if a > b. 
// 
int cmp_poly(poly_ptr a, poly_ptr b)
{
    uint32 i, max_row;
    int result = 0;
    
    max_row = max(a->max_row, b->max_row);

    for (i = 0; i <= max_row; i++)
    {
        if (a->row[i] > b->row[i])
        {
            result = +1;
            break;
        }

        if (a->row[i] < b->row[i])
        {
            result = -1;
            break;
        }
    }

    return result;
}

int find_poly(poly_ptr poly, poly_ptr * prevp, poly_ptr * nextp)
{
    // Assumes poly_list is in order. 
    // Returns +1 if poly_list is empty, 0 if poly is found, -1 otherwise. 
    // The caller's prev and next pointers (*prevp and *nextp) are set to 
    // indicate where poly should be inserted into the polyomino list. 

    poly_ptr prev, next;
    int result = +1;

    prev = poly_list;
    next = poly_list->next;

    while (next != NULL)
    {
        result = cmp_poly(poly, next);
        if (result <= 0)
        {
            break;
        }
        prev = next;
        next = next->next;
    }
    *prevp = prev;
    *nextp = next;

    return result;
}

// Merge a new polyomino into the list, i.e.: add it to the set. 
void merge(poly_ptr p)
{
    poly_ptr prev, next; 
    poly_ptr new_poly;
    int found;

    // prev and next are outputs from find_poly()
    found = (find_poly(p, &prev, &next) == 0);
    if (!found)
    {
        new_poly = create_poly();
        memcpy(new_poly, p, sizeof(poly_t));

        new_poly->next = next;
        prev->next = new_poly;
    }
}

// "Yield" a polyomino by adding it to a list. 
void yield(poly_t poly)
{
    normalize(&poly);
    merge(&poly);   
}

void gen_polys(uint32 n, poly_t poly, poly_t shell)
{
    uint32 i;
    uint32 poly_min_row, poly_max_row, poly_col_mask;
    int32  bits;
    uint32 bit;

    if (n == 1)
    {
        n_polys += 1;
        yield(poly);
        return;
    }

    shell.min_row = poly.min_row - 1;
    shell.max_row = poly.max_row + 1;

    for (i = shell.min_row; i <= shell.max_row; i++)
    {
        shell.row[i] |= poly.row[i + 1];
        shell.row[i] |= poly.row[i - 1];
        shell.row[i] |= poly.row[i] << 1;
        shell.row[i] |= poly.row[i] >> 1;
        shell.row[i] ^= poly.row[i];
    }

    poly_max_row = poly.max_row;
    poly_min_row = poly.min_row;
    poly_col_mask = poly.col_mask;

    for (i = shell.min_row; i <= shell.max_row; i++)
    {
        if (i > poly_max_row) poly.max_row += 1;
        if (i < poly_min_row) poly.min_row -= 1;

        bits = shell.row[i];
        while (bits)
        {
            bit = bits & -bits;

            poly.row[i] |= bit;
            poly.col_mask |= bit;
            gen_polys(n - 1, poly, poly);
            poly.row[i] ^= bit;
            poly.col_mask ^= bit;

            bits ^= bit;
        }

        poly.max_row = poly_max_row;
        poly.min_row = poly_min_row;
    }
}

void check_assumptions(void)
{
    if (sizeof(int) != 4)
    {
        printf("Expected sizeof(int) to be 4, but it is actually %d.\n", sizeof(int));
        exit(-1);
    }
}
void usage(int argc, char* argv[])
{
    printf("usage: %s <n>\n", argv[0]);
    exit(-2);
}

int parse_args(int argc, char* argv[])
{
    if (argc != 2)
    {
        usage(argc, argv);
    }
    return atoi(argv[1]);
}

//---------------------------------------------------------------
int main(int argc, char *argv[])
{
    poly_t monomino;
    int n;
    int n_polys;
    time_t start, stop;
    double elapsed_time;

    printf("Poly ver 0.0, a program to generate fixed polynomials of order n.\n\n");

    // Check assumptions and parse args
    check_assumptions();
    n = parse_args(argc, argv);

    // Create a head node for the polynomial list. 
    poly_list = create_poly();

    // Polyomino construction begins with a monomino in the center of a 32x32 grid. 
    for (int i = 0; i < 32; i++)
    {
        monomino.row[i] = 0;
    }
    monomino.row[16] = 1 << 16;
    monomino.col_mask = 1 << 16;
    monomino.min_row = 16;
    monomino.max_row = 16;
    monomino.next = NULL;
    n_polys = 1;

    // Recursively generate n-ominos.
    time(&start);
    gen_polys(n, monomino, monomino);
    time(&stop);

    // Print out the polyominos. 
    display_polys();
    elapsed_time = difftime(stop, start);

    printf("Generated %d %s in %.2f seconds.", n_polys, polyomino_name(n), elapsed_time);

}

