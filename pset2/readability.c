#include <stdio.h>
#include <math.h>
#include <cs50.h>

//Compute the Coleman-Liau index
int cl_index(float l, float s);
//Compute average num per 100 words
float per100words(int num, int den);

int main(void)
{

    string s = get_string("Text: ");

    int letters = 0, words = 1, sentences = 0;

    for (int i = 0; s[i] != '\0'; ++i)
    {
        if (s[i] == 32)
        {
            words += 1;
        }
        else if (s[i] == 46 || s[i] == 63 || s[i] == 33) //Includes abbreviations that end with a period e.g: "Mr." or "Mrs."
        {
            sentences += 1;
        }
        else if ((s[i] > 64 && s[i] < 91) || (s[i] > 96 && s[i] < 123))
        {
            letters += 1;
        }
    }

    float avg_letters = per100words(letters, words);
    float avg_sentences = per100words(sentences, words);
    int index = cl_index(avg_letters, avg_sentences);

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int cl_index(float l, float s)
{
    return roundf(0.0588 * l - 0.296 * s - 15.8);
}

float per100words(int num, int den)
{
    return ((float) num * 100 / (float) den) ;
}
