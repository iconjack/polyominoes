#include <stdio.h>
#include <stdint.h>

int main()
{
    printf("sizeof(int)       = %zu\n", sizeof(int));
    printf("sizeof(long)      = %zu\n", sizeof(long));
    printf("sizeof(long long) = %zu\n", sizeof(long long));
    printf("sizeof(uint32_t)  = %zu\n", sizeof(uint32_t));
    printf("sizeof(uint64_t)  = %zu\n", sizeof(uint64_t));
}
