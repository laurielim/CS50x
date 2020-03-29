#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        int n = strlen(argv[1]);
        for (int i = 0; i < n; i++)
        {
            if (isdigit(argv[1][i]) == 0)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    string p = get_string("plaintext: ");
    int k = atoi(argv[1]);
    int pn = strlen(p);
    int c[pn];
    for (int i = 0; i < pn; i++)
    {
        if (p[i] > 64 && p[i] < 91)
        {
            c[i] = (((int) p[i] - 64 + k) % 26) + 64;
        }
        else if (p[i] > 96 && p[i] < 123)
        {
            c[i] = (((int) p[i] - 96 + k) % 26) + 96;
        }
        else
        {
            c[i] = (int) p[i];
        }
        
    }
    
    printf("ciphertext: ");
    for (int i = 0; i < pn; ++i)
    {
        printf("%c", c[i]);
    }
    printf("\n");
    return 0;
}
