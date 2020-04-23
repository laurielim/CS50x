// Implements a dictionary's functionality

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 547;

// Hash table
node *table[N] = {NULL};

// Word count and counter pointer
int count = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    int key = hash(word);

    // Check if bucket is empty
    if (table[key] != NULL)
    {
        // Traverse list
        node *cursor = table[key];
        while (cursor != NULL)
        {
            if (strcasecmp(cursor->word, word) == 0)
            {
                return true;
            }
            else
            {
                cursor = cursor->next;
            }
        }
    }
        
    return false;
}

// Hashes word to a number
// Hash function djb2 by Dan Bernstein as found on http://www.cse.yorku.ca/~oz/hash.html
unsigned int hash(const char *word)
{
    {
        unsigned long hash = 5381;
        int c;

        while ((c = *word++))
        {
            hash = ((hash << 5) + hash) + tolower(c);
        }

        return hash % N;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary file and check for error
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return 1;
    }
    
    // Create buffer to store words
    char buffer[LENGTH + 1];
    int index = 0;

    // Read strings from file one string at a time until end of file
    while (fscanf(file, "%s", buffer) != EOF)
    {
        // Create a new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            // Close the file
            fclose(file); 
            return false;
        }
        
        // Hash word to obtain a hash value
        int key = hash(buffer);
        
        // Copy word into new node
        strcpy(n->word, buffer);
        // Insert node into hash table
        n->next = table[key];
        table[key] = n;
        count++;
    }
    // Close the file
    fclose(file); 
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Iterate through the bucket
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
            
        // Traverse list freeing nodes
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
