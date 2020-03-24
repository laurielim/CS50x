#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1  || n > 8);
    for (int blocks = 1, spaces = n - 1;
         blocks <= n;
         blocks++, spaces--)
    {
        for (int i = 0; i < spaces; i++)
        {
            printf(" ");
        }
        for (int i = 0; i < blocks; i++)
        {
            printf("#");
        }
        printf("  ");
        for (int i = 0; i < blocks; i++)
        {
            printf("#");
        }
        printf("\n");
    }
        
}
