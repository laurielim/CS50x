#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    int coins = round(dollars * 100);
    int total = 0;

    for (; coins > 24; coins -= 25)
    {
        total += 1;
    }
    for (; coins > 9; coins -= 10)
    {
        total += 1;
    }
    for (; coins > 4; coins -= 5)
    {
        total += 1;
    }
    for (; coins > 0; coins -= 1)
    {
        total += 1;
    }
    printf("%d\n", total);
}
